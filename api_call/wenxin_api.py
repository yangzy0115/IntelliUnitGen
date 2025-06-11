# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 13:43:41 2025

@author: An Wen
"""

import requests
import json

# 文心 API Key
CLIENT_ID = input("Please Enter Your CLIENT_ID")
CLIENT_SECRET = input("Please Enter Your CLIENT_SECRET")

# 获取 access_token
def get_access_token():
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    response = requests.get(url)
    result = response.json()
    return result.get("access_token", "")

ACCESS_TOKEN = get_access_token()
if not ACCESS_TOKEN:
    print("获取 access_token 失败，请检查 client_id 和 client_secret")
    exit()

API_URL = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={ACCESS_TOKEN}"

def large_model_response(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    return response.json().get("result", "")
