import re


def clean_string(input_string):
    # 检查输入是否为字符串
    if not isinstance(input_string, str):
        return input_string
    # 使用正则表达式替换所有空白字符为空字符串
    cleaned_string = re.sub(r'\s+', '', input_string)
    cleaned_string = re.sub(r'[<>:"/\\|?*]', '', cleaned_string)
    return cleaned_string
