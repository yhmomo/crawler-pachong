import os
import shutil

import cv2
from PIL import Image


def FDdel(source_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        # 判断文件夹是否为空
        if not os.listdir(folder_path):  # 文件夹为空
            try:
                os.rmdir(folder_path)  # 删除空文件夹
                print(f"已删除空文件夹: {folder_path}")
            except Exception as e:
                print(f"删除文件夹 {folder_path} 时出错: {e}")
        # 文件夹不为空且文件夹名包含"[AIGenerated]"，删除文件夹及其内容
        elif "AIGenerated" in folder_name:
            try:
                shutil.rmtree(folder_path)
                print(f"已删除文件夹及其内容: {folder_path}")
            except Exception as e:
                print(f"删除文件夹 {folder_path} 时出错: {e}")
        else:
            print(f"保留文件夹: {folder_name}")
    print("删除文件夹成功")


def is_valid_video(file_path):
    """检查视频是否可被 OpenCV 正常读取"""
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        return False
    # 尝试读取一帧以确认视频完整性
    ret, _ = cap.read()
    cap.release()
    return ret


def WJdel(source_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        if os.path.isdir(folder_path):
            for filename in sorted(os.listdir(folder_path)):
                file_path = os.path.join(folder_path, filename)

                # 图片处理部分
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    try:
                        img = Image.open(file_path)
                        img.verify()
                        # print("图片有效:", file_path)  # 快速检查是否为有效图像文件
                    except Exception as e:
                        os.remove(file_path)
                        print("图片无效或损坏:", file_path, "已删除", e)

                # 视频处理部分
                elif filename.lower().endswith('.mp4'):
                    try:
                        if not is_valid_video(file_path):
                            raise Exception("视频无法读取")
                        # print("视频有效:", file_path)
                    except Exception as e:
                        os.remove(file_path)
                        print("视频无效或损坏:", file_path, "已删除", e)
                # 其他非图片/视频文件可选处理（如日志记录）
                else:
                    print("未知文件类型，跳过:", file_path)
    print("筛选的文件已删除完成")


def imgdel(source_folder, output_folder):
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        if os.path.isdir(folder_path):
            for filename in sorted(os.listdir(folder_path)):
                file_path = os.path.join(folder_path, filename)

                # 图片处理部分
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    os.remove(file_path)
    print("图片已删除完成")
# # 视频处理部分
# elif filename.lower().endswith('.mp4'):
#     try:
#         if not is_valid_video(file_path):
#             raise Exception("视频无法读取")
#         # print("视频有效:", file_path)
#     except Exception as e:
#         os.remove(file_path)
#         print("视频无效或损坏:", file_path, "已删除", e)
