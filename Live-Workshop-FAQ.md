# AWS Live Streaming and Live-to-VOD Workshop FAQ:

## AWS IAM

## AWS MediaLive

**Q. I can't delete my AWS Elemental MediaLive input.** 

A. Your input is still attached to a channel. You must first delete the channel before you can delete the input. 


**Q. I can't delete my AWS Elemental MediaLive channel.**

A. Your channel is still in a running state. You must first stop the channel before you can delete it. 

## AWS MediaPackage

**Q. There seems to be no data or content making it to AWS Elemental MediaPackage.**

A. When copy/pasting anything from the console (ie. MediaLive Role ARN, MediaPackage endpoint username/password), make sure that there are no trailing spaces.

**Q. The player (Live or VOD) won’t load or playback any output.**

A. You might be using the MediaPackage’s Input URL instead of the Endpoint URL. For playback, you want to use the Endpoint URL.

**Q. I can't delete my AWS Elemental MediaPackage channel.**

A. Delete all origin endpoints from the channel before deleting the channel.

## Browser

**Q. VOD playback doesn't work. Player just spins or starts from the live edge.**

A. The ISO timestamp you entered for the Start or End time might be in the wrong format. Make sure it's in the following format: *YYYY-MM-DDTHH:MM:SS.SSSZ*.


## AWS CloudWatch

**Q. I don't see any egress data in the graphs, what's wrong?**

A. Make sure there is playback happening to generate egress metric data. After a minute or two of playback, egress graphs will populate.
