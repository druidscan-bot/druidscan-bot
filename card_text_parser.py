import json
import urllib.request
import re
from functools import reduce

def turnRowToString(row):
    #please don't shoot me
    return json.dumps(row)\
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
        .replace("\\u00a0", " ")\
        .replace("\\u2019", "'")\
        .replace("\\n", " ")

request = urllib.request.Request("https://api.hearthstonejson.com/v1/28855/enUS/cards.collectible.json", headers={'Accept': 'text/html', 'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(request) as response:
    content = response.read()

jsonContent = json.loads(content)
descriptions = map(lambda x: x["text"], filter(lambda x: "text" in x, jsonContent))
descriptionsText = reduce(lambda x,y: x + "\n" + turnRowToString(y), descriptions, "")[1:]

f = open("descriptions.txt", "w")
f.write(descriptionsText)
