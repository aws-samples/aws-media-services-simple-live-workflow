import json
import boto3
import os
from botocore.vendored import requests
import string
from urllib.parse import urlparse
import resource_tools

def lambda_handler(event, context):
    print("Event Input: %s" % json.dumps(event))
    emt_client = boto3.client('mediatailor') 

    # get environment variables
    distribution_id = os.environ["CloudFrontDistributionId"]
    video_source = os.environ["VideoSource"]
    ad_server = os.environ["ADS"]

    # make up the configuration name
    emt_config_name = "%s-%s" % (resource_tools.stack_name(event), event["LogicalResourceId"])

    response = {}
    result = {
        "Status": "SUCCESS",
        "Data": response,
        "ResourceId": emt_config_name
    }
    
    if event["RequestType"] == "Create" or event["RequestType"] == "Update":
        cf_client = boto3.client('cloudfront')
        session = boto3.session.Session()
        region = session.region_name

        # all the info we need to set up a proper distribution
        parsed_url = urlparse(video_source)
        source_domain_name = parsed_url.netloc
        # remove the asset name (eg. index.m3u8) from the path
        url_path_list = parsed_url.path.split('/')
        asset_name = url_path_list.pop(-1)
        source_path = ('/').join(url_path_list)

        # CloudFront distro info
        distribution_info = cf_client.get_distribution(Id = distribution_id)
        distribution_domain_name = distribution_info['Distribution']['DomainName']
        distribution_config = distribution_info['Distribution']['DistributionConfig']
        etag = distribution_info['ETag']
    
        cdn_prefix = "https://" + distribution_domain_name
        cdn_segment_prefix = cdn_prefix + source_path
        video_source_without_asset_name = "https://" + source_domain_name + source_path
        emt_data = {}
        try:
            emt_data = emt_client.put_playback_configuration(
                AdDecisionServerUrl=ad_server,
                Name=emt_config_name,
                VideoContentSourceUrl=video_source_without_asset_name,
                CdnConfiguration={
                    "AdSegmentUrlPrefix": cdn_prefix,
                    "ContentSegmentUrlPrefix": cdn_segment_prefix
                }
            )
            parsed_emt_url = urlparse(emt_data["HlsConfiguration"]["ManifestEndpointPrefix"])
            hls_playback_path = parsed_emt_url.path
            ads_domain_name = "ads.mediatailor." + region + ".amazonaws.com"
            meditailor_domain_name = parsed_emt_url.netloc
    
            result["Data"] = {
                "ConfigurationName": emt_config_name,
                "HLSPlaybackURL": emt_data["HlsConfiguration"]["ManifestEndpointPrefix"] + asset_name,
                "CloudFrontPlaybackURL": cdn_prefix + hls_playback_path + asset_name
            }  
            #update the origins of the CloudFront Distribution
            response = update_distribution_origins(cf_client, distribution_config, distribution_id, etag, 
                source_domain_name, meditailor_domain_name, ads_domain_name )
            print("CloudFront update origins response: %s" % response)
            #if successful, update the cache behaviors of the distribution
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                #get the latest distribution information after origin update
                distribution_info = cf_client.get_distribution(Id = distribution_id)
                distribution_config = distribution_info['Distribution']['DistributionConfig']
                etag = distribution_info['ETag']
                response = update_distribution_cache_behaviors(cf_client, distribution_config, distribution_id, etag)
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print("CloudFront update cache behaviors response: %s" % response)
                else:
                    result["Status"] = "FAILED",
        except Exception as exp:
            print("Exception: %s" % exp)
            result["Status"] = "FAILED"
            result["Data"] = {"Exception": str(exp)}

    elif event["RequestType"] == "Delete":
        try:
            result["Data"] = emt_client.delete_playback_configuration(Name=emt_config_name)
        except Exception as exp:
            print("Exception: %s" % exp)
            result["Status"] = "FAILED",
            result["Data"] = {"Exception": str(exp)}

    resource_tools.send(event, context, result["Status"],
         result["Data"], result["ResourceId"])
    return


