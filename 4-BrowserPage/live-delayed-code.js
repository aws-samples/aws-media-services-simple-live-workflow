// video element ids
var live_player_id = "video_player_live";
var delayed_player_id = "video_player_delayed";

// HLS endpoint
//Replace live_video_source with the first endpoint of the Primary MediaPackage Channel
var live_video_source = "http://d2qohgpffhaffh.cloudfront.net/HLS/vanlife/sdr_uncage_vanlife.m3u8";
//Replace delayed_video_source with the second endpoint of the same Primary MediaPackage Channel
var delayed_video_source = "http://d2qohgpffhaffh.cloudfront.net/HLS/vanlife/sdr_uncage_vanlife.m3u8";

// initalize the page
$(document).ready(() => {
    // set the live player
    prepare_player(live_player_id, live_video_source);
    // set the time delayed player
    prepare_player(delayed_player_id, delayed_video_source);
    //display the source URLs of the two players
    $("#live_source_URL").text("URL: " + live_video_source);
    $("#delayed_source_URL").text("URL: " + delayed_video_source);
});

// set the specified player with the source URL
var prepare_player = (id, source) => {
    console.log("id = " + id);
    console.log("source = " + source);
    let player = videojs("#" + id);
    player.reset();
    player.src({
        "src": source,
        "type": "application/x-mpegURL"
    });
    player.load();
    player.play();
}