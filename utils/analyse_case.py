import json
import logging

import allure

from config.config import BASE_URL


@allure.step("1.解析请求数据")
def analyse_case(case):
    request_data = {
        "method": case["method"],
        "url": BASE_URL + case["path"],
        "headers": case["headers"],
        "params": case["params"],
        "data": case["data"],
        "json": str_to_obj(case["json"]),
        "files": case["files"]
    }
    logging.info(f'1.解析请求数据，请求数据为:{request_data}')
    # allure.attach(f"{request_data}",name="解析数据结果")
    return request_data

def str_to_obj(value):
    if isinstance(value, str):
        # 优先json.loads，更安全；如果需要兼容python字典写法再用eval
        return json.loads(value)
    return value
