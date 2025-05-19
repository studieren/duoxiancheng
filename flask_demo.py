# app.py
from flask import Flask, request, render_template
import time
import random
from datetime import datetime

app = Flask(__name__)


# 首页路由 - 列出所有测试页面
@app.route("/")
def index():
     

    return render_template(
        "index.html",
        title="Flask测试服务器",
        header="Flask测试服务器",
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request_url=request.url,
        request_method=request.method,
    )


# 分页示例
@app.route("/page/<int:page_id>")
def show_page(page_id):
    return render_template(
        "page.html",
        title=f"Page {page_id}",
        header=f"Page {page_id}",
        page_id=page_id,
        random_num=random.randint(1, 100),
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request_url=request.url,
        request_method=request.method,
    )


# 动态内容生成
@app.route("/dynamic")
def dynamic_content():
    content = request.args.get("content", "default content")
    return render_template(
        "dynamic.html",
        title="Dynamic Content",
        header="Dynamic Content",
        content=content,
        timestamp=int(time.time()),
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request_url=request.url,
        request_method=request.method,
    )


# 模拟延迟响应
@app.route("/delay")
def delayed_response():
    delay = request.args.get("t", "1")
    try:
        delay = float(delay)
    except ValueError:
        delay = 1.0

    start_time = time.time()
    time.sleep(delay)
    actual_delay = time.time() - start_time

    return render_template(
        "delay.html",
        title="Delayed Response",
        header="Delayed Response",
        requested_delay=delay,
        actual_delay=round(actual_delay, 2),
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request_url=request.url,
        request_method=request.method,
    )


# 生成随机数据
@app.route("/random_data")
def random_data():
    seed = request.args.get("seed", None)
    if seed:
        try:
            random.seed(int(seed))
        except:
            pass

    data = [random.randint(100, 999) for _ in range(10)]

    return render_template(
        "random_data.html",
        title="Random Data",
        header="Random Data",
        data=data,
        seed=seed if seed else "random",
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request_url=request.url,
        request_method=request.method,
    )


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
# 测试示例：

# http://localhost:5000/page/3

# http://localhost:5000/dynamic?content=test123

# http://localhost:5000/delay?t=1.5

# http://localhost:5000/random_data?seed=123

# 这个后端可以配合多线程爬虫练习：

# 多线程请求不同页面

# 处理动态生成的内容

# 处理延迟响应

# 保持会话状态（如果需要可以添加cookie支持）

# 解析HTML内容
