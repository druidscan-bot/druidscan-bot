import praw
import os
import sys
from database import Database
from hearthstone_circlejerk_subreddit_processor import HearthstoneCirclejerkSubredditProcessor
from druidscanbot_subreddit_processor import DruidscanbotSubredditProcessor
from post_generator import PostGenerator

database = Database('posts_replied_to.txt')
hearthstoneCirclejerkSubredditProcessor = HearthstoneCirclejerkSubredditProcessor()
druidscanbotSubredditProcessor = DruidscanbotSubredditProcessor()
postGenerator = PostGenerator()

# Mode to run the bot in.
# 'Run' runs the bot, and will repeat until mode becomes something other than 'Run'
# 'DryRun' does a dry run, which doesn't actually post anything to reddit but shows in the console what would happen.
# 'None' does nothing.
def getMode():
    modeFileName = 'mode.txt'
    if not os.path.isfile(modeFileName):
        return 'None'
    with open('mode.txt', 'r') as f:
        modeText = f.read()
        if modeText == 'DryRun':
            return 'DryRun'
        if modeText == 'Run':
            return 'Run'
        return 'None'
        
while True:
    mode = getMode()
    if mode == 'None':
        sys.exit(0)

    reddit = praw.Reddit('bot1')
    herbjerkSubreddit = reddit.subreddit('HearthstoneCircleJerk')
    druidscanbotSubreddit = reddit.subreddit('DruidscanBot')

    commentsWithBracketedTexts = hearthstoneCirclejerkSubredditProcessor.process(herbjerkSubreddit)
    imagePosts = druidscanbotSubredditProcessor.process(druidscanbotSubreddit)

    commentsToReplyTo = [x for x in commentsWithBracketedTexts if x.post.id not in database.postsRepliedTo()]

    try:
        for comment in commentsToReplyTo:
            postText = postGenerator.generate_post_text(comment, imagePosts)
            if mode == 'Run':
                comment.post.reply(postText)
                database.add_post_id_to_replied(comment.post.id)
            else:
                print(f'Responding to post {comment.post.id} with text:')
                print(f'{postText}')
    except:
        pass
    finally:
        database.save()
        if mode == 'DryRun':
            sys.exit(0)
