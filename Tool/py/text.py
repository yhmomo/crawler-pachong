import PyPDF2
from PIL import Image, ImageDraw, ImageFont
from spire.ocr import *
from spire.pdf import *


def pdfimgtxet():
    # 将PDF页面转换为图片
    def convert_pdf_page_to_image(pdf, page_index):
        return pdf.SaveAsImage(page_index)

    # 从图片中识别文本
    def recognize_text_from_image(imgName, language, model_path):
        # 初始化OCR扫描器并配置OCR模型的路径和文本识别语言
        scanner = OcrScanner()
        configure_options = ConfigureOptions()
        configure_options.Language = language
        configure_options.ModelPath = model_path
        scanner.ConfigureDependencies(configure_options)

        # 执行OCR并返回识别的文本
        scanner.Scan(imgName)
        data = scanner.Text.ToString()
        return data

    # 加载扫描PDF文档
    pdf = PdfDocument()
    pdf.LoadFromFile('sample.pdf')

    # 创建文本文件以保存提取的文本
    with open('扫描PDF.txt', 'a', encoding='utf-8') as writer:
        for page_index in range(pdf.Pages.Count):
            # 将PDF页面转换为图片
            image = convert_pdf_page_to_image(pdf, page_index)
            imgName = "toImage_" + str(page_index) + ".png"
            image.Save(imgName)

            # 从图片中识别文本
            recognized_text = recognize_text_from_image(imgName, 'Chinese', r'D:\OCR\win-x64')

            # 将识别的文本写入文本文件
            writer.write(f'Page {page_index + 1}:\n')
            writer.write(recognized_text)
            writer.write('\n\n')  # 在页面之间添加两个换行符

    print('文本已成功保存到"扫描PDF.txt"。')


def pdfto_img(response):
    with open("sample.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)

    # 打开 PDF 文件
    with open("sample.pdf", "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # 提取每一页的文字内容
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()

    print(text_content)

    # 创建一个白色背景的图片，大小可以根据文字内容调整
    image = Image.new('RGB', (800, 600), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 选择字体和字体大小，字体文件需要在系统中存在
    font = ImageFont.truetype("arial.ttf", 20)

    # 在图片上绘制文字，位置可以根据需要调整
    draw.text((10, 10), text_content, fill=(0, 0, 0), font=font)

    # 保存图片
    image.save("output.png")


if __name__ == "__main__":
    pdfimgtxet()
    # cookies = {
    #     'SESSION': 'ODIyNTg0Y2QtOGNhYS00YTBlLTg3NzItNmI5OTBiYWYxYTgw',
    # }
    #
    # headers = {
    #     'Accept': '*/*',
    #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    #     'Connection': 'keep-alive',
    #     'Referer': 'http://www.tdztb.com//resource/css/pdfjs/web/viewer.html?file=http://www.tdztb.com/bidprocurement/datacenter-cebpubserver/cebpubserver/dataCeboubServerCommonController/openFileById?fileType%3D5%26id%3Db6256c5e7b98456994d57dfe87238f36&page=1',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    #     # 'Cookie': 'SESSION=ODIyNTg0Y2QtOGNhYS00YTBlLTg3NzItNmI5OTBiYWYxYTgw',
    # }
    #
    # params = {
    #     'fileType': '5',
    #     'id': 'b6256c5e7b98456994d57dfe87238f36',
    # }
    #
    # response = requests.get(
    #     'http://www.tdztb.com/bidprocurement/datacenter-cebpubserver/cebpubserver/dataCeboubServerCommonController/openFileById',
    #     params=params,
    #     cookies=cookies,
    #     headers=headers,
    #     verify=False,
    # )
    # pdfto_img(response)
