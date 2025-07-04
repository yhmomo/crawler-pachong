import os

from PIL import Image


def imgPDF(source_folder, output_folder):
    """
    将指定文件夹中的所有图片转换为一个 PDF 文件。
    遍历 source_folder 下的所有文件夹，将每个文件夹中的图片转换为 PDF 文件，
    并将输出的 PDF 文件保存到 output_folder 文件夹中。
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        if os.path.isdir(folder_path):
            pdf_name = f"{folder_name}.pdf"
            pdf_path = os.path.join(output_folder, pdf_name)
            images = []
            filenames = os.listdir(folder_path)
            # 按文件名中“ảnh”后的数字从小到大排序
            if "ảnh" in filenames:
                filenames.sort(key=lambda x: int(x.split('ảnh')[1].split('.')[0]))
            for filename in filenames:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    image_path = os.path.join(folder_path, filename)
                    img = Image.open(image_path)
                    # 调整图片宽度为595像素(A4宽度)，同时保持宽高比
                    width_percent = 595 / img.size[0]
                    new_height = int(img.size[1] * width_percent)
                    img = img.resize((595, new_height), Image.LANCZOS).convert('RGB')
                    images.append(img)

            if images:
                images[0].save(pdf_path, save_all=True, append_images=images[1:])
                print(f"已将文件夹 {folder_path} 中的图片转换为 PDF 文件 {pdf_path}")
            else:
                print(f"文件夹 {folder_path} 中没有找到图片文件")
    print("所有图片已转换为 PDF 文件")
