# app.py
from flask import Flask, request, make_response
import time
import random

app = Flask(__name__)


# 首页路由 - 列出所有测试页面
@app.route("/")
def index():
    links = [
        "<h1>Flask测试服务器</h1>",
        "<p>可用测试路径：</p>",
        '<a href="/page/1">/page/1</a> - 基础页面示例',
        '<a href="/dynamic?content=hello">/dynamic?content=hello</a> - 动态内容示例',
        '<a href="/delay?t=2">/delay?t=2</a> - 延迟响应示例',
        '<a href="/random_data?seed=42">/random_data?seed=42</a> - 随机数据生成示例',
    ]
    return "<br>".join(links)


# 分页示例
@app.route("/page/<int:page_id>")
def show_page(page_id):
    return f"""
        <h1>Page {page_id}</h1>
        <p>This is test page {page_id}</p>
        <p>Random number: {random.randint(1, 100)}</p>
    """


# 动态内容生成
@app.route("/dynamic")
def dynamic_content():
    content = request.args.get("content", "default content")
    return f"""
        <h1>Dynamic Content</h1>
        <p>Your content: {content}</p>
        <p>Timestamp: {int(time.time())}</p>
    """


# 模拟延迟响应
@app.route("/delay")
def delayed_response():
    delay = request.args.get("t", "1")
    try:
        delay = float(delay)
    except ValueError:
        delay = 1.0

    time.sleep(delay)
    return f"""
        <h1>Delayed Response</h1>
        <p>Waited {delay} seconds</p>
        <p>Actual delay: {delay}s</p>
    """


# 生成随机数据
@app.route("/random_data")
def random_data():
    seed = request.args.get("seed", None)
    if seed:
        try:
            random.seed(int(seed))
        except:
            pass

    data = [
        f"<tr><td>Item {i}</td><td>{random.randint(100, 999)}</td></tr>"
        for i in range(1, 11)
    ]
    return f"""
        <h1>Random Data</h1>
        <table border="1">
            {"".join(data)}
        </table>
        <p>Seed used: {seed if seed else "random"}</p>
    """


if __name__ == "__main__":
    app.run(debug=True, threaded=True)  # 启用多线程模式
