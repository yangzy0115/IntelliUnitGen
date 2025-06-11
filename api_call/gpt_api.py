# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 13:52:37 2025

@author: An Wen
"""

# gpt_api.py
import openai

openai.api_key = input("Please Enter Your API Key: ")

def large_model_response(messages, temperature):
# def large_model_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # 注意这里换成了 gpt-4o
        messages=messages,
        # temperature=0.2,   # 保持生成内容准确、稳定
        temperature=temperature   # 保持生成内容准确、稳定
        # max_tokens=50000
    )
    
    response = response['choices'][0]['message']['content']
    return response

# prompt = '你好'
# messages = [{"role": "user", "content": prompt}]
# ans = large_model_response(messages, 0.5)
# print(ans) 


