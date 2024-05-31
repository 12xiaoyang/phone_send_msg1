import logging
from Utils import Utils
from Configuration import ConfigManager
from EmailSender import EmailSender


def main():
    # 清除logging的handler
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    modify_config = input("是否需要修改配置文件 如果需要请输入yes 否则任意键退出 .....\n")
    if modify_config.lower() == "yes":
        ConfigManager.initialize_config(ConfigManager())

    config = Utils.load_config_file("config.json")
    Utils.setup_logging(config)
    image_folder = config["Folder_Path"]
    emailSender = EmailSender()

    while True:
        send_email = input("是否发送邮件？输入yes发送,输入其他键跳过本次发送：\n")
        if send_email.lower() == "yes":
            emailSender.daily_report_job(image_folder)


if __name__ == "__main__":
    main()
