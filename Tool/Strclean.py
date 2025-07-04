import re


def clean_string(input_string):
    # 检查输入是否为字符串
    if not isinstance(input_string, str):  # 如果输入不是字符串，直接返回
        return input_string
    if 'http' in input_string:  # 如果字符串中包含'http'
        pattern = r'\n|\r|\t|\b|\f'  # 定义要替换的特殊字符模式
        cleaned_string = re.sub(pattern, '', input_string)  # 替换特殊字符为空字符串
    else:
        # 先移除特殊字符，再移除空白字符
        pattern = r'\n|\r|\t|\b|\f'  # 定义要替换的特殊字符模式
        cleaned_string1 = re.sub(pattern, '', input_string)  # 替换特殊字符为空字符串
        input_string = re.sub(r'[<>:"/\\|?*]', '', cleaned_string1)  # 移除特殊字符
        cleaned_string = re.sub(r'\s+', '', input_string)  # 移除所有空白字符
    return cleaned_string


def trim(str):
    if str is None:
        return None
    else:
        str = str.strip()
        str = str.replace("\r", "")
        str = str.replace("\t", "")
        str = str.replace(" ", "")
        str = str.replace("　", "")
        str = str.replace(" ", "")
        str = str.replace("?", "")
        str = str.replace("&", "")
        str = str.replace("nbsp", "")
        str = str.replace(" ", "")
        str = str.replace("/", "")
        return str
