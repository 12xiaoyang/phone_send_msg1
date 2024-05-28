"""
主程序用来发送电脑发送图片
"""
import time

from Utils import Utils
from Configuration import ConfigManager
from EmailSender import EmailSender
import logging


def main():
    # 清除logging的hander
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    modify_config = input("是否需要修改配置文件 如果需要请输入yes 否则任意键退出 .....\n")
    if modify_config == "yes":
        ConfigManager.initialize_config(ConfigManager())
    config = Utils.load_config_file("config.json")
    Utils.setup_logging(config)
    image_folder = config["Folder_Path"]
    emailSender = EmailSender()
    while True:
        emailSender.daily_report_job(image_folder)
        time.sleep(60)


if __name__ == "__main__":
    main()

# /storage/emulated/0/Pictures/Screenshots/
