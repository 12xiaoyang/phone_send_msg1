"""
处理图片路径的
"""
import re
import glob
import os


def extract_filename(path):
    # 匹配文件名和扩展名
    pattern = r'([^\\/:*?"<>|\r\n]+)\.(jpg|jpeg|png|gif)$'

    match = re.search(pattern, path, re.IGNORECASE)
    if match:
        filename = match.group(1)  # 提取文件名部分
        full_name = f"{filename + '.'}{match.group(2)}"  # 构建完整的文件路径（包括后缀）
        return full_name
    return None


def extract_datetime_info(text):
    # 正则表达式模式
    pattern = r'_([0-9]{4})-([0-9]{2})-([0-9]{2})-([0-9]{2})-([0-9]{2})-([0-9]{2})'

    match = re.search(pattern, text)
    if match:
        return {text: {
            'year': match.group(1),
            'month': match.group(2),
            'day': match.group(3),
            'hour': match.group(4),
            'minute': match.group(5),
            'second': match.group(6)
        }}
    return None


def get_All_image_paths(folder_path, extensions=('*.jpg', '*.jpeg', '*.png', '*.gif', '*html')):
    image_paths = []

    # 遍历所有指定扩展名的图片文件
    for ext in extensions:
        image_paths.extend(glob.glob(os.path.join(folder_path, ext)))
    return image_paths


def remove_duplicates(arr1, arr2):
    # 找出 arr1 中不在 arr2 中的元素
    unique_arr1 = [x for x in arr1 if x not in arr2]
    # 找出 arr2 中不在 arr1 中的元素
    unique_arr2 = [x for x in arr2 if x not in arr1]
    # 合并两个结果
    return unique_arr1 + unique_arr2


# 返回所有图片的年月日
def GetAllImageDate(folder_path):
    result = []
    image_paths = get_All_image_paths(folder_path)
    for image_path in image_paths:
        image_name = extract_filename(image_path)
        info = extract_datetime_info(image_name)
        result.append(info)
    return result
