# Module 1: AWS IAM

This module guides the participant in configuring permissions for the AWS services used in this workshop. You will learn how to create and manage policies that permit access for users in your account to AWS Elemental MediaLive. You will attach these policies to roles and users in your account.

## Prerequisites

### Pre-configured AWS Account

If you are using a pre-configured AWS account, you will need to retrieve the ARN for the IAM Role that allows AWS Elemental MediaLive to access resources in your account.

1. Navigate to the AWS IAM Console
1. Select Roles
1. Find the Role previously defined to AWS Elemental MediaLive access
1. Select the Role to show it's summary
1. Select and copy the Role's ARN at the top of the page
1. Paste the Role ARN into text editor to save for later in the workshop
1. Skip forward to the next module

### No previous account configuration

In order to complete this workshop you'll need an AWS Account with access to create policies and roles within the AWS Identity and Access Management (IAM) service. 

The signed-in user must have the AdministratorAccess policy or a policy that allows the user to access all actions for the mediapackage service and at least read access to CloudWatch. The steps for creating a policy for AWS Elemental MediaPackage is covered near the end of this module.

The code and instructions in this workshop assume only one student is using a given AWS account at a time. If you try sharing an account with another student, you'll run into naming conflicts for certain resources. You can work around this by either using a suffix in your resource names or using distinct Regions, but the instructions do not provide details on the changes required to make this work.

### Region

AWS MediaLive and AWS MediaPackage are available in several regions. But for the purpose of this lab, we will use the **US West (Oregon)** region.

### Creating a Role to Use with AWS Elemental MediaLive
AWS Elemental MediaLive needs permission to make calls to AWS APIs on your behalf. For example,
credentials such as AWS Elemental MediaPackage or input passwords must be stored in the Parameter Store of EC2 Systems Manager.
The password key is then expected to be given to AWS Elemental MediaLive when creating the channel. AWS
Elemental MediaLive needs permission to access the value of the key from EC2 Systems Manager.

To create a role to use with AWS Elemental MediaLive:
1. Go to IAM -> Roles
1. Click on Create Role

    ![alt](CreateRole.png)

1. Select **AWS Service** under type of trusted entity, and **EC2** as the service that will use this role.
1. Click on Next:Permissions button,
1. In the Filter Policies search box, enter `AmazonSSMReadOnlyAccess` and select the checkbox of the matching policy.
1. In the Filter Policies search box, enter `CloudWatchLogsFullAccess` and select the checkbox of the matching policy.
1. Click on Next:Tags button.
1. Click on Next:Review button.
1. Give the role a name such as `AllowMediaLiveAccessRole`.
1. Click on Create Role.
1. Search for the newly created role in the IAM Roles page by typing `AllowMediaLiveAccessRole` in the search box.
1. Click on the newly created role.
1. Under **Permissions**, click on the **Add inline policy** link.
1. Click on the **JSON** tab.
1. Replace the policy with the following:
    ```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": "mediaconnect:Managed*",
                "Resource": "*"
            }
        ]
    }
    ```
1. Click on Review Policy. 
1. Give the policy a name like `MediaConnectManagedPolicy`. This allows MediaLive to create MediaConnect inputs, if you're using them.
1. Click on Create Policy.
1. Click on tab called **Trust relationships**.
1. Click on Edit trust relationship
1. Replace the existing policy with the following in the Policy Document edit window:
    ```
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "ec2.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        },
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "medialive.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
    ```
1. Click on Update Trust Policy.

### Adding AWS Elemental MediaLive permissions to the current signed-in IAM user
If the current user does not have the AdministratorAccess policy, use the following steps to attach a IAM policy to the user that allows access to AWS Elemental MediaLive.
1. Go to IAM > Users
1. Find your currently signed-in user at the top-right of the console page.

    ![alt](IAMUsers.png)

1. Find the same user in the user list and click it to see details.
1. Click the **Add Permissions button**
1. Click **Attach existing policies directly**
1. Attach ‘AmazonS3ReadOnlyAccess’ and ‘CloudWatchReadOnlyAccess’ policies to
the user.
1. Click Next: Review
1. Click Add Permissions
1. Click on Add inline policy at the bottom right of the Permissions tab
1. Click on Custom Policy and click the Select button
1. For Policy name, use something like MedialiveAccessPolicy. In the policy document field, paste the following.
1. Replace the value of the Resource attribute in the last statement of the policy with the Role ARN you created previously in this module
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "medialive:*"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "INSERT ROLE ARN HERE" 
    }
  ]
}
```
13. Click on Validate Policy to check for typos, then click Apply Policy

### Adding AWS Elemental MediaPackage permissions to a IAM user (optional)

If the current user does not have the AdministratorAccess policy, use the following steps to attach a IAM policy to the user that allows access to AWS Elemental MediaPackage.

1. From the user's Summary page in IAM, click on Add inline policy at the bottom right of the Permissions tab
1. Click on Custom Policy and click the Select button
1. For Policy name, use something like MediaPackageAccessPolicy. In the policy document field, paste the following:
    ```
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "mediapackage:*"
          ],
          "Resource": "*"
        }
      ]
    }
    ```
1. Click on Validate Policy to check for typos, then click Apply Policy

## Completion

At the end of the module you have created a IAM Role to allow access from MediaLive to resources in your account. You have also added MediaLive and, optionally, MediaPackage permissions to the signed-in user.

Move forward to the next module to configure [**AWS Elemental MediaPackage**](../2-MediaPackage/README.md).

Return to the [main](../README.md) page.

## Cloud Resource Clean Up

To manually remove resources created in this module, go to the AWS IAM console and remove the Role created here.

