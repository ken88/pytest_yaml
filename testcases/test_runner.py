import logging
import pytest
from utils.analyse_case import analyse_case, replace_vars
from utils.asserts import http_assert, jdbc_assert
from utils.extractor import json_extractor
from utils.allure_utils import allure_init
from utils.send_request import send_http_request
from utils.yaml_utils import read_yaml


class TestRunner:
    # 读取yaml测试数据
    data = read_yaml()

    @pytest.mark.parametrize("case", data)
    def test_case(self, case, global_context):

        # 1. 初始化allure报告
        allure_init(case)
        logging.info(f'1.用例ID:{case["id"]} 模块:{case["feature"]} 场景:{case["story"]}')

        # 2. 渲染替换：遍历 case 字典，把里面的 ${TOKEN} 等占位符换成 global_context 里的真实值
        rendered_case = replace_vars(case, global_context)

        # 3. 解析请求数据
        req_data = analyse_case(rendered_case)

        # 4. 发起HTTP请求
        res_http = send_http_request(**req_data)

        # 5. http响应断言
        http_assert(rendered_case,res_http)
        #
        # # 数据库断言
        jdbc_assert(rendered_case)
        #
        # json提取
        json_extractor(rendered_case,res_http,global_context)

        # logging.info(f"JSON提取完成，此时全局变量为: {global_context}")
