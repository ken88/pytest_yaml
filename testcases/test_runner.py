import logging
import pytest
from jinja2 import Template
from utils.analyse_case import analyse_case
from utils.asserts import http_assert, jdbc_assert
from utils.extractor import json_extractor

from utils.allure_utils import allure_init
from utils.send_request import send_http_request
from utils.yaml_utils import read_yaml


class TestRunner:
    # 读取excel测试数据
    data = read_yaml()

    # 全局变量，存放jsonExData解析数据，例如全局token。。。
    all = {}
    @pytest.mark.parametrize("case", data)
    def test_case(self,case):
        all = self.all

        # 根据all的值，渲染case
        case = eval(Template(str(case)).render(all))

        # 初始化allure报告
        allure_init(case)
        logging.info(f'1.用例ID:{case["id"]} 模块:{case["feature"]} 场景:{case["story"]}')

        # logging.info(case)
        # 解析请求数据
        req_data = analyse_case(case)

        # print("请求参数：",req_data)
        res_http =send_http_request(**req_data)
        # print("返回结果：",res_http.json())
        # assert res.json()["msg"] == case["expected"]

        # http响应断言
        http_assert(case,res_http)

        # 数据库断言
        jdbc_assert(case)

        # json提取
        json_extractor(case,res_http,all)
        print("全局变量",all)