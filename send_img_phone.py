import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import ssl
import json
import logging
import os

from load_config import load_config_file
from get_img_path import filter_image
from get_name import remove_duplicates

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 读取配置文件
config = load_config_file("config.json")
done_img = []

# 配置SMTP服务器
SMTP_SERVER = config["EMAIL_CONFIG"]["SMTP_SERVER"]
SMTP_PORT = config["EMAIL_CONFIG"]["SMTP_PORT"]
SMTP_USERNAME = config["EMAIL_CONFIG"]["SMTP_USERNAME"]
SMTP_PASSWORD = config["EMAIL_CONFIG"]["SMTP_PASSWORD"]  # 使用应用专用密码

# 配置邮件信息
FROM_EMAIL = config["EMAIL_CONFIG"]["FROM_EMAIL"]
TO_EMAIL = config["EMAIL_CONFIG"]["TO_EMAIL"]  # QQ邮箱地址
SUBJECT = config["EMAIL_CONFIG"]["SUBJECT"]


def send_email(report_content, image_paths):
    """
    发送包含文本和图片附件的邮件
    """
    logging.info("准备发送邮件，附件数量: %d", len(image_paths))

    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = SUBJECT

    # 附加邮件正文
    msg.attach(MIMEText(report_content, 'plain', 'utf-8'))

    # 添加图片附件
    for image_path in image_paths:
        try:
            with open(image_path, 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
                msg.attach(img)
                logging.info("附件添加成功: %s", image_path)
        except FileNotFoundError:
            logging.error("图片文件未找到: %s", image_path)
            continue

    # 连接到SMTP服务器并发送邮件
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
            logging.info("邮件发送成功")
    except smtplib.SMTPException as e:
        logging.error("发送邮件失败: %s", e)


def daily_report_job1(folder_path):
    """
    执行每日报告任务，发送包含新图片的邮件
    """
    global done_img

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
        image_paths = filter_image(folder_path)
        logging.info("找到 %d 张图片", len(image_paths))
    except Exception as e:
        logging.error("获取图片路径失败: %s", e)
        return

    # 去除重复的图片路径
    try:
        remaining_img = remove_duplicates(image_paths, done_img)
        done_img = remaining_img + done_img
        if remaining_img:  # 有新的图片才会进行发送
            logging.info("当前有 %d 新的图片将会被发送", len(remaining_img))
            send_email(report_content, remaining_img)
            logging.info("成功发送")
        else:
            logging.info("当前没有新的图片需要发送")
    except Exception as e:
        logging.error("处理图片时出错: %s", e)



