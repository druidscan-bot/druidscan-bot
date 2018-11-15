import praw
import pdb
import re
import os
import random
import string
import time

reddit = praw.Reddit('bot1')


class BracketedText:
    def __init__(self, text, post):
        self.text = text
        self.post = post

    def __eq__(self, other):
        if isinstance(other, BracketedText):
            return self.text == other.text and self.post.id == other.post.id
        return False


class Database:
    filepath = 'posts_replied_to.txt'

    def __init__(self):
        if not os.path.isfile(Database.filepath):
            self.posts_replied_to = []
        else:
            with open(Database.filepath, 'r') as f:
                self.posts_replied_to = list(
                    filter(None, f.read().split('\n')))

    def addPostToReplied(self, post):
        self.posts_replied_to.append(post.id)

    def saveToDatabase(self):
        with open(Database.filepath, 'w') as f:
            for post_id in set(self.posts_replied_to):
                f.write(post_id + '\n')


def uniqueify(seq):
    u = []
    for x in seq:
        if x not in u:
            u.append(x)
    return u


def extractBracketedTextFromSubmission(submission):
    bracketedTexts = []
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        matches = re.findall(
            r'\\?\[\\?\[(.*?)\\?\]\\?\]', comment.body, re.M | re.I)
        for group in matches:
            bracketedTexts.append(BracketedText(group, comment))
    return bracketedTexts


def getBracketedTexts(subreddit):
    resultLimit = 30
    bracketedTexts = []
    for submission in subreddit.new(limit=resultLimit):
        for val in extractBracketedTextFromSubmission(submission):
            bracketedTexts.append(val)
    for submission in subreddit.hot(limit=resultLimit):
        for val in extractBracketedTextFromSubmission(submission):
            bracketedTexts.append(val)
    return uniqueify(bracketedTexts)


possibleClasses = ['Neutral', 'Druid', 'Hunter', 'Mage',
                   'Paladin', 'Priest', 'Rogue', 'Shaman', 'Warlock', 'Warrior']
possibleTypes = ['Minion', 'Spell', 'Weapon']
rarities = ['Common', 'Rare', 'Epic', 'Legendary']
manaCosts = range(11)
attackValues = range(13)
healthValues = range(1, 13)
types = ['', 'Beast', 'Demon', 'Dragon',
         'Elemental', 'Mech', 'Murloc', 'Pirate', 'Totem', 'All']
nonSpellDescriptions = [
    '**Battlecry**: Destroy a random snake.',
    'Overload: (2)',
    'Whenever you cast a spell, gain Armor equal to its cost, gain +1 attack, summon a random 2 cost minion, draw a card, gain +2 attack this turn only, summon a 1/1 Violet Apprentice, draw a minion from your deck, add a \'Fireball\' spell to your hand, put a copy into the other player\'s hand, and add a random Priest spell to your hand.',
    'Whenever you play a card with Overload, buff a random Tunnel Trogg.',
    '**Battlecry**:  Cause a random hearthstone player from a random game to lose.',
    '**Battlecry**:  Discard your hand and deck and dust your entire collection.',
    '**Battlecry**:  Summon a random 7 drop with 2 attack and 1 health.',
    '**Rush**.  **Battlecry**:  Can attack heroes this turn.',
    '**Magnetic**.  **Battlecry**:  Destroy this minion.',
    '**Deathrattle**:  oof ouch owie im dead',
    '**Taunt**.  **Taunt**.  **Taunt**.  **Taunt**.  **Taunt**.']
spellDescriptions = [
    'Deal 5 damage.  Draw 5 cards.  Gain 5 Armor.  Summon a 5/5 Ghoul.',
    'Deal like 9 damage randomly.  Just kinda fuckin\' throw it in there, see what happens.',
    'Call your opponent a nerd.',
    'Summon a bunch of monsters in one turn, even though it\'s against the rules.',
    '**Battlecry**: wait no this is a spell never mind.',
    'Summon 7 1/5 scarabs with **Taunt**.',
    'Give a minion +6/+18.  When it dies, summon 3 stegodons.',
    'Overload: (3)',
    'Summon a Knife Juggler, a Flamewaker, and a Shadowboxer.  Cast Light of the Naaru on your hero, then Implosion on a random enemy minion.',
    'Deal 1-100 damage to a random character in a random game.',
    'Destroy the opponent\'s hero.  If that kills them, draw a card.']


def generateDescription(name, imageUrl, postUrl):
    name = name if name != '' else '_'
    selectedClass = random.choice(possibleClasses)
    cardType = random.choice(possibleTypes)
    rarity = random.choice(rarities)
    expansion = ''.join(random.choice(string.ascii_lowercase)
                        for i in range(3)).upper()
    manaCost = random.choice(manaCosts)
    attack = random.choice(attackValues) if cardType != 'Spell' else '-'
    health = random.choice(healthValues) if cardType != 'Spell' else '-'
    minionType = random.choice(types) if cardType == 'Minion' else ''
    minionType = minionType + ' ' if minionType != '' else ''
    description = random.choice(
        spellDescriptions) if cardType == 'Spell' else random.choice(nonSpellDescriptions)
    return f'* [{name}]({imageUrl}) {selectedClass} {cardType} {rarity} {expansion}\n\n {manaCost}/{attack}/{health} {minionType}| {description}\n\n [Original Post]({postUrl})\n\n'


database = Database()

druidscanbotSubreddit = reddit.subreddit('DruidscanBot')
herbjerkSubreddit = reddit.subreddit('HearthstoneCircleJerk')

bracketedTexts = [x for x in getBracketedTexts(
    herbjerkSubreddit) if x.post.id not in database.posts_replied_to]

if len(bracketedTexts) > 0:
    bracketedTextDictionary = {}
    for bracketedText in bracketedTexts:
        if bracketedText.post.id in bracketedTextDictionary:
            bracketedTextDictionary[bracketedText.post.id].append(
                bracketedText)
        else:
            bracketedTextDictionary[bracketedText.post.id] = [bracketedText]
    imagePosts = [x for x in druidscanbotSubreddit.hot(limit=20) if not re.match(
        r'.*www\.reddit\.com.*', x.url, re.M | re.I)]
    try:
        for postId in bracketedTextDictionary:
            post = bracketedTextDictionary[postId].post
            description = ''
            for bracketedText in bracketedTextDictionary[postId]:
                imagePost = random.choice(imagePosts)
                description += generateDescription(
                    bracketedText.text, imagePost.url, imagePost.permalink)
            description += '[About](https://www.reddit.com/r/DruidscanBot/comments/9u0e36/how_this_works/)&nbsp;&nbsp;[Code for nerds](https://github.com/druidscan-bot/druidscan-bot)'
            post.reply(description)
            database.addPostToReplied(post)
    except:
        pass
    finally:
        database.saveToDatabase()
