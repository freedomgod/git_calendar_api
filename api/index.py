import json
from gevent import pywsgi
from api.util import get_data
from datetime import datetime
from flask import Flask, request, Response


# 实例化api，把当前这个python文件当作一个服务，__name__代表当前这个python文件
app = Flask(__name__)


@app.route('/api', methods=['get', 'post'])
def do_get():
    """
    路径格式大约为 /api?usernamefreedomgod?year=2021
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
