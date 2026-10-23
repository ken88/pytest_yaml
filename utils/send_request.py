import logging
import allure
import requests

@allure.step("2.发起HTTP请求")
def send_http_request(**kwargs):
   try:
      # 发送真实请求
      response = requests.request(**kwargs)
      logging.info(f"2.发送HTTP请求，响应文本为:{response.text}")
      return response
   except Exception as e:
      logging.error(f"请求发送失败: {e}")
      raise e
   finally:
      # 发送完毕（无论成功失败），如果参数里有 files，立刻关闭文件！
      files = kwargs.get("files")
      if files:
         for f in files.values():
            if hasattr(f, "close"):
               f.close()