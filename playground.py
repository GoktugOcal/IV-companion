import os
import json

print([
        {
            "label" : item + " | saved at: " + json.load(open(os.path.join(os.path.abspath("."),"games",item,"game.json")))["latest_save_time"],
            "value": os.path.join(os.path.abspath("."),"games",item,"game.json")
        }
        for item in os.listdir("./games/") if os.path.isdir(os.path.join(os.path.abspath("."),"games",item))
        ])


# for item in os.listdir("./games"):
#     print(item)
#     if os.path.isdir(os.path.join("./games", item)):
#         print("\t", item)