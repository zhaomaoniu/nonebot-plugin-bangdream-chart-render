import os
import csv
import json
import aiohttp
import pandas as pd

from fuzzywuzzy import process
from nonebot.log import logger


async def fetch_data(url: str, file_path: str, file_name: str, use_cache: bool = True) -> dict: 
    # 检查缓存文件是否存在
    if os.path.exists(file_path + file_name) and use_cache:
        with open(file_path + file_name, "r", encoding="UTF-8") as file:
            cached_data = json.load(file)
        return cached_data

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                json_data = await response.json(encoding="UTF-8")

                # 保存到缓存文件
                os.makedirs(file_path, exist_ok=True)
                with open(file_path + file_name, "w", encoding="UTF-8") as file:
                    file.write(json.dumps(json_data, indent=4))

                return json_data
            else:
                logger.error(f"{response.status}")
                raise ValueError("获取谱面信息失败")

def read_csv_to_dict(file_path):
    data_dict = {}
    with open(file_path, 'r', encoding="UTF-8") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        for row in csv_reader:
            key = row[0]  # 使用第一列作为字典的键
            values = row[1:]  # 使用剩余列作为字典的值
            if key is not None and values is not None and key != "":
                data_dict[key] = [value for value in values if value != '']
    result = {}
    for key, values in data_dict.items():
        new_values = []
        for value in values:
            new_values.extend(value.split(','))
        result[key] = new_values
    return result

def read_xlsx_to_dict(file_path):
    data_dict = {}
    df = pd.read_excel(file_path, sheet_name='工作表1')
    columns = df.columns.tolist()
    for index, row in df.iterrows():
        key = row[columns[0]]  # 使用第一列作为字典的键
        values = row[columns[1:]]  # 使用剩余列作为字典的值
        if pd.notnull(key) and pd.notnull(values).any() and key != "":
            data_dict[str(int(key))] = [value for value in values if pd.notnull(value)]
    result = {}
    for key, values in data_dict.items():
        new_values = []
        for value in values:
            new_values.extend(str(value).split(','))
        result[key] = new_values
    return result

def fuzzy_match(query, dictionary):
    max_ratio = 0
    matched_key = None
    for key, value in dictionary.items():
        catch, ratio = process.extractOne(query, value)
        if ratio > max_ratio:
            max_ratio = ratio
            matched_key = key
    return matched_key