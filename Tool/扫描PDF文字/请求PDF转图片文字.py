import os
from datetime import datetime

import pdf2image
import pytesseract
import requests
from PIL import Image


def getPDFtoimg(binary_data, title):
    # 设置 Tesseract OCR 的可执行文件路径
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    pdf_binary_data = binary_data
    pdf_title = title
    pages = pdf2image.convert_from_bytes(pdf_binary_data, dpi=600)

    output_dir = "output"  # 输出目录名称
    os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在，创建它

    pages_data = []  # 用于存储所有页面的图片数据
    all_text = ""  # 用于存储所有页面的文字内容

    for page_number, page_data in enumerate(pages):
        pages_data.append(page_data)
        text = pytesseract.image_to_string(page_data, lang='chi_sim')  # 使用中文简体语言包提取文字
        all_text += text  # 将文字内容添加到总文字中

    # 合并图片
    def merge_images(image_list, output_path):
        widths, heights = zip(*(i.size for i in image_list))
        total_width = max(widths)
        total_height = sum(heights)
        new_img = Image.new('RGB', (total_width, total_height))
        y_offset = 0
        for img in image_list:
            new_img.paste(img, (0, y_offset))
            y_offset += img.height
        new_img.save(output_path)

    # 合并图片并保存
    merged_image_path = os.path.join(output_dir, pdf_title + '.png')
    merge_images(pages_data, merged_image_path)
    print(f'图片已合并为: {merged_image_path}')

    # 保存合并后的文字到文本文件中
    merged_text_path = os.path.join(output_dir, pdf_title + '.txt')
    with open(merged_text_path, 'w', encoding='utf-8') as text_file:
        text_file.write(all_text)
    print(f'文字已合并为: {merged_text_path}')


def getPDFtoimg_url(response):
    timestamp = datetime.now().timestamp()
    title = str(int(timestamp))
    binary_data = response.content
    getPDFtoimg(binary_data, title)


if __name__ == '__main__':
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(
        'https://bidfile.norincogroup-ebuy.com/bdfileservice//upfile2023/tpl/pdf/014301/C1100000096008036020/zbgg/16885f32ccb14a0ba0db6382a7450594.pdf',
        headers=headers,
    )
    getPDFtoimg_url(response)
