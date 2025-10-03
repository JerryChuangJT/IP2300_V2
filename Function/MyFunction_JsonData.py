import os
import json

### Funciton for loading json datas.
def Get_jsonAllData(file_path:str)->dict:
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

### Function for Get Key Values From Dict Data.
def Get_DictKey(dict_value:dict)->list:
    list_DictKey = list(dict_value.keys())
    return list_DictKey

### Function for Get Value Values From Dict Data.
def Get_DictValue(dict_value:dict)->list:
    list_DictValue = list(dict_value.values())
    return list_DictValue

def Create_JsonFile(file_path:str):
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump({}, file, ensure_ascii=False, indent=4)

### Function for Update JSON File Data.
def Update_jsonFileData(file_path:str, key_value:str, value):
    ### Create Json File.
    Create_JsonFile(file_path)
            
    ### Read JSON File.
    data = Get_jsonAllData(file_path)

    ### Modify JSON File Data.
    data[key_value] = value

    ### Rewrite New Data into JSON File.
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def Remove_jsonFileKey(file_path:str, key_value:str):
    ### Read JSON File.
    data = Get_jsonAllData(file_path)

    ### Remove Key from JSON File Data.
    if key_value in data:
        del data[key_value]

    ### Rewrite New Data into JSON File.
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
