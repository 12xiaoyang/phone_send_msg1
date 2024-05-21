# 加载配置文件
from init import initialize_config
import json
import logging

modify_config = input("是否需要修改配置文件 如果需要请输入yes 否则任意键退出.....\n")
if modify_config == "yes":
    initialize_config()


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
