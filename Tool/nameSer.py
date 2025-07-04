import re
from typing import List, Tuple

import jieba

# 百家姓列表（部分）
common_surnames = [
    '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈',
    '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
    '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏',
    '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
    '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦',
    '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
    '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺',
    '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
    '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余',
    '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹'
]

# 构建正则表达式模式
surname_pattern = re.compile(f'^({"|".join(common_surnames)})(.*)$')


def extract_surnames_from_text(text: str) -> List[Tuple[str, str]]:
    """
    从文本中提取可能的姓氏和名字组合

    参数:
        text: 输入的文本内容

    返回:
        包含(姓氏, 名字)元组的列表
    """
    # 使用jieba分词
    words = jieba.lcut(text)

    results = []
    for word in words:
        # 检查是否为2-4个字符的词语（中文姓名通常2-4字）
        if 2 <= len(word) <= 4:
            match = surname_pattern.match(word)
            if match:
                surname = match.group(1)
                given_name = match.group(2)
                results.append((surname, given_name))

    return results


def extract_surnames_from_name(name: str) -> Tuple[str, str]:
    """
    从单个姓名中提取姓氏

    参数:
        name: 姓名字符串

    返回:
        (姓氏, 名字)元组，如无法识别返回(None, None)
    """
    match = surname_pattern.match(name)
    if match:
        return match.group(1), match.group(2)
    return None, None
