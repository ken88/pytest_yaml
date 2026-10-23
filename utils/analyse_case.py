import json
import logging
import os
import re
import allure
from config.config import BASE_URL


@allure.step("1.解析请求数据")
def analyse_case(case):
    # 1. 基础数据组装
    request_data = {
        "method": case.get("method"),
        "url": BASE_URL + case.get("path", ""),
        "headers": case.get("headers"),
        "params": case.get("params"),
        "data": case.get("data"),
        "json": case.get("json"),
    }

    # 2. 显式读取文件二进制流
    files_config = case.get("files")
    processed_files = {}
    if files_config:
        try:
            for key, file_path in files_config.items():
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"框架报错：测试文件不存在 -> {file_path}")
                processed_files[key] = open(file_path, "rb")
            request_data["files"] = processed_files
        except Exception as e:
            # 如果在打开后续文件时崩溃，把前面已经打开的文件关掉
            for f in processed_files.values():
                f.close()
            raise e  #把异常重新抛出去，让用例失败

    # 3. 参数清洗：剔除值为 None 的字段
    clean_request_data = {k: v for k, v in request_data.items() if v is not None}

    # 4. 日志与 Allure 记录（处理文件对象，防止打印出内存地址）
    log_data = clean_request_data.copy()
    if "files" in log_data:
        log_data["files"] = {k: f"<File: {v.name}>" for k, v in log_data["files"].items()}

    logging.info(f'1.解析请求数据，请求数据为: {log_data}')


    return clean_request_data


def str_to_obj(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value

# 替换全局变量
def replace_vars(data, context):
    # 1. 字典
    if isinstance(data, dict):
        return {k: replace_vars(v, context) for k, v in data.items()}
    # 2. 列表
    elif isinstance(data, list):
        return [replace_vars(i, context) for i in data]
    # 3. 字符串
    elif isinstance(data, str):
        full_match = re.fullmatch(r"\$\{(\w+)\}", data)
        if full_match:
            key = full_match.group(1)
            if key in context:
                return context[key]  # 保留原始类型
            else:
                raise ValueError(f"变量替换失败：在全局上下文中找不到变量 '{key}'")

        def repl(match):
            key = match.group(1)
            if key in context:
                return str(context[key])
            else:
                raise ValueError(f"变量替换失败：在全局上下文中找不到变量 '{key}'")

        return re.sub(r"\$\{(\w+)\}", repl, data)
    # 4. 其他
    else:
        return data