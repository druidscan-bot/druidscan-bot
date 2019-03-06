import praw
import os
import sys
from database import Database
from hearthstone_circlejerk_subreddit_processor import HearthstoneCirclejerkSubredditProcessor
from druidscanbot_subreddit_processor import DruidscanbotSubredditProcessor
from post_generator import PostGenerator

dryRun = len(sys.argv) > 1 and sys.argv[1] == '-d'
hearthstoneCirclejerkSubredditProcessor = HearthstoneCirclejerkSubredditProcessor()
druidscanbotSubredditProcessor = DruidscanbotSubredditProcessor()
postGenerator = PostGenerator()

reddit = praw.Reddit('bot1')
herbjerkSubreddit = reddit.subreddit('HearthstoneCircleJerk')
druidscanbotSubreddit = reddit.subreddit('DruidscanBot')

commentsWithBracketedTexts = hearthstoneCirclejerkSubredditProcessor.process(herbjerkSubreddit)
imagePosts = druidscanbotSubredditProcessor.process(druidscanbotSubreddit)

database = Database('posts_replied_to.txt')

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
