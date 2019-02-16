import json
import urllib2
import re
from functools import reduce

def turnRowToString(row):
    #please don't shoot me
    return json.dumps(row).replace("\"", "").replace("$", "").replace("#", "").replace("[x]", "").replace("\u00a0", " ").replace("\\n", " ")

request = urllib2.Request("https://api.hearthstonejson.com/v1/28855/enUS/cards.collectible.json", headers={'Accept': 'text/html', 'User-Agent': 'Mozilla/5.0'})
content = urllib2.urlopen(request).read()

jsonContent = json.loads(content)
descriptions = map(lambda x: x["text"], filter(lambda x: "text" in x, jsonContent))
descriptionsText = reduce(lambda x,y: x + "\n" + turnRowToString(y), descriptions, "")

f = open("descriptions.txt", "w")
f.write(descriptionsText)
