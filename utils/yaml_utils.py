import yaml

from config.config import YAML_FILE


def read_yaml():
    # 1、读取原始文本
    with open(YAML_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()
        case_list = yaml.safe_load(raw_text)

        data = []
        for dict_data in case_list:
            if dict_data.get("is_true"):
                data.append(dict_data)
    return data