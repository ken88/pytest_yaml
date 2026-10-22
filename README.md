# pytestDemo

本项目实现接口自动化的技术选型：**Python+Requests+Pytest+YAML+Allure** ，主要是针对本人的一个接口项目来开展的，通过 Python+Requests 来发送和处理HTTP协议的请求接口，使用 Pytest 作为测试执行器，使用 YAML 来管理测试数据，使用 Allure 来生成测试报告。


## 项目说明

本项目在实现过程中，把整个项目拆分成请求方法封装、HTTP接口封装、关键字封装、测试用例等模块。

首先利用Python把HTTP接口封装成Python接口，接着把这些Python接口组装成一个个的关键字，再把关键字组装成测试用例，而测试数据则通过YAML文件进行统一管理，然后再通过Pytest测试执行器来运行这些脚本，并结合Allure输出测试报告。

当然，如果感兴趣的话，还可以再对接口自动化进行Jenkins持续集成。

## 项目部署

首先，下载项目源码后，在根目录下找到 ```requirements.txt``` 文件，然后通过 pip 工具安装 requirements.txt 依赖，执行命令：

```
pip3 install -r requirements.txt
```

接着，修改 ```config/config.py``` 配置文件，在Windows环境下，安装相应依赖之后，在命令行窗口执行命令：

```
pytest
```

## 项目结构


conftest.py 可以存放夹具，用于测试用例执行前后的数据初始化和销毁
- data ====>> 用于保存 excel/yaml 格式的测试用例
- testcases ====>> 测试用例
- utils ====>> 用于保存各种工具类/函数，例如读取excel/yaml 文件用到的工具函数
- config ====>> 用于保存一些配置信息，例如BASE_URL，数据库配置信息等
- file ====>> 涉及文件上传类接口时，可以用于保存需要上传的文件
- log ====>> 用于保存日志
- report ====>> 用于生成allure测试报告
- pytest.ini ====>> pytest配置文件
- requirements.txt ====>> 相关依赖包文件
- run.py ====>> 运行入口

## 关键字封装说明


## 测试报告效果展示



![img_1.png](img_1.png)![img_2.png](img_2.png)