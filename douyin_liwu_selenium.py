import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from lxml import etree
import time
from jinja2 import Environment, FileSystemLoader


def get_first_element_value(lst):
    return lst[0] if lst else ""


def read_data(driver):
    return driver.page_source


def analysis_data():
    # 设置 ChromeDriver 的路径
    service = Service(r"C:\Python\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    # 替换为实际的网页 URL
    driver.get("https://baidu.com")
    # 滚动次数
    scroll_times = 3
    for _ in range(scroll_times):
        # 模拟按下 Page Down 键滚动页面
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        # 等待页面加载新数据
        time.sleep(2)

    html_text = read_data(driver)
    ht = etree.HTML(html_text)
    line_list = ht.xpath('//div[@class="xo0lKTXY"]')
    data_list = []
    with open("liwu.csv", "w", encoding="utf-8-sig", newline="") as f:
        csv_writer = csv.writer(f)
        for line in line_list:
            img_url = get_first_element_value(line.xpath(".//img/@src"))
            price = get_first_element_value(
                line.xpath('.//div[@class="qO_N1Mn_"]/span/text()')
            )
            name = get_first_element_value(
                line.xpath('.//div[@class="DCwD5QXG FwVIESLr"]//text()')
            )

            new_list = [img_url, price, name]
            if new_list:
                if new_list not in data_list:
                    data_list.append(new_list)
                    csv_writer.writerow(new_list)
    ss = input("")
    # driver.quit()
    return data_list


# button //div[@id="giftPanelEntrance"]
def mouse_move():
    from selenium import webdriver
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import time

    # 初始化 Chrome 浏览器驱动
    driver = webdriver.Chrome()

    try:
        # 打开目标网页，替换为实际网页 URL
        driver.get("https://example.com")

        # 等待页面加载完成，可根据实际情况调整等待时间
        time.sleep(3)

        # 定位需要鼠标悬停并点击的元素，这里以元素的 ID 为例，可根据实际情况修改定位方式
        target_element = driver.find_element(By.ID, "element_id")

        # 创建 ActionChains 对象，用于执行鼠标操作
        actions = ActionChains(driver)

        # 移动鼠标到目标元素上方
        actions.move_to_element(target_element).perform()
        time.sleep(1)

        # 点击目标元素以触发菜单
        actions.click(target_element).perform()
        time.sleep(2)

        # 定位菜单元素，这里以元素的 CSS 选择器为例，可根据实际情况修改定位方式
        menu_element = driver.find_element(By.CSS_SELECTOR, "menu_css_selector")

        # 不断滚动菜单直到获取所有信息
        previous_height = 0
        while True:
            # 获取当前菜单的滚动高度
            current_height = driver.execute_script(
                "return arguments[0].scrollHeight", menu_element
            )

            # 如果滚动高度没有变化，说明已经滚动到菜单底部
            if current_height == previous_height:
                break

            previous_height = current_height

            # 模拟鼠标滚轮滚动菜单
            actions.move_to_element(menu_element).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)

        # 此时菜单已经滚动到最底部，可以获取菜单中的所有信息
        menu_items = menu_element.find_elements(
            By.CSS_SELECTOR, "menu_item_css_selector"
        )
        for item in menu_items:
            print(item.text)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # 关闭浏览器
        driver.quit()


def write_html():
    data = analysis_data()
    # 配置 Jinja2 环境
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.html")
    # 渲染模板
    output = template.render(data=data)
    # 将渲染后的内容保存为 HTML 文件
    with open("output.html", "w", encoding="utf-8") as f:
        f.write(output)


if __name__ == "__main__":
    # analysis_data()
    write_html()
