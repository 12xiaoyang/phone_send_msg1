from kivy.app import App
from kivy.uix.label import Label
import schedule
import json
import get_img_path
import get_name
import send_img_phone
import time


class MyApp(App):
    def build(self):
        # 此处展示一个简单的 Label，表示应用启动成功
        return Label(text="自动发送图片程序运行中...")

    def on_start(self):
        # 应用启动时，开始调度任务
        schedule.every(1).minutes.do(self.run_daily_report_job)
        self.run_scheduled_tasks()

    def run_daily_report_job(self):
        # 获取 config.json 配置
        with open('config.json', 'r') as f:
            config = json.load(f)

        folder_path = config.get("Folder_Path", r"C:\Users\admin1\Pictures\Saved Pictures")

        # 调用你的主要逻辑
        send_img_phone.daily_report_job1(folder_path)

    def run_scheduled_tasks(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    MyApp().run()
