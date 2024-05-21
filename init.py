import os
import json
import logging

def initialize_config():
    """
    初始化配置，创建或覆盖config.json文件。
    """
    default_config = {
        "Folder_Path": "/storage/emulated/0/Pictures/Screenshots/",
        "EMAIL_CONFIG": {
            "SMTP_SERVER": "smtp.qq.com",
            "SMTP_PORT": 465,
            "SMTP_USERNAME": "",
            "SMTP_PASSWORD": "",
            "FROM_EMAIL": "",
            "TO_EMAIL": "",
            "SUBJECT": "Daily Report"
        },
        "SCHEDULE_TIME": {
            "SET_YEAR": "",
            "SET_MONTH": "",
            "SET_DAY": "",
            "SET_HOUR": ""
        }
    }

    # 始终重新创建config.json文件
    config = default_config

    # 如果EMAIL_CONFIG中某些字段为空，则从用户输入中获取
    config["EMAIL_CONFIG"]["SMTP_USERNAME"] = input("填写自己的qq邮箱: ")
    config["EMAIL_CONFIG"]["FROM_EMAIL"] = input("填写您自己的qq邮箱: ")
    config["EMAIL_CONFIG"]["TO_EMAIL"] = input("选择要发送的给哪个邮箱: ")
    config["EMAIL_CONFIG"]["SMTP_PASSWORD"] = input("输入你的qq邮箱授权密钥: ")



    # 输入图片筛选时间
    times = get_user_schedule_time()
    config["SCHEDULE_TIME"]["SET_YEAR"] = times["SET_YEAR"]
    config["SCHEDULE_TIME"]["SET_MONTH"] = times["SET_MONTH"]
    config["SCHEDULE_TIME"]["SET_DAY"] = times["SET_DAY"]
    config["SCHEDULE_TIME"]["SET_HOUR"] = times["SET_HOUR"]

    # 设置日志格式和级别

    try:
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
            logging.info("Created and updated config file: config.json")
    except Exception as e:
        logging.error(f"Failed to update config file: {e}")

    return config

def get_user_schedule_time():
    """
    从用户输入中获取调度时间。
    """
    year = int(input("Enter the year: "))
    month = int(input("Enter the month: "))
    day = int(input("Enter the day: "))
    hour = int(input("Enter the hour: "))

    return {
        "SET_YEAR": year,
        "SET_MONTH": month,
        "SET_DAY": day,
        "SET_HOUR": hour
    }

