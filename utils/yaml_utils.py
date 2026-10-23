import os
import yaml
from config.config import YAML_DIR


def read_yaml():
    all_cases = []

    # 1. 获取文件夹下所有的文件
    if not os.path.exists(YAML_DIR):
        raise FileNotFoundError(f"用例目录不存在: {YAML_DIR}")

    # 2. 过滤出 yaml 文件，并进行排序（保证执行顺序稳定）
    file_list = sorted([f for f in os.listdir(YAML_DIR) if f.endswith(('.yaml', '.yml'))])

    for filename in file_list:
        file_path = os.path.join(YAML_DIR, filename)

        # 3. 读取每个 YAML 文件
        with open(file_path, "r", encoding="utf-8") as f:
            case_list = yaml.safe_load(f)

            # 4. 过滤 is_true 并合并到总列表
            if case_list and isinstance(case_list, list):
                for dict_data in case_list:
                    if dict_data.get("is_true", True):
                        all_cases.append(dict_data)


    return all_cases