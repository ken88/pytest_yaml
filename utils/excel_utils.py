import openpyxl

from config.config import EXCEL_FILE, SHETTL_NAME


def read_excel():
    # 打开 excel文件
    workbook = openpyxl.load_workbook(EXCEL_FILE)  # 参数传文件路径

    # 选择表
    worksheet = workbook[SHETTL_NAME]
    # 读数据操作，zip()函数的作用可以把可迭代对象打包成一个个元组
    # 思路，因为dict(zip(key，value))可以把读取到的数据变成字典类型，所以只需分别取出key行，和value行即可
    # print(dict(zip([1, 2, 3, 4], ["a", "b", "c"])))

    keys = [cell.value for cell in worksheet[2]] # 拿key行，也就是表的第二行,生成一个key的列表

    data = [] # 空列表，用于组装字典
    for row in worksheet.iter_rows(min_row=3, values_only=True): # 从第三行开始拿，只返回值
        # print(row) # 打印value列表
        # print(dict(zip(keys, row)))
        dict_data = dict(zip(keys, row))
        if dict_data["is_true"]:
            data.append(dict_data)

    # print(data) # 打印拿到的所有数据

    # 关闭excel文件
    workbook.close()

    return data

def str_to_obj(value):
    # 字符串转对象，如果不是字符串返回None
    if isinstance(value, str):
        # 优先json.loads，更安全；如果需要兼容python字典写法再用eval
        # return json.loads(value)
        return eval(value)
    return None