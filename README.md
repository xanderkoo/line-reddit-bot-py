# line-reddit-bot-py
LINE Bot for Reddit Posts

Simple app to get a specified number of Reddit posts (via LINE) from a specified subreddit by sending a message to the LINE bot, e.g. "r/pics 10". Made this to try and take advantage of the fact that my current mobile data plan gives me unlimited use of LINE, but not Reddit.

Once the LINE bot receives a message, it sends a webhook to an endpoint and then this program handles the input, scrapes the appropriate posts, and triggers a reply from the bot back to the user.

Uses the LINE Messaging API, Python Reddit API Wrapper (PRAW), with the webhook endpoint hosted on Google Cloud Platform.

Unfortunately the project has hit a wall because I've hit my monthly limit of 1000 (or maybe 500?) broadcast messages from the free plan on the LINE Messaging API. Maybe it'll work if I make it all of the images reply messages (i.e. one post at a time).
