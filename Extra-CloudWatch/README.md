# Extra Module 5: CloudWatch

In this module you'll use AWS CloudWatch to monitor certain operational and performance metrics for the AWS Elemental MediaLive and AWS Elemental MediaPackage channels you had set up in previous modules. You will set up alarms for when certain conditions are met and notifications for when these alarms are triggered.

## Prerequisites

### Previous Modules

This module relies on the having completed all prior modules on IAM, AWS Elemental MediaLive and AWS Elemental MediaPackage. You must also have handy the **AWS Elemental MediaLive Channel ID** of the MediaLive channel you've previously created, as well as the **AWS Elemental Mediapackage Channel Name**.  

## Implementation Instructions

### 1. Graph AWS Elemental MediaLive Metrics
In this section, you will be graphing the Network Out metrics of the AWS Elemental MediaLive channel you created in a previous module. 

**Step-by-step instructions**

1. From the AWS Console click **Services** then select **CloudWatch**.

1. At the top right corner of your screen, make sure you are in **US West(Oregon)** region.

1. On the left navigation pane, click on **Metrics**. 

1. Under **All Metrics**, put `MediaLive` in the search textbox and hit Enter. This will give you all relevant metrics for the AWS Elemental MediaLive service. 

1. Click on `MediaLive > ChannelId, Pipeline`, and add the Channel ID of the MediaLive channel you previously created in the search textbox and hit Enter. This will return all relevant metrics for your channel. 

1. Select **NetworkOut** for both pipelines 0 and 1. The selected metrics will now get reflected in the graphed area. 

1. Give the graph a title of `MediaLive Channel <ChannelNumber> NetworkOut`.


### 2. Add AWS Elemental MediaLive Graphed Metrics to Dashboard

**Step-by-step instructions**

1. Now that you've created a graphed metric, we will add this to a dashboard. Click on **Actions** and select **Add to Dashboard**. 

1. Click on the **Create New** link.

1. Enter `MediaLive_MediaPackage_Channels_Metrics` for the **Dashboard Name**.

1. Take all other defaults and click the **Add to dashboard** button. 
This will take you to the **Dashboards** page. 

1. Stretch the graph so it fills the width of your screen. 

1. Click on **Save Dashboard** button.

**Step-by-step instructions**


### 3. Graph AWS Elemental MediaPackage Metrics

**Step-by-step instructions**

1. On the left navigation pane, click on **Metrics**. 

1. Under **Graphed Metrics** tab, delete existing selected metrics.

1. Under **All Metrics** tab, click on the **All** link and clear the search textbox (remove `MediaLive` and the channel ID you entered). 

1. Put `MediaPackage` in the search textbox and hit Enter. This will give you all relevant metrics for the AWS Elemental MediaPackage service.  

1. Click on `MediaPackage > Per Origin Endpoint`, and add the Channel Name of the MediaPackage channel you previously created in the search textbox and hit Enter. This will return all relevant metrics for your channel. 

1. Select **EgressBytes** for your Channel. The selected metrics will now get reflected in the graphed area. 

1. Edit the graph title and enter `MediaPackage Channel Egress Bytes`. Save your title by clicking on the check mark icon. 

1. Under **Graphed Metrics** tab, set **Period** to every **1 minute**. Set **Statistics** to **Sum**.

### 4. Add AWS Elemental MediaPackag Graphed Metrics to Dashboard

**Step-by-step instructions**

1. Click on **Actions** and select **Add to Dashboard**. Add to the Dashboard you created earlier (`MediaLive_MediaPackage_Channels_Metrics`).

1. Stretch the graph so it fills the width of your screen. 

1. Take all other defaults and click the **Add to dashboard** button. This will take you to the **Dashboards** page. Click on **Save Dashboard** button.

### 5. Setup Alarm and Notification

In this section, we're going to set up two alarms and notifications based on the Egress Bytes of your MediaPackage Channel Endpoint. Whenever the Egress Bytes meets a certain threshold, an alarm will be raised, and notification sent. 

**Step-by-step instructions**

1. On the left navigation pane, click on **Alarms**. Then click on **Create Alarm** button. 

1. In the **Search Metrics** textbox, enter the name of your MediaPackage channel and hit Enter. 

1. Under **MediaPackage > Per Origin Endpoint**, select **Egress Bytes** and click Next.

1. Enter `MediaPackage Egress Bytes - Low` for **Name**. Enter same for **Description**. 

1. For the condition **Whenever: Egress Bytes**, set **is** to `<= 10000000`.

1. Under **Alarm Preview**, set **Period** to **1 minute** and **Statistic** to **Standard**, **Sum**.

1. Under **Actions**, **Set Notifications To**, click on **New List**.
    1. For **Topic Name**, enter `MediaPackage_Notification`.
    1. For **Email List**, enter a valid email address if you want to be able to receive the notification that gets sent when your Alarm gets triggered.

1. Click on **Save Changes** button. This will pop up a window to confirm the email address that you provided. You can choose to do it later, in which case you won't receive notifications. Or you can verify it via a link that gets sent to the email address you provided.

1. On the left navigation pane, click on **Alarms**. Then click on **Create Alarm** button. 

1. In the **Search Metrics** textbox, enter the name of your MediaPackage channel and hit Enter. 

1. Under **MediaPackage > Per Origin Endpoint**, select **Egress Bytes** and click Next.

1. Enter `MediaPackage Egress Bytes - Normal` for **Name**. Enter same for **Description**. 

1. For the condition **Whenever: Egress Bytes**, set **is** to `> 10000000`.

1. Under **Alarm Preview**, set **Period** to **1 minute** and **Statistic** to **Standard**, **Sum**.

1. Under **Actions**, **Set Notifications To**, select the list you created previously, `MediaPackage_Notification`.

1. Click on **Save Changes** button. 

1.  On the left navigation pane, click on **Alarms**. Then enter `Egress` in the search textbox. This should now display the two alarms you just created.




## Completion

Return to the [main](../README.md) page.




## Cloud Resource Clean Up

Remove the AWS CloudWatch dashboard when you are finished with it.

