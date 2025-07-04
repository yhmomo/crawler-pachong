from del_FD import FDdel

output_folder = r"D:\txet\pdf"
source_folder = r"D:\txet\cangcuc"
if __name__ == '__main__':
    print("删除文件夹")
    FDdel(source_folder, output_folder)
    print("-------------------------------------------")

    # print("删除筛选文件与已图片后缀的数据")
    # WJdel(source_folder, output_folder)
    # print("-------------------------------------------")
    #
    # print("将文件夹中的图片转换为PDF")
    # imgPDF(source_folder, output_folder)  # 数据导出
    # print("-------------------------------------------")
    # print("数据处理完成")

    # print("删除文件夹中图片")
    # print("-------------------------------------------")
    # imgdel(source_folder, output_folder)
    # print("数据处理完成")
