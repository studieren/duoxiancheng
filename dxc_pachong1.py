import requests, threading
from lxml import etree

urls = [f"http://localhost:5000/page/{num}" for num in range(200)]


def crawl_one(url):
    res = requests.get(url)
    # print(len(res.text))
    print(res.text)


def parse(html_text):
    ht = etree.HTML(html_text)
    p1 = ht.xpath("//h1/text()")
    print(p1)


if __name__ == "__main__":
    ts = []
    for index, url in enumerate(urls):
        sub_crawl = threading.Thread(target=crawl_one, args=(url,))
        ts.append(sub_crawl)
        sub_crawl.start()

    for p in ts:
        p.join()
    print("结束")
