# smtplib 用于邮件的发信动作
import re
import smtplib
import subprocess
# 构建邮件头
from email.header import Header
from email.mime.multipart import MIMEMultipart
# email 用于构建邮件内容
from email.mime.text import MIMEText

import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'dnt': '1',
    'origin': 'https://ipw.cn',
    'priority': 'u=1, i',
    'referer': 'https://ipw.cn/',
    'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
}


def get_ipv6_from_ipv4(ipv4_address):
    try:
        # 先获取目标主机的 MAC 地址（通过 ARP 表）
        arp_result = subprocess.run(
            ['arp', '-a', ipv4_address],
            capture_output=True,
            text=True
        )
        mac_pattern = r'([0-9A-Fa-f]{2}[-:]){5}[0-9A-Fa-f]{2}'
        mac_match = re.search(mac_pattern, arp_result.stdout)
        if mac_match:
            mac_address = mac_match.group(0).replace('-', ':')  # 统一格式为 xx:xx:xx:xx:xx:xx
            ndp_result = subprocess.run(
                ['netsh', 'interface', 'ipv6', 'show', 'neighbors'],
                capture_output=True,
                text=True
            )
            ipv6_from_ndp_pattern = rf'([A-Fa-f0-9:]+)\s+{mac_address.replace(":", "-")}\b'
            ipv6_match = re.search(ipv6_from_ndp_pattern, ndp_result.stdout)
            if ipv6_match:
                return ipv6_match.group(1)
            else:
                pass
        else:
            pass
    except Exception as e:
        pass
    return None  # 如果所有方式都未获取到 IPv6 地址


def get_ip():
    response_ip6 = requests.get('https://test.ipw.cn/api/ip/myip?json', headers=headers)
    ip6_json = response_ip6.json()
    response_ip4 = requests.get('https://4.ipw.cn/api/ip/myip?json', headers=headers)
    ip4_json = response_ip4.json()
    ypget_ipv4 = "192.168.0.106"
    yp2 = '192.168.0.175'
    ypget_ipv6 = get_ipv6_from_ipv4(ypget_ipv4)
    ypget2_ipv6 = get_ipv6_from_ipv4(yp2)
    html_msg = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>网络配置信息</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }}
            .header {{
                font-size: 1.2em;
                font-weight: bold;
            }}
            .content {{
                margin-top: 10px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 0.9em;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="header">尊敬的用户：</div>
        <div class="content">
            <p>您好！</p>
            <p>以下是您的网络配置信息：</p>
            <p>IPv6地址：{}</p>
            <p>IPv4地址：{}</p>
            <p>云盘地址（IPv6）：[{}]</p>
            <p>云盘地址（IPv6）：[{}]</p>
        </div>
        <div class="footer">
            <p>如有疑问，请随时与我们联系。</p>
            <p>祝好，</p>
            <p>JBWang</p>
        </div>
    </body>
    </html>
    """.format(ip6_json["IP"], ip4_json["IP"], ypget_ipv6, ypget2_ipv6)
    return html_msg


# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = '1022405818@qq.com'  # 发送者邮箱
to_addr = 'w17538620107@dingtalk.com'  # 接收者邮箱
password = 'pbftrnhmpwnvbeac'  # 授权码
smtp_server = 'smtp.qq.com'
# 收信方邮箱
# 发信服务器


# 创建一个实例msg
msg = MIMEMultipart()
msg['From'] = '"JBWang" <1022405818@qq.com>'  # 发送者
msg['To'] = Header('w17538620107@dingtalk.com')  # 接收者
subject = '代码运行结果'
msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
# 邮件正文内容
msg.attach(MIMEText(get_ip(), 'html', 'utf-8'))

try:
    smtpobj = smtplib.SMTP_SSL(smtp_server)
    smtpobj.connect(smtp_server, 465)  # 建立连接--qq邮箱服务和端口号
    smtpobj.login(from_addr, password)  # 登录--发送者账号和口令
    smtpobj.sendmail(from_addr, to_addr, msg.as_string())
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print("无法发送邮件:", e)
finally:
    # 关闭服务器
    smtpobj.quit()
