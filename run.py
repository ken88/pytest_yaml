import os
import subprocess

import pytest

# --alluredir ./report/json_report 指定一个目录，并生成中间结果
# --clean-alluredir 每次运行会清空中间结果

# os.system(命令) 相当于在 cmd 中执行命令
# allure generate 中间结果目录 -o 目标html报告目录 --clean

if __name__ == "__main__":
    pytest.main()

    # 通过 subprocess 生成 allure报告
    # print("=== 开始生成 Allure HTML 报告 ===")
    # try:
    #     cmd = "allure generate ./report/json_report -o ./report/html_report --clean --language zh"
    #     subprocess.run(cmd, shell=True, check=True)
    #
    #     print("=== ✅ 测试完成，报告已生成在 ./report/html_report ===")
    #
    # except subprocess.CalledProcessError as e:
    #     print(f"=== ❌ 报告生成失败，请检查是否安装了 Allure 并配置了环境变量。错误信息: {e} ===")

    # 通过os.system 生成 allure报告
    # os.system("allure generate ./report/json_report -o ./report/html_report --clean --language zh")
    # 可选：自动打开报告
    # os.system("allure open ./report/html_report")