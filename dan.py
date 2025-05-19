import requests
from lxml import etree



def crawl(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()  # 检查请求是否成功
        res.encoding = res.apparent_encoding  # 自动检测编码
        return res.text
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return ""


def parse(html_text):
    ht = etree.HTML(html_text)
    p1 = ht.xpath("//h1/text()")
    return p1
