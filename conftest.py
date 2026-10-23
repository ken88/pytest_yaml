import logging
import subprocess

import pytest
import requests

from config.config import BASE_URL,USERNAME,PASSWORD
from utils.db_cleaner import run_cleanup

def pytest_sessionfinish(session, exitstatus):
    """
    全局钩子：整个测试会话结束后，自动生成 Allure HTML 报告
    """
    print("\n" + "=" * 50)
    print("🚀 测试执行完毕，开始生成 Allure HTML 可视化报告...")

    # 命令：根据你 pytest.ini 里的路径来生成
    cmd = "allure generate ./report/json_report -o ./report/html_report --clean --language zh"

    try:
        # 使用 shell=True 兼容各种环境（包括你刚才遇到的 Mac 环境变量问题）
        subprocess.run(cmd, shell=True, check=True)
        print("✅ 报告生成成功！")
        print("👉 你可以手动输入以下命令直接在浏览器中查看报告：")
        print("   allure open ./report/html_report")
    except subprocess.CalledProcessError as e:
        print(f"❌ 报告生成失败，错误信息: {e}")
    print("=" * 50 + "\n")

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

    try:
        res = requests.post(login_url, json=payload)
        if res.status_code == 200 and res.json().get("code") == 1:
            context["TOKEN"] =  res.json().get("data", {}).get("token")
            logging.info(f"前置登录成功，Token 已注入: {str(context['TOKEN'])[:10]}...")
        else:
            # 如果业务返回失败，调用 pytest.skip
            pytest.skip(f"【全局跳过】前置登录业务失败，返回: {res.text}")
    except Exception as e:
        # 如果网络异常等，也调用 pytest.skip
        pytest.skip(f"【全局跳过】前置登录发生异常: {e}")

    #  使用 yield 把字典交出去
    yield context

    # 后置操作
    context.clear()

    """后置清理：跑完了，把自己的战场打扫干净"""
    logging.info("=== 开始执行 [后置清理] ===")
    run_cleanup()
