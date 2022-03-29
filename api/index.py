import re
import json
import requests
from gevent import pywsgi
from datetime import datetime
from flask import Flask, request, Response


# 实例化api，把当前这个python文件当作一个服务，__name__代表当前这个python文件
app = Flask(__name__)


def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def get_data(name, year=None):
    if year:
        url = "https://github.com/" + name + f"?from={year}-01-01&to={year}-12-31"
    else:
        url = "https://github.com/" + name
    git_page = requests.get(url)
    data = git_page.text
    data_date_reg = re.compile(r'data-date="(.*?)" data-level')
    data_count_reg = re.compile(r'data-count="(.*?)" data-date')
    data_date = data_date_reg.findall(data)
    data_count = data_count_reg.findall(data)
    data_count = list(map(int, data_count))
    contributions = sum(data_count)
    datalist = []
    for index, item in enumerate(data_date):
        item_list = {"date": item, "count": data_count[index]}
        datalist.append(item_list)
    data_list_split = list_split(datalist, 7)
    return_data = {
        "total": contributions,
        "contributions": data_list_split
    }
    return return_data


@app.route('/api', methods=['get'])
def do_get():
    """
    路径格式大约为 /api/freedomgod?y=2021
    :param user_name:
    :return:
    """
    user_name = request.args.get("username", "freedomgod")
    cur_year = request.args.get("year", datetime.now().year)
    data = get_data(user_name, cur_year)
    return Response(json.dumps(data), content_type='application/json')


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
    app.run()
