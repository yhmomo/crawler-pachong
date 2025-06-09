from del_FD import WJdel, FDdel
from imgPDF import imgPDF

output_folder = r"D:\txet\pdf"
source_folder = r"D:\txet\cangcuc"
if __name__ == '__main__':
    print("删除文件夹中非图片文件")
    FDdel(source_folder, output_folder)
    print("-------------------------------------------")

    print("删除文件夹中筛选文件")
    WJdel(source_folder, output_folder)
    print("-------------------------------------------")

    print("将文件夹中的图片转换为PDF")
    imgPDF(source_folder, output_folder)  # 数据导出
    print("-------------------------------------------")
    print("数据处理完成")
