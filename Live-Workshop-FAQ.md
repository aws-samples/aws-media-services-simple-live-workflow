# AWS Live Streaming and Live-to-VOD Workshop FAQ:

**Q. There seems to be no data or content making it to AWS Elemental MediaPackage.**

A. When copy/pasting anything from the console (ie. MediaLive Role ARN, MediaPackage endpoint username/password), make sure that there are no trailing spaces.


**Q. The player (Live or VOD) won’t load or playback any output.**

A. You might be using the MediaPackage’s Input URL instead of the Endpoint URL. For playback, you want to use the Endpoint URL.

**Q. VOD playback doesn't work. Player just spins or starts from the live edge.**

A. The ISO timestamp you entered for the Start or End time might be in the wrong format. Make sure it's in the following format: *YYYY-MM-DDTHH:MM:SS.SSSZ*.

