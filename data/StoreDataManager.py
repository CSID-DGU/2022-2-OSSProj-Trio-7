import json
import os

from object.Character import Character


# 캐릭터 데이터 json 파일 읽기/쓰기 클래스
class StoreDataManager:
    # 캐릭터 데이터 json 파일 업데이트
    # default=Character.json_dumpt_obj로 설정함으로 필요한 속성값만 포함시켜 serialize
    def save(characters):
        char_dict = {"Characters":characters}
        json_str = json.dumps(char_dict,indent=4,default=Character.json_dump_obj) # 사전형 데이터를 json데이터로 담을 수 있는 메서드
        json_file = open("./data/storedata.json", "w") # 쓰기 모드로 json파일을 연다.
        json_file.write(json_str)
        json_file.close()

    # json 파일 읽어와 캐릭터 클래스 객체로 deserialize
    def load(char_info):
        if(os.path.isfile("./data/storedata.json")):
            try:
                characters = []
                with open("./data/storedata.json", "r") as json_file:
                    data = json.loads(json_file.read())
                    if char_info=="fire":
                        for i in data["fire"]:
                            characters.append(Character(**i))
                        json_file.close()
                        return characters

                    if char_info == "police":
                        for i in data["police"]:
                            print("캐릭터 : ",i)
                            characters.append(Character(**i))
                        json_file.close()
                        return characters

                    if char_info =="doctor":
                        for i in data["doctor"]:
                            characters.append(Character(**i))
                        json_file.close()
                        return characters
                    
            except:
                print("파일 불러오는 중 에러가 발생했습니다.")
        else:
            print("불러올 데이터가 없습니다.")