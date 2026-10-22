import logging
import allure
import requests

@allure.step("2.发起HTTP请求")
def send_http_request(**req_data):
   res = requests.request(**req_data)
   logging.info(f"2.发送HTTP请求，响应文本为:{res.text}")
   return  res