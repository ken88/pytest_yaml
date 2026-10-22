import logging

import allure
import jsonpath


def json_extractor(case,res_http,all):
    if case["jsonExData"]:
        with allure.step("4.JSON提取数据"):
            for key, value in case["jsonExData"].items():
                # print(key)
                # print(value)
                value = jsonpath.jsonpath(res_http.json(), value)[0]
                # print(value)
                all[key] = value
            logging.info(f'4.JSON提取，根据{case["jsonExData"]}提取数据，此时全局变量为:{all}')