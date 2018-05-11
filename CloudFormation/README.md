# CloudFormation Templates

CloudFormation templates are available if you would like to move faster or see the intended outcome of a single module or the entire lab. Following are links to CloudFormation templates for each module of the workshop. **Copy the link address and use that with CloudFormation to create the module contents in your account.** You may need to enter information into the CloudFormation template about resources created in previous modules. If you are not familiar with AWS CloudFormation, review the online [User Guide](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html). 


## Prerequisites

### Permissions

The CloudFormation templates rely on permissions necessary to create and configure the AWS Cloud services from each module. These are the same permission you will need to perform the creation and configuration of the AWS Cloud services manually.

### Hosting

The current templates can be downloaded here and run individually. They can also be run from the hosted location within AWS using the links below. The main template named LiveStreamingWorkshopResources.json includes hosted links to the subordinate templates. If you plan to fork and modify these templates, you will need to consider hosting them to take advantage of the nesting.

## Templates

**These templates are supported in regions: us-west-2, us-east-1, and eu-west-1.**

- [**Entire Workshop**](https://s3-us-west-2.amazonaws.com/rodeolabz-us-west-2/cloudformation/LiveStreamingWorkshopResources.json) - This template will perform all the configuration steps of modules 1, 2, 3 and the Extra Cloudwatch module.

- [**AWS IAM**](https://s3-us-west-2.amazonaws.com/rodeolabz-us-west-2/cloudformation/IAMResources.json)

- [**AWS Elemental MediaPackage**](https://s3-us-west-2.amazonaws.com/rodeolabz-us-west-2/cloudformation/MediaPackageResources.json)

- [**AWS Elemental MediaLive**](https://s3-us-west-2.amazonaws.com/rodeolabz-us-west-2/cloudformation/MediaLiveResources.json)

- **Browser Page** (not applicable)

- [**AWS Elemental MediaTailor**](https://s3-us-west-2.amazonaws.com/rodeolabz-us-west-2/cloudformation/CreateCloudfrontDistribution.json) - This template only automates the creation of CloudFront for MediaTailor. This does **not** automate the MediaTailor configuration creation. 

- [**Extra: AWS CloudWatch**](https://s3-us-west-2.amazonaws.com/rodeolabz-us-west-2/cloudformation/CloudWatchResources.json)


## Completion

At the end of the module you learned how to test streaming video endpoints using web and standalone players. You learned about the design of browser pages that support video playback, how different security models of browsers effect streaming playback, and how to access live and restart window streams of the origin service using URL parameters. 

Return to the [main](../README.md) page.

## Cloud Resource Clean Up

Deleting a deployed stack through the CloudFormation console will remove all resources created with the template or templates previously applied. The CloudFormation templates for AWS Elemental MediaLive will automatically start and stop channels to allow several steps to be completed without user intervention.

You should always try to use CloudFormation to remove resources created by templates. If that is not possible, consult the CloudFormation documentation on the best practices for cleaning up a problematic stack.

