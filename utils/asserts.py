import logging
import allure
import jsonpath
from utils.pymysql import query_one


@allure.step("3.HTTP响应断言")
def http_assert(case,res_http):
    if case["check"]:
        result = jsonpath.jsonpath(res_http.json(), case["check"])[0]
        logging.info(f'3.HTTP响应断言内容:实际结果({result}) == 预期结果({case["expected"]})')
        assert result == case["expected"]
    else:
        logging.info(f'3.HTTP响应断言内容:预期结果({case["expected"]})in 实际结果({res_http.text})')
        assert case["expected"] in res_http.text

def jdbc_assert(case):
    if case["sql_check"] and case["sql_expected"]:
        with allure.step("3.JDBC数据库断言"):
            res_db = query_one(case["sql_check"])
            logging.info(f'3.JDBc响应断言内容:实际结果({res_db})== 预期结果({case["sql_expected"]})')
            assert res_db == case["sql_expected"]