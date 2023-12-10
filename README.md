# SummarizeBot-Medium-Discord-Notifier
This Discord Bot notify a new medium post and summarize it with AI model BERT

## Prerequisites

Before using SummarizeBot, make sure you have the following:

- **Medium Feed URL:** Obtain the URL for the Medium feed you want to monitor.
- **Discord Webhook URL:** Create a Discord webhook on the channel where you want notifications and obtain the URL.
- **`processed_posts.txt`:** Create a file named `processed_posts.txt` in the directory where the script will run.

## Libraries Required

Ensure you have the necessary Python libraries installed:

```bash
pip install feedparser discord-webhook requests transformers
```

## Running Automatically

For windows, use task scheduler to schedule the execution of the python script at reguler intervals


