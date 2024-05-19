"""
手机端发送程序
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from get_img_path import filter_image
from get_name import remove_duplicates
import ssl
import json

# 读取配置文件
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
done_img = []
# 配置SMTP服务器
SMTP_SERVER = config["EMAIL_CONFIG"]["SMTP_SERVER"]
SMTP_PORT = config["EMAIL_CONFIG"]["SMTP_PORT"]
SMTP_USERNAME = config["EMAIL_CONFIG"]["SMTP_USERNAME"]
SMTP_PASSWORD = config["EMAIL_CONFIG"]["SMTP_PASSWORD"]  # 使用应用专用密码

# print(SMTP_USERNAME)
# 配置邮件信息
FROM_EMAIL = config["EMAIL_CONFIG"]["FROM_EMAIL"]
TO_EMAIL = config["EMAIL_CONFIG"]["TO_EMAIL"]  # QQ邮箱地址
SUBJECT = config["EMAIL_CONFIG"]["SUBJECT"]


def send_email(report_content, image_paths):
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
                img.add_header('Content-Disposition', 'attachment', filename=image_path)
                msg.attach(img)
        except FileNotFoundError:
            print(f"Image file {image_path} not found.")
            continue

    # 连接到SMTP服务器并发送邮件
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            # server.set_debuglevel(1)  # 启用调试输出
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
            # print("Email sent phone successfully.")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")


def daily_report_job1(fold_path):
    global done_img
    # 读取报告内容（这里假设报告内容存储在一个文件中）
    try:
        with open('daily_report.txt', 'r', encoding='utf-8') as file:
            report_content = file.read()
    except FileNotFoundError:
        print("Report file not found.")
        return

    # 图片路径列表
    image_paths = filter_image(fold_path)  # 添加需要附加的图片路径
    remaining_img = remove_duplicates(image_paths, done_img)
    done_img = remaining_img + done_img
    if remaining_img:  # 有新的图片才会进行发送
        print(f"当前有{len(remaining_img)}新的图片将会被发送")
        send_email(report_content, remaining_img)
    else:
        print(f"当前有{len(remaining_img)}新的图片将会被发送")


# daily_report_job1(r"C:\Users\admin1\Pictures\Camera Roll")
