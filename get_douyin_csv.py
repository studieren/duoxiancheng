from lxml import etree
import csv
from jinja2 import Environment, FileSystemLoader


def read_data():
    with open("temp.html", "r", encoding="utf-8") as f:
        return f.read()


def get_first_element_value(elements):
    texts = [element.strip() for element in elements if element.strip()]
    return "".join(texts) if texts else None


def analysis_data():
    html_text = read_data()
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
    return data_list


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
    write_html()
