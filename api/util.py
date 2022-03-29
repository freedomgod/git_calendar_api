def list_split(items, n):
    """
    将列表分割，每份n个
    :param items:
    :param n:
    :return:
    """
    return [items[i:i + n] for i in range(0, len(items), n)]


def get_data(name, year=None):
    """
    用requests获取GitHub提交的数据，可提供年份数据，默认为今年
    :param name:
    :param year:
    :return:
    """
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
