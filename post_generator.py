import random
import string
from description_generator import DescriptionGenerator

class PostGenerator:
    def __init__(self):
        self.__descriptionGenerator = DescriptionGenerator()
        self.__classes = ['Neutral', 'Druid', 'Hunter', 'Mage', 
                        'Paladin', 'Priest', 'Rogue', 'Shaman', 'Warlock', 'Warrior']
        self.__types = ['Minion', 'Spell', 'Weapon']
        self.__rarities = ['Common', 'Rare', 'Epic', 'Legendary']
        self.__manaCosts = range(11)
        self.__attackValues = range(13)
        self.__healthValues = range(1, 13)
        self.__types = ['', 'Beast', 'Demon', 'Dragon',
                        'Elemental', 'Mech', 'Murloc', 'Pirate', 'Totem', 'All']
                        
    def generate_post_text(self, CommentWithBracketedTexts, imagePosts):
        postText = ''
        for bracketedText in CommentWithBracketedTexts.bracketedTexts:
            imagePost = random.choice(imagePosts)
            postText += self.__generate_post_description(bracketedText, imagePost.url, imagePost.permalink)
        postText += '[About](https://www.reddit.com/r/DruidscanBot/comments/9u0e36/how_this_works/)&nbsp;&nbsp;[Code for nerds](https://github.com/druidscan-bot/druidscan-bot)'
        return postText

    def __generate_post_description(self, name, imageUrl, postUrl):
        name = name if name != '' else '_'
        selectedClass = random.choice(self.__classes)
        cardType = random.choice(self.__types)
        rarity = random.choice(self.__rarities)
        expansion = ''.join(random.choice(string.ascii_lowercase) for _ in range(3)).upper()
        manaCost = random.choice(self.__manaCosts)
        attack = random.choice(self.__attackValues) if cardType != 'Spell' else '-'
        health = random.choice(self.__healthValues) if cardType != 'Spell' else '-'
        minionType = random.choice(self.__types) + ' ' if cardType == 'Minion' else ''
        description = self.__descriptionGenerator.generate_description(2)
        return f'* **[{name}]({imageUrl})** ([Thread]({postUrl})) **{selectedClass} | {cardType} | {rarity} | {expansion}**\n\n {manaCost}/{attack}/{health} {minionType}| {description}\n\n'
