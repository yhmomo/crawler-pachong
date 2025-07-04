import os

import pdf2image
import pytesseract
from PIL import Image

# 设置 Tesseract OCR 的可执行文件路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# 定义 PDF 文件路径
pdf_path = 'aa.pdf'

# 使用 pdf2image 将 PDF 转换为图像列表
pages = pdf2image.convert_from_path(pdf_path, dpi=600)

# 创建输出目录
output_dir = "output"  # 输出目录名称
os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在，创建它

# 初始化变量
pages_data = []  # 用于存储所有页面的图片数据
texts_path = []  # 用于存储所有页面的文字文件路径
all_text = ""  # 用于存储所有页面的文字内容

# 遍历每一页图像
for page_number, page_data in enumerate(pages):
    # 将图片数据添加到列表中
    pages_data.append(page_data)

    # 提取文字
    text = pytesseract.image_to_string(page_data, lang='chi_sim')  # 使用中文简体语言包提取文字
    all_text += text + "\n"  # 将文字内容添加到总文字中


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
merged_image_path = os.path.join(output_dir, 'merged_image.png')
merge_images(pages_data, merged_image_path)
print(f'图片已合并为: {merged_image_path}')

# 保存合并后的文字到文本文件中
merged_text_path = os.path.join(output_dir, 'merged_text.txt')
with open(merged_text_path, 'w', encoding='utf-8') as text_file:
    text_file.write(all_text)
print(f'文字已合并为: {merged_text_path}')

# # 删除原来的图片和文字文件
# for page_number in range(len(pages)):
#     image_path = os.path.join(output_dir, f'page_{page_number + 1}.png')
#     text_path = os.path.join(output_dir, f'page_{page_number + 1}.txt')
#     if os.path.exists(image_path):
#         os.remove(image_path)
#     if os.path.exists(text_path):
#         os.remove(text_path)
# print('原来的图片和文字文件已删除。')