def update_distribution_origins(client, distribution_config, distribution_id, etag,
                mediapackage_origin, mediatailor_origin, ads_origin):
    distribution_config['Comment'] = "CloudFront for MediaPackage and MediaTailor"
    distribution_config['Origins'] = {
                'Quantity': 3,
                'Items': [
                    {
                        'Id': 'MediaPackage',
                        'DomainName': mediapackage_origin,
                        'OriginPath': '',
                        'CustomHeaders': {
                            'Quantity': 0
                        },
                        'CustomOriginConfig': {
                            'HTTPPort': 80,
                            'HTTPSPort': 443,
                            'OriginProtocolPolicy': 'https-only',
                            'OriginReadTimeout': 30,
                            'OriginKeepaliveTimeout': 5,
                            'OriginSslProtocols': {
                                'Quantity': 4,
                                'Items': [
                                    'SSLv3',
                                    'TLSv1',
                                    'TLSv1.1',
                                    'TLSv1.2'
                                ]
                            }
                        }
                    },
                    {
                        'Id': 'MediaTailor',
                        'DomainName': mediatailor_origin,
                        'OriginPath': '',
                        'CustomHeaders': {
                            'Quantity': 0
                        },
                        'CustomOriginConfig': {
                            'HTTPPort': 80,
                            'HTTPSPort': 443,
                            'OriginProtocolPolicy': 'https-only',
                            'OriginReadTimeout': 30,
                            'OriginKeepaliveTimeout': 5,
                            'OriginSslProtocols': {
                                'Quantity': 4,
                                'Items': [
                                    'SSLv3',
                                    'TLSv1',
                                    'TLSv1.1',
                                    'TLSv1.2'
                                ]
                            }
                        }
                    },
                    {
                        'Id': 'AdvertisementService',
                        'DomainName': ads_origin,
                        'OriginPath': '',
                        'CustomHeaders': {
                            'Quantity': 0
                        },
                        'CustomOriginConfig': {
                            'HTTPPort': 80,
                            'HTTPSPort': 443,
                            'OriginProtocolPolicy': 'https-only',
                            'OriginReadTimeout': 30,
                            'OriginKeepaliveTimeout': 5,
                            'OriginSslProtocols': {
                                'Quantity': 4,
                                'Items': [
                                    'SSLv3',
                                    'TLSv1',
                                    'TLSv1.1',
                                    'TLSv1.2'
                                ]
                            }
                        }
                    }
                ]
            }
    response = client.update_distribution(
        DistributionConfig = distribution_config,
        Id = distribution_id,
        IfMatch = etag
    )    
    return response

def update_distribution_cache_behaviors(client, distribution_config, distribution_id, etag):
    #update Default Cache Behavior
    distribution_config['DefaultCacheBehavior'] = {
                'TargetOriginId': 'AdvertisementService',
                'ForwardedValues': {
                    'QueryString': True,
                    'Cookies': {
                        'Forward': 'none',
                    },
                    'Headers': {
                        'Quantity': 0
                    },
                    'QueryStringCacheKeys': {
                        'Quantity': 0
                    }
                },
                'TrustedSigners': {
                    'Enabled': False,
                    'Quantity': 0,
                },
                'ViewerProtocolPolicy': 'allow-all',
                'MinTTL': 0,
                'AllowedMethods': {
                    'Quantity': 2,
                    'Items': [
                        'GET',
                        'HEAD'
                    ],
                    'CachedMethods': {
                        'Quantity': 2,
                        'Items': [
                            'GET',
                            'HEAD',
                        ]
                    }
                },
                'SmoothStreaming': False,
                'DefaultTTL': 86400,
                'MaxTTL': 31536000,
                'Compress': False,
                'LambdaFunctionAssociations': {
                    'Quantity': 0
                },
                'FieldLevelEncryptionId': ''
            }
    #update Cache Behaviors
    distribution_config['CacheBehaviors'] =  {
                'Quantity': 2,
                'Items': [
                    {
                        'PathPattern': '/v1/*',
                        'TargetOriginId': 'MediaTailor',
                        'ForwardedValues': {
                            'QueryString': True,
                            'Cookies': {
                                'Forward': 'none'
                            },
                            'Headers': {
                                'Quantity': 0
                            },
                            'QueryStringCacheKeys': {
                                'Quantity': 0
                            }
                        },
                        'TrustedSigners': {
                            'Enabled': False,
                            'Quantity': 0
                        },
                        'ViewerProtocolPolicy': 'allow-all',
                        'MinTTL': 0,
                        'AllowedMethods': {
                            'Quantity': 2,
                            'Items': [
                                'GET',
                                'HEAD',
                            ],
                            'CachedMethods': {
                                'Quantity': 2,
                                'Items': [
                                    'GET',
                                    'HEAD'
                                ]
                            }
                        },
                        'SmoothStreaming': False,
                        'DefaultTTL': 86400,
                        'MaxTTL': 31536000,
                        'Compress': False,
                        'LambdaFunctionAssociations': {
                            'Quantity': 0
                        },
                        'FieldLevelEncryptionId': ''
                    },
                    {
                        'PathPattern': '/out/v1/*',
                        'TargetOriginId': 'MediaPackage',
                        'ForwardedValues': {
                            'QueryString': True,
                            'Cookies': {
                                'Forward': 'none'
                            },
                            'Headers': {
                                'Quantity': 0
                            },
                            'QueryStringCacheKeys': {
                                'Quantity': 0
                            } 
                        },
                        'TrustedSigners': {
                            'Enabled': False,
                            'Quantity': 0
                        },
                        'ViewerProtocolPolicy': 'allow-all',
                        'MinTTL': 0,
                        'AllowedMethods': {
                            'Quantity': 2,
                            'Items': [
                                'GET',
                                'HEAD',
                            ],
                            'CachedMethods': {
                                'Quantity': 2,
                                'Items': [
                                    'GET',
                                    'HEAD'
                                ]
                            }
                        },
                        'SmoothStreaming': False,
                        'DefaultTTL': 86400,
                        'MaxTTL': 31536000,
                        'Compress': False,
                        'LambdaFunctionAssociations': {
                            'Quantity': 0
                        },
                        'FieldLevelEncryptionId': ''
                    }
                ]
            }
    response = client.update_distribution(
        DistributionConfig = distribution_config,
        Id = distribution_id,
        IfMatch = etag
    )
    return response