import glob
import json

# data를 json 파일로 저장
def save_json(username, filename, now, data):
    num = len(glob.glob(f'logs/{username}_*.json')) + 1
    file_path = 'logs/' + filename + '_' + now + '_' + f'{num:04d}' + '.json'

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# username에 대한 log 중 가장 최근 json 파일을 읽어서 data로 반환
def load_json(username):
    file_list = glob.glob(f'logs/{username}_*.json')
    file_list.sort()
    file_paths = file_list[-2:]

    if len(file_paths) < 2:
        return None, None
    else:
        with open(file_paths[0], 'r', encoding='utf-8') as file:
            pre_data = json.load(file)
            file.close()

        with open(file_paths[1], 'r', encoding='utf-8') as file:
            last_data = json.load(file)
            file.close()
            
        return pre_data, last_data
