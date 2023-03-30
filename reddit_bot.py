import os
import praw
import sys
from datetime import datetime, date
from database import Database
from hearthstone_circlejerk_subreddit_processor import HearthstoneCirclejerkSubredditProcessor
from druidscanbot_subreddit_processor import DruidscanbotSubredditProcessor
from post_generator import PostGenerator

dryRun = len(sys.argv) > 1 and sys.argv[1] == '-d'
hearthstoneCirclejerkSubredditProcessor = HearthstoneCirclejerkSubredditProcessor()
druidscanbotSubredditProcessor = DruidscanbotSubredditProcessor()

reddit = praw.Reddit('bot1')
herbjerkSubreddit = reddit.subreddit('HearthstoneCircleJerk')
druidscanbotSubreddit = reddit.subreddit('DruidscanBot')

today = datetime.today()
postGenerator = PostGenerator(today.day == 1 and today.month == 4)
database = Database('posts_replied_to.txt')

while True:
    if (datetime.today() - today).days >= 1:
        today = datetime.today()
        postGenerator = PostGenerator(today.day == 1 and today.month == 4)
        database = Database('posts_replied_to.txt') 
        
    commentsWithBracketedTexts = hearthstoneCirclejerkSubredditProcessor.process(herbjerkSubreddit)
    imagePosts = druidscanbotSubredditProcessor.process(druidscanbotSubreddit)

    commentsToReplyTo = [x for x in commentsWithBracketedTexts if x.post.id not in database.postsRepliedTo()]

    try:
        for comment in commentsToReplyTo:
            postText = postGenerator.generate_post_text(comment, imagePosts)
            if dryRun:
                print(f'Responding to post {comment.post.id} with text:')
                print(f'{postText}')
            else:
                comment.post.reply(postText)
                database.add_post_id_to_replied(comment.post.id)
    except:
        pass
    finally:
        database.save()
