import logging

import pytest
import requests

from config.config import BASE_URL,USERNAME,PASSWORD
from utils.db_cleaner import run_cleanup


@pytest.fixture(scope="session", autouse=True)
def global_context():
    """前置清理：把昨天或者之前没删干净的干掉"""
    logging.info("=== 开始执行 [前置清理] ===")
    run_cleanup()

    # 定义一个全局的测试上下文（字典）。
    # 用于在不同测试用例之间传递数据，例如 Token、新增的 ID 等。
    # 前置操作：初始化一个空字典
    context = {}

    # 框架启动时，自动去请求一次登录接口（前置造数据）
    login_url = f"{BASE_URL}/login"
    payload = {"username": USERNAME, "password": PASSWORD}

    res = requests.post(login_url, json=payload)

    try:
        res = requests.post(login_url, json=payload)
        if res.status_code == 200 and res.json().get("code") == 1:
            context["TOKEN"] =  res.json().get("data", {}).get("token")
            logging.info(f"前置登录成功，Token 已注入: {context['TOKEN'][:10]}...")
        else:
            # 如果业务返回失败，调用 pytest.skip
            pytest.skip(f"【全局跳过】前置登录业务失败，返回: {res.text}")
    except Exception as e:
        # 如果网络异常等，也调用 pytest.skip
        pytest.skip(f"【全局跳过】前置登录发生异常: {e}")


    #  提取 Token 并存入上下文
    if res.status_code == 200 and res.json().get("code") == 1:
        token = res.json().get("data", {}).get("token")
        context["TOKEN"] = token  # 存起来

    else:
        # 如果业务返回失败，调用 pytest.skip
        pytest.skip(f"【全局跳过】前置登录业务失败，返回: {res.text}")
    #  使用 yield 把字典交出去
    yield context

    # 后置操作
    context.clear()

    """后置清理：跑完了，把自己的战场打扫干净"""
    logging.info("=== 开始执行 [后置清理] ===")
    run_cleanup()