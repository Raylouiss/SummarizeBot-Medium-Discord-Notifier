import os
import feedparser
from discord_webhook import DiscordWebhook
from transformers import pipeline
from bs4 import BeautifulSoup

# URL of the Medium RSS feed
medium_rss_url = "" # fill this with the url of the medium feed you want

# Replace the placeholder with your actual Discord webhook URL
discord_webhook_url = "" # fill this with the url of the discord webhook

# Full file path for the processed_posts.txt file
processed_posts_file = r"" # fill this with the path of the processed_posts file

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn") # change model if you want to

def extract_text_from_html(html_content):
    # Parse HTML and extract text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def check_for_new_posts():
    # Parse the Medium RSS feed
    feed = feedparser.parse(medium_rss_url)

    # Check if there are entries in the feed
    if len(feed.entries) > 0:

        # Get the latest post
        latest_post = feed.entries[0]

        # Check if the post title is not already processed
        if not is_post_processed(latest_post.title):

            # Create a summary
            html_content = latest_post.content[0]['value']
            text_content = extract_text_from_html(html_content)

            # Generate summary using the AI model
            summary = generate_summary(text_content)

            # Send a Discord notification
            send_discord_notification(latest_post.title, latest_post.link, summary)
            mark_post_as_processed(latest_post.title)

        else:
            # Print if there's no new post
            print("No new posts.")
    else:
        # Print if entries not found
        print("No entries in the feed.")

def send_discord_notification(title, link, summary):

    # Create a Discord webhook
    webhook = DiscordWebhook(url=discord_webhook_url, content=f"New Medium post: {title}\n{link}\n\nSummary: {summary}")

    # Execute the webhook
    webhook.execute()

def is_post_processed(post_title):

    # Check if the post title is in the list of processed posts
    processed_posts = get_processed_posts()
    return post_title in processed_posts

def mark_post_as_processed(post_title):

    # Add the post title to the list of processed posts
    processed_posts = get_processed_posts()
    processed_posts.append(post_title)
    
    # Save the updated list to the file
    with open(processed_posts_file, "a") as file:
        file.write(post_title + "\n")

def get_processed_posts():

    # Read the list of processed posts from the file
    if os.path.exists(processed_posts_file):
        with open(processed_posts_file, "r") as file:
            return [line.strip() for line in file.readlines()]
    else:
        return []

def generate_summary(text):

    # Generate a summary
    return summarizer(text, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)[0]['summary_text']

if __name__ == "__main__":
    check_for_new_posts()
