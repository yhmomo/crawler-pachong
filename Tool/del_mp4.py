import os
import subprocess

from PIL.Image import Image


def is_valid_video_ffmpeg(file_path):
    """使用ffmpeg检查视频是否有效"""
    try:
        # 使用ffmpeg检查视频文件
        result = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", file_path, "-f", "null", "-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # 如果ffmpeg没有报错，则认为视频有效
        if result.returncode == 0:
            return True
        else:
            print("ffmpeg校验视频时发现错误:", result.stderr.decode())
            return False
    except Exception as e:
        print("ffmpeg校验视频时出错:", e)
        return False


def WJdel(source_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for folder_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, folder_name)

        # 图片处理部分
        if folder_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            try:
                img = Image.open(file_path)
                img.verify()
            except Exception as e:
                os.remove(file_path)
                print("图片无效或损坏:", file_path, "已删除", e)

        # 视频处理部分
        elif folder_name.lower().endswith('.mp4'):
            try:
                if not is_valid_video_ffmpeg(file_path):
                    raise Exception("视频无法读取")
            except Exception as e:
                os.remove(file_path)
                print("视频无效或损坏:", file_path, "已删除", e)
        else:
            print("未知文件类型，跳过:", file_path)
    print("筛选的文件已删除完成")
