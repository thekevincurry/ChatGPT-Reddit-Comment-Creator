import praw
import time

# Replace the following variables with your own credentials
client_id = "your_client_id"
client_secret = "your_client_secret"
user_agent = "your_user_agent"
username = "your_username"
password = "your_password"

# Threshold for the minimum number of comments in r/conservative to be considered a frequenter
frequenter_threshold = 10

def main():
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        username=username,
        password=password,
    )

    politics_sub = reddit.subreddit("politics")
    conservative_sub = reddit.subreddit("conservative")

    while True:
        rising_posts = politics_sub.rising(limit=10)
        for post in rising_posts:
            print(f"Monitoring comments on post: {post.title}")
            post.comment_sort = "new"
            post.comments.replace_more(limit=None)
            for comment in post.comments.list():
                user = comment.author
                if user:
                    user_comments = list(user.comments.new(limit=100))
                    conservative_comments = [c for c in user_comments if c.subreddit == conservative_sub]

                    if len(conservative_comments) >= frequenter_threshold:
                        print(f"User '{user}' frequently posts in r/conservative. Comment: {comment.body}")

        time.sleep(300)  # Wait 5 minutes before checking again

if __name__ == "__main__":
    main()
