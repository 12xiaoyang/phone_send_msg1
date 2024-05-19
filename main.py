"""
主程序用来发送电脑发送图片
"""

import json
import schedule
from send_img_phone import daily_report_job1

# 读取配置文件
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

folder_path = config["Folder_Path"]

# 定义定时任务
schedule.every(1).minutes.do(daily_report_job1, folder_path)


# 运行定时任务
def run_scheduled_tasks():
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    run_scheduled_tasks()
