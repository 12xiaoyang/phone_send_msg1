import json
import logging
import re
import glob
import os


class Utils:
    @staticmethod
    def load_config_file(file_path):
        """
        加载配置文件
        """

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except Exception as e:
            logging.error(f"配置文件加载失败: {e}")
            return None
    @staticmethod
    def extract_filename(path):
        # 匹配文件名和扩展名
        pattern = r'([^\\/:*?"<>|\r\n]+)\.(jpg|jpeg|png|gif)$'

        match = re.search(pattern, path, re.IGNORECASE)
        if match:
            filename = match.group(1)  # 提取文件名部分
            full_name = f"{filename + '.'}{match.group(2)}"  # 构建完整的文件路径（包括后缀）
            return full_name
        return None

    @staticmethod
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

    @staticmethod
    def get_all_image_paths(folder_path, extensions=('*.jpg', '*.jpeg', '*.png', '*.gif', '*html')):
        image_paths = []

        # 遍历所有指定扩展名的图片文件
        for ext in extensions:
            image_paths.extend(glob.glob(os.path.join(folder_path, ext)))
        return image_paths

    @staticmethod
    def remove_duplicates(arr1, arr2):
        # 找出 arr1 中不在 arr2 中的元素
        unique_arr1 = [x for x in arr1 if x not in arr2]
        # 找出 arr2 中不在 arr1 中的元素
        unique_arr2 = [x for x in arr2 if x not in arr1]
        # 合并两个结果
        return unique_arr1 + unique_arr2

    @staticmethod
    def get_All_image_paths(folder_path, extensions=('*.jpg', '*.jpeg', '*.png', '*.gif', '*html')):
        image_paths = []

        # 遍历所有指定扩展名的图片文件
        for ext in extensions:
            image_paths.extend(glob.glob(os.path.join(folder_path, ext)))
        return image_paths

    @staticmethod
    def setup_logging(config):
        """
        设置日志配置。

        参数:
        config (dict): 包含日志配置信息的字典。
        """
        if config.get("DEBUG", {}).get("ENABLE_LOGGING", False):
            log_level = getattr(logging, config["DEBUG"].get("LOG_LEVEL", "INFO").upper(), logging.INFO)
            log_format = config["DEBUG"].get("LOG_FORMAT", '%(asctime)s - %(levelname)s - %(message)s')
            # log_file = config["DEBUG"].get("LOG_FILE", None)
            logging.basicConfig(level=log_level, format=log_format)
        else:
            logging.disable(logging.CRITICAL)
    # 返回所有图片的年月日
    @staticmethod
    def GetAllImageDate(folder_path):
        result = []
        image_paths = Utils.get_All_image_paths(folder_path)
        for image_path in image_paths:
            image_name = Utils.extract_filename(image_path)
            info = Utils.extract_datetime_info(image_name)
            result.append(info)
        return result
