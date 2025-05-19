import threading, time, random, requests
from lxml import etree
from queue import Queue

urls = [f"http://localhost:5000/page/{num}" for num in range(200)]


def crawl(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()  # 检查请求是否成功
        res.encoding = "utf-8"
        content = res.text
        return content
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return ""


def parse(html_text):
    ht = etree.HTML(html_text)
    p1 = ht.xpath("//h1/text()")
    return p1


def do_crawl(url_queue: Queue, html_queue: Queue):
    while True:
        url = url_queue.get()
        if url is None:  # 退出信号
            url_queue.put(None)  # 让其他爬虫线程也收到信号
            html_queue.put(None)  # 告诉解析线程可以退出了
            break
        html = crawl(url)
        html_queue.put(html)
        # time.sleep(random.randint(1, 2))


def do_parse(html_queue: Queue, result_queue: Queue):
    while True:
        html = html_queue.get()
        if html is None:
            break
        results = parse(html)
        for result in results:
            result_queue.put(result)  # 不直接写文件，而是放入队列


def main():
    url_queue = Queue()
    html_queue = Queue()
    result_queue = Queue()  # 新增：存储解析结果

    # 填充URL队列
    for url in urls:
        url_queue.put(url)

    # 添加退出信号
    for _ in range(20):
        url_queue.put(None)

    # 启动爬虫线程
    crawl_threads = []
    for index in range(20):
        t = threading.Thread(
            target=do_crawl, args=(url_queue, html_queue), name=f"crawl{index}"
        )
        t.start()
        crawl_threads.append(t)

    # 启动解析线程
    parse_threads = []
    for index in range(2):
        t = threading.Thread(
            target=do_parse, args=(html_queue, result_queue), name=f"parse{index}"
        )
        t.start()
        parse_threads.append(t)

    # 等待所有解析线程完成
    for t in parse_threads:
        t.join()

    # 等待所有爬虫线程完成
    for t in crawl_threads:
        t.join()

    # 现在安全地写入文件（所有线程已完成）
    with open("duo.txt", "w") as fout:
        while not result_queue.empty():
            result = result_queue.get()
            fout.write(result + "\n")


if __name__ == "__main__":
    main()
