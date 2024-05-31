import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ssl
import logging
import os
import zipfile
from Utils import Utils
from Configuration import ConfigManager
from ImagePathFilter import ImagePathFilter


class EmailSender:
    def __init__(self, config_path="config.json"):
        self.config = Utils.load_config_file(config_path)
        self.done_img = []

        # 配置SMTP服务器
        self.SMTP_SERVER = self.config["EMAIL_CONFIG"]["SMTP_SERVER"]
        self.SMTP_PORT = self.config["EMAIL_CONFIG"]["SMTP_PORT"]
        self.SMTP_USERNAME = self.config["EMAIL_CONFIG"]["SMTP_USERNAME"]
        self.SMTP_PASSWORD = self.config["EMAIL_CONFIG"]["SMTP_PASSWORD"]  # 使用应用专用密码

        # 配置邮件信息
        self.FROM_EMAIL = self.config["EMAIL_CONFIG"]["FROM_EMAIL"]
        self.TO_EMAIL = self.config["EMAIL_CONFIG"]["TO_EMAIL"]  # QQ邮箱地址
        self.SUBJECT = self.config["EMAIL_CONFIG"]["SUBJECT"]

        # 设置日志
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def send_email(self, report_content, zip_path):
        """
        发送包含文本和压缩文件附件的邮件
        """
        logging.info("准备发送邮件，附件: %s", zip_path)

        msg = MIMEMultipart()
        msg['From'] = self.FROM_EMAIL
        msg['To'] = self.TO_EMAIL
        msg['Subject'] = self.SUBJECT

        # 附加邮件正文
        msg.attach(MIMEText(report_content, 'plain', 'utf-8'))

        # 添加压缩文件附件
        try:
            with open(zip_path, 'rb') as zip_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(zip_file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(zip_path))
                msg.attach(part)
                logging.info("附件添加成功: %s", zip_path)
        except FileNotFoundError:
            logging.error("压缩文件未找到: %s", zip_path)
            return

        # 连接到SMTP服务器并发送邮件
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT, context=context) as server:
                server.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)
                server.sendmail(self.FROM_EMAIL, self.TO_EMAIL, msg.as_string())
                logging.info("邮件发送成功")
        except smtplib.SMTPException as e:
            logging.error("发送邮件失败: %s", e)

    def daily_report_job(self, folder_path):
        """
        执行每日报告任务，发送包含新图片的邮件
        """
        # 读取报告内容（假设报告内容存储在一个文件中）
        try:
            with open('daily_report.txt', 'r', encoding='utf-8') as file:
                report_content = file.read()
            logging.info("日报内容读取成功")
        except FileNotFoundError:
            logging.error("日报文件未找到")
            return

        # 获取图片路径列表
        try:
            image_filter = ImagePathFilter()
            image_paths = image_filter.filter_image(folder_path)
            logging.info("找到 %d 张图片", len(image_paths))
        except Exception as e:
            logging.error("获取图片路径失败: %s", e)
            return

        # 去除重复的图片路径
        try:
            remaining_img = Utils.remove_duplicates(image_paths, self.done_img)
            self.done_img = remaining_img + self.done_img
            if remaining_img:  # 有新的图片才会进行发送
                logging.info("当前有 %d 新的图片将会被发送", len(remaining_img))

                # 压缩图片文件夹
                zip_path = 'images.zip'
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for img in remaining_img:
                        zipf.write(img, os.path.basename(img))
                logging.info("图片文件夹压缩成功: %s", zip_path)

                self.send_email(report_content, zip_path)
                logging.info("成功发送")
                print("zip was sent successfully ok!")
            else:
                logging.info("当前没有新的图片需要发送")
        except Exception as e:
            logging.error("处理图片时出错: %s", e)