import os

from PIL import Image

source_folder = r"D:/downloaded_images"
output_folder = r"D:/downloaded_images"


def imgPDF(source_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filenames = os.listdir(source_folder)
    filenames.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    images = []
    for filename in filenames:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(source_folder, filename)
            img = Image.open(image_path)
            # 调整图片宽度为595像素(A4宽度)，同时保持宽高比
            width_percent = 595 / img.size[0]
            new_height = int(img.size[1] * width_percent)
            img = img.resize((595, new_height), Image.LANCZOS).convert('RGB')
            images.append(img)

    if images:
        pdf_path = os.path.join(output_folder, 'output.pdf')
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        print(f"已将文件夹 {source_folder} 中的图片转换为 PDF 文件 {pdf_path}")
    else:
        print(f"文件夹 {source_folder} 中没有找到图片文件")


print("所有图片已转换为 PDF 文件")

imgPDF(source_folder, output_folder)
