/**
 * Created by nikita_kartashov on 16/11/2013.
 */

function handleRetweets() {
    var retweets = $('div.tweet[is_retweet="True"]');
    var checkbox = $("#displayRetweetsCheckBox");
    handleCheckboxState(checkbox, retweets);
}

function handlePositiveTweets() {
    var positive_tweets = $("div.tweet.positive");
    var checkbox = $("#displayPositiveTweetsCheckBox");
    handleCheckboxState(checkbox, positive_tweets)
}

function handleNegativeTweets() {
    var negative_tweets = $("div.tweet.negative");
    var checkbox = $("#displayNegativeTweetsCheckBox");
    handleCheckboxState(checkbox, negative_tweets)
}

function handleCheckboxState(checkbox, elements){
   if (checkbox.prop("checked")) {
       elements.show();
   }
   else {
       elements.hide();
   }
}

function handleTweetsDisplay() {
    handleRetweets();
    handlePositiveTweets();
    handleNegativeTweets();
}