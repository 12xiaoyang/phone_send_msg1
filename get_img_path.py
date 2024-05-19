"""
用于处理图像路径过滤的模块

"""
import os
import glob
from get_name import GetAllImageDate
import json

# 读取配置文件
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

SET_YEAR = config["SCHEDULE_TIME"]["SET_YEAR"]
SET_MONTH = config["SCHEDULE_TIME"]["SET_MONTH"]
SET_DAY = config["SCHEDULE_TIME"]["SET_DAY"]
SET_HOUR = config["SCHEDULE_TIME"]["SET_HOUR"]


def filter_image_paths(folder_path, filter_func):
    # 应用过滤函数来过滤指定图片
    results = GetAllImageDate(folder_path)
    return [list(result.keys())[0] for result in results if filter_func(result)]


# 示例过滤函数：过滤文件大小大于1MB的图片
def size_filter(path):
    return os.path.getsize(path) > 1 * 1024 * 1024


def time_fileter(dict):
    if dict:
        values = list(dict.values())[0];
        key = list(dict.keys())[0];
    else:
        return 0
        # 年份比较
    if int(values["year"]) > SET_YEAR:
        return key
    elif int(values["year"]) == SET_YEAR:
        # 月份比较
        if int(values["month"]) > SET_MONTH:
            return key
        elif int(values["month"]) == SET_MONTH:
            # 日期比较
            if int(values["day"]) > SET_DAY:
                return key
            elif int(values["day"]) == SET_DAY:
                # 小时比较
                if int(values["hour"]) >= SET_HOUR:
                    return key
                else:
                    return 0
            else:
                return 0
        else:
            return 0
    else:
        return 0

    return 0


# 返回文件里面所有符合规定的图片
def filter_image(folder_path, filter_func=True):  # 默认开启过滤检测
    img_paths = []
    if filter_func:  # 如果开启过滤检测
        img_path_filters = filter_image_paths(folder_path, filter_func=time_fileter)
    # 获取到符合要求的图片的名称
    for img_path_filter in img_path_filters:
        img_paths.append(f"{folder_path}/{img_path_filter}")

    return img_paths
