from urllib.request import urlopen
import json
import pprint

response = urlopen("https://www.purdue.edu/drsfacilityusage/api/CurrentActivity")
data = json.loads(response.read().decode("utf-8"))

pprint.PrettyPrinter(indent=4).pprint(data)
