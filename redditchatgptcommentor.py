import praw
import openai
import random
import time

# Your Reddit and OpenAI API credentials
reddit_client_id = "YOUR_REDDIT_CLIENT_ID"
reddit_secret = "YOUR_REDDIT_SECRET"
reddit_username = "YOUR_REDDIT_USERNAME"
reddit_password = "YOUR_REDDIT_PASSWORD"

openai_api_key = "YOUR_OPENAI_API_KEY"

# Initialize PRAW and OpenAI clients
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_secret,
    username=reddit_username,
    password=reddit_password,
    user_agent="rising_posts_commenter"
)

openai.api_key = openai_api_key

# Select subreddits
subreddit_list = ["subreddit1", "subreddit2", "subreddit3"]

def generate_comment(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Limit the number of comments left daily to 50
max_comments_per_day = 50
comments_left = 0

# Randomize the time between comments (between 5 minutes and 4 hours)
min_time_between_comments = 5 * 60  # 5 minutes in seconds
max_time_between_comments = 4 * 60 * 60  # 4 hours in seconds

while comments_left < max_comments_per_day:
    # Find rising posts in the selected subreddits
    rising_posts = []
    for subreddit_name in subreddit_list:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.rising(limit=10):
            rising_posts.append(submission)

    # Randomly select a rising post
    selected_post = random.choice(rising_posts)

    # Generate relevant top-level comment based on the article written by ChatGPT
    prompt = f"Create a relevant and informative comment for the following Reddit post: {selected_post.title} {selected_post.url}"
    generated_comment = generate_comment(prompt)

    # Leave the comment on the selected post
    selected_post.reply(generated_comment)
    comments_left += 1

    print(f"Commented on post: {selected_post.title}")

    # Wait for a random time between comments
    sleep_time = random.uniform(min_time_between_comments, max_time_between_comments)
    time.sleep(sleep_time)
