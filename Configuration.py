import os
import json
import logging


class ConfigManager:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.config = self.load_existing_config()

    def load_existing_config(self):
        """
        加载现有的配置文件（如果存在）。
        """
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def initialize_config(self):
        """
        初始化配置，创建或覆盖config.json文件。
        """
        existing_config = self.load_existing_config()

        default_config = {
            "Folder_Path": "/storage/emulated/0/Pictures/Screenshots/",
            "DEBUG": {
                "ENABLE_LOGGING": "",
                "LOG_LEVEL": "INFO",
                "LOG_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "LOG_FILE": "app.log"
            },
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

        # 合并默认配置和现有配置
        config = {**default_config, **existing_config}

        # 如果EMAIL_CONFIG中某些字段为空，则从用户输入中获取
        config["EMAIL_CONFIG"]["SMTP_USERNAME"] = input(
            f"填写自己的qq邮箱 (当前: {config['EMAIL_CONFIG']['SMTP_USERNAME']}): ") or config["EMAIL_CONFIG"][
                                                      "SMTP_USERNAME"]
        config["EMAIL_CONFIG"]["FROM_EMAIL"] = input(
            f"填写您自己的qq邮箱 (当前: {config['EMAIL_CONFIG']['FROM_EMAIL']}): ") or config["EMAIL_CONFIG"]["FROM_EMAIL"]
        config["EMAIL_CONFIG"]["TO_EMAIL"] = input(
            f"选择要发送的给哪个邮箱 (当前: {config['EMAIL_CONFIG']['TO_EMAIL']}): ") or config["EMAIL_CONFIG"]["TO_EMAIL"]
        config["EMAIL_CONFIG"]["SMTP_PASSWORD"] = input(
            f"输入你的qq邮箱授权密钥 (当前: {config['EMAIL_CONFIG']['SMTP_PASSWORD']}): ") or config["EMAIL_CONFIG"][
                                                      "SMTP_PASSWORD"]

        # 输入图片筛选时间
        times = self.get_user_schedule_time(config["SCHEDULE_TIME"])
        config["SCHEDULE_TIME"]["SET_YEAR"] = times["SET_YEAR"]
        config["SCHEDULE_TIME"]["SET_MONTH"] = times["SET_MONTH"]
        config["SCHEDULE_TIME"]["SET_DAY"] = times["SET_DAY"]
        config["SCHEDULE_TIME"]["SET_HOUR"] = times["SET_HOUR"]

        debug = self.set_out_information(self.config["DEBUG"])
        self.config["DEBUG"]["ENABLE_LOGGING"] = debug["ENABLE_LOGGING"]
        self.config["DEBUG"]["LOG_LEVEL"] = debug["LOG_LEVEL"]


        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
                logging.info("Created and updated config file: config.json")
        except Exception as e:
            logging.error(f"Failed to update config file: {e}")

        return config

    def set_out_information(self, debug):
        ENABLE_LOGGING = input(f"是否开启日志模式 true 开启  false 开启(当前: {debug['ENABLE_LOGGING']}): ") or debug[
            'ENABLE_LOGGING']  # 启用日志记录
        LOG_LEVEL = input(f"日志信息模式 (当前: {debug['LOG_LEVEL']}): ") or debug[
            'LOG_LEVEL']  # 日志级别
        # 默认开启日志信息状态
        if ENABLE_LOGGING == "false":
            ENABLE_LOGGING = False
        else:
            ENABLE_LOGGING = True
        return {
            "ENABLE_LOGGING": bool(ENABLE_LOGGING),
            "LOG_LEVEL": LOG_LEVEL
        }
    def get_user_schedule_time(self, existing_schedule_time):
        """
        从用户输入中获取调度时间，如果用户不输入，则保留现有时间。
        """
        year = input(f"Enter the year (当前: {existing_schedule_time['SET_YEAR']}): ") or existing_schedule_time['SET_YEAR']
        month = input(f"Enter the month (当前: {existing_schedule_time['SET_MONTH']}): ") or existing_schedule_time[
            'SET_MONTH']
        day = input(f"Enter the day (当前: {existing_schedule_time['SET_DAY']}): ") or existing_schedule_time['SET_DAY']
        hour = input(f"Enter the hour (当前: {existing_schedule_time['SET_HOUR']}): ") or existing_schedule_time['SET_HOUR']

        return {
            "SET_YEAR": int(year),
            "SET_MONTH": int(month),
            "SET_DAY": int(day),
            "SET_HOUR": int(hour)
        }


