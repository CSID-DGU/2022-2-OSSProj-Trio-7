import json
import os

from object.Character import Character


# 캐릭터 데이터 json 파일 읽기/쓰기 클래스
class CharacterDataManager:
    # 캐릭터 데이터 json 파일 업데이트
    # default=Character.json_dumpt_obj로 설정함으로 필요한 속성값만 포함시켜 serialize
    def save(characters):
        char_dict = {"Characters":characters}
        json_str = json.dumps(char_dict,indent=4,default=Character.json_dump_obj)
        json_file = open("./data/characterdata.json", "w")
        json_file.write(json_str)
        json_file.close()

    # json 파일 읽어와 캐릭터 클래스 객체로 deserialize
    def load():
        if(os.path.isfile("./data/characterdata.json")):
            try:
                characters = []
                with open("./data/characterdata.json", "r") as json_file:
                    data = json.loads(json_file.read())
                    for i in data["Characters"]:
                        characters.append(Character(**i))
                    json_file.close()
                    return characters
            except:
                print("파일 불러오는 중 에러가 발생했습니다.")
        else:
            print("불러올 데이터가 없습니다.")


# pvp캐릭터 데이터 json 파일 읽기/쓰기 클래스
class PvpCharacterDataManager:
    # 캐릭터 데이터 json 파일 업데이트
    # default=Character.json_dumpt_obj로 설정함으로 필요한 속성값만 포함시켜 serialize
    def save(characters):
        char_dict = {"Characters":characters}
        json_str = json.dumps(char_dict,indent=4,default=Character.json_dump_obj)
        json_file = open("./data/characterdata.json", "w")
        json_file.write(json_str)
        json_file.close()

    # json 파일 읽어와 캐릭터 클래스 객체로 deserialize
    def load():
        if(os.path.isfile("./data/characterdata.json")):
            try:
                characters = []
                with open("./data/characterdata.json", "r") as json_file:
                    data = json.loads(json_file.read())
                    for i in data["Characters"]:
                        characters.append(Character(**i))
                    json_file.close()
                    return characters
            except:
                print("파일 불러오는 중 에러가 발생했습니다.")
        else:
            print("불러올 데이터가 없습니다.")