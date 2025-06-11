import os

import pdf2image  # 将 PDF 转换为图像
import pytesseract  # OCR 库

# 设置 Tesseract OCR 的可执行文件路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# 定义 PDF 文件路径
pdf_path = 'sample.pdf'

# 使用 pdf2image 将 PDF 转换为图像列表
pages = pdf2image.convert_from_path(pdf_path, dpi=600)

# 创建输出目录
output_dir = "output"  # 输出目录名称
os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在，创建它

# 遍历每一页图像
for page_number, page_data in enumerate(pages):
    # 保存图片为 PNG 文件
    image_path = os.path.join(output_dir, f'page_{page_number + 1}.png')  # 图片保存路径
    page_data.save(image_path, 'PNG')  # 保存图片
    print(f'保存了图片: {image_path}')

    # 提取文字
    text = pytesseract.image_to_string(page_data, lang='chi_sim')  # 使用中文简体语言包提取文字

    # 保存提取的文字到文本文件中
    text_path = os.path.join(output_dir, f'page_{page_number + 1}.txt')  # 文字保存路径
    with open(text_path, 'w', encoding='utf-8') as text_file:  # 打开文件并写入
        text_file.write(text)
    print(f'保存了文字: {text_path}')

print('所有页面处理完毕。')
