import csv
import json
import re

import jieba
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.manifold import TSNE
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from wordcloud import WordCloud

# 设置字体为黑体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 或 'Microsoft YaHei'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'dnt': '1',
    'referer': 'https://tech.sina.com.cn/',
    'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
}


def get_news_content(url):
    """获取新闻正文内容"""
    contentStr = requests.get(url, headers=headers).content
    soup = BeautifulSoup(contentStr, 'lxml')
    contentsoup = soup.find('div', id='artibody')
    if contentsoup:
        paragraphs = contentsoup.find_all('p')
        contentText = "".join(p.text for p in paragraphs)
        return contentText
    return ""


def get_TitleAndUrl(page, writer):
    """获取标题和URL并写入CSV"""
    params = {
        'pageid': '372',
        'lid': '2431',
        'k': '',
        'num': '50',
        'page': page,
    }

    response = requests.get('https://feed.mix.sina.com.cn/api/roll/get', params=params, headers=headers)
    data_loaded = json.loads(response.text)
    data = data_loaded['result']['data']

    for item in data:
        title = item['title']
        url = item['url']
        contentText = get_news_content(url)
        writer.writerow([title, url, contentText])


# ========== 数据分析部分 ==========
def clean_text(text):
    """清洗文本数据"""
    if not isinstance(text, str):
        return ""
    # 保留中文、英文和基本标点
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？；：,.!?;:\s]', '', text)
    return text.strip()


def tokenize_text(text):
    """对文本进行分词处理"""
    text = clean_text(text)
    if not text:
        return []

    tokens = jieba.lcut(text)
    stopwords = set(
        ['的', '了', '和', '是', '我', '也', '就', '都', '及', '与', '等', '对', '中', '有', '在', '不', '上'])
    tokens = [t for t in tokens if len(t) > 1 and t not in stopwords]
    return tokens


def preprocess_df(df):
    """数据预处理"""
    df = df.dropna(subset=['contentText'])  # 移除空内容
    df['clean_content'] = df['contentText'].apply(clean_text)
    df['tokens'] = df['clean_content'].apply(tokenize_text)
    df['seg_str'] = df['tokens'].apply(lambda x: " ".join(x))
    return df


# 情感分析词库
pos_words = set(['创新', '领先', '突破', '增长', '支持', '利好', '提升', '优化'])
neg_words = set(['下滑', '失败', '危机', '拖累', '减少', '损失', '质疑', '问题'])


def simple_sentiment_label(tokens):
    """简单情感分析标注"""
    pos_count = sum(t in pos_words for t in tokens)
    neg_count = sum(t in neg_words for t in tokens)
    return 1 if pos_count > neg_count else 0


def label_sentiment(df):
    """添加情感标签"""
    df['sentiment'] = df['tokens'].apply(simple_sentiment_label)
    return df


def get_tfidf_features(df):
    """提取TF-IDF特征"""
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(df['seg_str'])
    return X, vectorizer


def train_classification_models(X_train, y_train, X_test, y_test):
    """训练分类模型"""
    print("== 逻辑回归 ==")
    lr = LogisticRegression(max_iter=500)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    print(classification_report(y_test, y_pred_lr))
    print("准确率:", accuracy_score(y_test, y_pred_lr))

    print("\n== 随机森林 ==")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    print(classification_report(y_test, y_pred_rf))
    print("准确率:", accuracy_score(y_test, y_pred_rf))
    return lr, rf


def cluster_text(X, n_clusters=4):
    """聚类分析"""
    print("\nKMeans聚类")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels_km = kmeans.fit_predict(X)

    print("\n层次聚类")
    agg = AgglomerativeClustering(n_clusters=n_clusters)
    labels_agg = agg.fit_predict(X.toarray())
    return labels_km, labels_agg


def plot_wordcloud(tokens_list, title='新浪科技新闻词云图'):
    """生成词云图"""
    text = " ".join([token for tokens in tokens_list for token in tokens])
    wordcloud = WordCloud(
        font_path='simhei.ttf',  # 使用黑体，确保字体文件存在
        background_color='white',
        width=800,
        height=400
    ).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()


def plot_heatmap(df, vectorizer):
    """绘制TF-IDF热力图"""
    X = vectorizer.transform(df['seg_str']).toarray()
    avg_tfidf = np.mean(X, axis=0)
    top_indices = np.argsort(avg_tfidf)[::-1][:20]
    top_words = [vectorizer.get_feature_names_out()[i] for i in top_indices]
    top_values = avg_tfidf[top_indices]

    df_heat = pd.DataFrame(top_values.reshape(1, -1), columns=top_words)
    plt.figure(figsize=(24, 10))
    sns.heatmap(df_heat, annot=True, cmap='YlGnBu', fmt=".2f")
    plt.title("TF-IDF 前20词热度图")
    plt.show()


def plot_pca_tsne(X, labels, title='文本降维可视化'):
    """降维可视化"""
    pca = PCA(n_components=50)
    X_pca = pca.fit_transform(X.toarray())

    tsne = TSNE(n_components=2, random_state=42)
    X_tsne = tsne.fit_transform(X_pca)

    plt.figure(figsize=(10, 8))
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=labels, cmap='viridis', alpha=0.6)
    plt.colorbar()
    plt.title(title)
    plt.xlabel('t-SNE 1')
    plt.ylabel('t-SNE 2')
    plt.show()


def analyze_data():
    """主分析函数"""
    # 读取爬取的数据
    try:
        df = pd.read_csv('news_data.csv')
        print(f"成功读取 {len(df)} 条新闻数据")
    except FileNotFoundError:
        print("未找到数据文件，请先运行数据获取部分")
        return

    # 预处理
    print("文本预处理中...")
    df = preprocess_df(df)
    print(f"预处理后有效数据: {len(df)} 条")

    if len(df) < 20:
        print("数据量不足，至少需要20条数据进行有效分析")
        return

    # 情感分析
    print("情感标注中...")
    df = label_sentiment(df)

    # TF-IDF特征提取
    print("TF-IDF特征提取...")
    X, vectorizer = get_tfidf_features(df)

    # 分类模型
    print("\n训练分类模型...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, df['sentiment'], test_size=0.3, random_state=42
    )
    train_classification_models(X_train, y_train, X_test, y_test)

    # 聚类分析
    print("\n聚类分析中...")
    labels_km, labels_agg = cluster_text(X, n_clusters=3)
    df['cluster_kmeans'] = labels_km
    df['cluster_agglo'] = labels_agg

    # 可视化
    print("\n生成词云图...")
    plot_wordcloud(df['tokens'])

    print("\n生成TF-IDF热力图...")
    plot_heatmap(df, vectorizer)

    print("\n降维可视化聚类结果 (KMeans)...")
    plot_pca_tsne(X, labels_km, title='KMeans聚类结果')

    print("\n降维可视化聚类结果 (层次聚类)...")
    plot_pca_tsne(X, labels_agg, title='层次聚类结果')


# ========== 主执行入口 ==========
if __name__ == '__main__':
    # 第一步：爬取数据并保存到CSV
    print("开始爬取新浪科技新闻...")
    with open('news_data.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['title', 'url', 'contentText'])
        for page in range(1, 20):  # 爬取19页数据
            print(f"正在爬取第 {page} 页...")
            get_TitleAndUrl(page, writer)

    print("\n爬取完成，开始数据分析...")
    # 第二步：进行数据分析
    analyze_data()
    print("分析完成！")
