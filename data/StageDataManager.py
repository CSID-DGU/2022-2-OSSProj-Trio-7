import json
from collections import OrderedDict

from data.Stage import Stage


class StageDataManager:

    @staticmethod
    def loadStageData():
        with open('./data/stagedata.json') as f:
            stageData = json.load(f,object_pairs_hook=OrderedDict)
        return stageData

    
    @staticmethod
    def unlockNextStage(stage):
        with open('./data/stagedata.json', 'r') as f:
            json_data = json.load(f,object_pairs_hook=OrderedDict)

        try: #unlock next stage of passed stage from parameter
            #make next stage's "is_unlocked" field 1
            json_data["chapter"][stage.chapter][str(list(json_data["chapter"][stage.chapter].keys()).index(f"{stage.stage}")+2)][6] = 1
        except:
            pass
            
        with open('./data/stagedata.json', 'w', encoding='utf-8') as make_file:
            json.dump(json_data, make_file, indent="\t")
