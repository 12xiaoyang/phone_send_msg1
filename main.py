"""
主程序用来发送电脑发送图片
"""

import logging
import schedule
from send_img_phone import daily_report_job1
from load_config import load_config_file

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_scheduled_tasks():
    """
    运行定时任务
    """
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    try:
        logging.info("Initializing scheduled tasks...")

        # 读取配置文件
        config = load_config_file("config.json")
        folder_path = config["Folder_Path"]

        # 定义定时任务
        schedule.every(1).minutes.do(daily_report_job1, folder_path)

        # 运行定时任务
        run_scheduled_tasks()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
