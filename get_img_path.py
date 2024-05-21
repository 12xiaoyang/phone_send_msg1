import os
import json
import logging
from get_name import GetAllImageDate
from load_config import load_config_file

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    config = load_config_file('config.json')
    SET_YEAR = config["SCHEDULE_TIME"]["SET_YEAR"]
    SET_MONTH = config["SCHEDULE_TIME"]["SET_MONTH"]
    SET_DAY = config["SCHEDULE_TIME"]["SET_DAY"]
    SET_HOUR = config["SCHEDULE_TIME"]["SET_HOUR"]
except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
    logging.error(f"Error loading configuration: {e}")
    SET_YEAR = SET_MONTH = SET_DAY = SET_HOUR = None


def filter_image_paths(folder_path, filter_func):
    try:
        results = GetAllImageDate(folder_path)
        return [list(result.keys())[0] for result in results if filter_func(result)]
    except Exception as e:
        logging.error(f"Error filtering image paths: {e}")
        return []


# 示例过滤函数：过滤文件大小大于1MB的图片
def size_filter(path):
    try:
        return os.path.getsize(path) > 1 * 1024 * 1024
    except Exception as e:
        logging.error(f"Error in size_filter: {e}")
        return False


def time_filter(image_data):
    try:
        if not image_data:
            return False

        values = list(image_data.values())[0]
        key = list(image_data.keys())[0]

        if int(values["year"]) > SET_YEAR:
            return key
        elif int(values["year"]) == SET_YEAR:
            if int(values["month"]) > SET_MONTH:
                return key
            elif int(values["month"]) == SET_MONTH:
                if int(values["day"]) > SET_DAY:
                    return key
                elif int(values["day"]) == SET_DAY:
                    if int(values["hour"]) >= SET_HOUR:
                        return key
        return False
    except Exception as e:
        logging.error(f"Error in time_filter: {e}")
        return False


# 返回文件夹中所有符合规定的图片
def filter_image(folder_path, filter_func=True):
    img_paths = []
    if filter_func:
        img_path_filters = filter_image_paths(folder_path, filter_func=time_filter)
    else:
        img_path_filters = os.listdir(folder_path)

    for img_path_filter in img_path_filters:
        if os.name == 'nt':  # Windows
            img_paths.append(f"{folder_path}\\{img_path_filter}")
        else:  # Unix/Linux
            img_paths.append(f"{folder_path}/{img_path_filter}")

    return img_paths
