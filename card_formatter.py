class CardFormatter:
    def format_card(self, card, imageUrl, postUrl, expansion):
        description = self.__clean_description(card.description)
        race = f' {card.race} ' if card.race else ' '
        attack = card.attack if card.cardType != 'Spell' else '-'
        return f"* **[{card.name}]({imageUrl})** ([Thread]({postUrl})) **{card.playerClass} | {card.cardType} | {card.rarity} | {expansion}**\n\n {card.manaCost}/{attack}/{card.health or card.durability or '-'}{race}| {description}\n\n"
    def __clean_description(self, description):
        return description\
        .replace("\"", "")\
        .replace("$", "")\
        .replace("#", "")\
        .replace("[x]", "")\
        .replace("<b>", "")\
        .replace("</b>", "")\
        .replace("<i>", "")\
        .replace("</i>", "")\
        .replace("{0}", "")\
        .replace("{1}", "")\
        .replace("_", " ")\
        .replace("\\u00a0", " ")\
        .replace("\\u2019", "'")\
        .replace("\\n", " ")