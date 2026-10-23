import logging

import allure
import jsonpath
import pytest


def json_extractor(case,res_http,global_context):
    extract_dict = case.get("jsonExData")
    if not extract_dict:
        return
    with allure.step("4.JSON提取数据"):
        res_json = res_http.json()

        for key, path in extract_dict.items():
            res_list = jsonpath.jsonpath(res_json, path)
            if not res_list:
                pytest.fail(f"提取失败: 找不到路径 {path}")
            else:
                # 把提取到的值存入上下文字典
                global_context[key] = res_list[0]
        logging.info(f'4.JSON提取，根据{extract_dict}提取数据，此时全局变量为:{global_context}')