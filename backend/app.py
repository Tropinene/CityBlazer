from flask import Flask, request, jsonify, render_template, send_from_directory
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import random
import time

# 加载环境变量
load_dotenv()

# 获取数据库连接字符串
mongo_uri = os.getenv('MONGO_URI')

# 创建 Flask 应用
app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")

# 连接到 MongoDB
client = MongoClient(mongo_uri)
db = client['US_cities']
collection = db['map']


@app.route('/')
def serve_index():
    return render_template('index.html')


@app.route('/script.js')
def serve_script():
    return send_from_directory('../frontend', 'script.js')


@app.route('/style.css')
def serve_style():
    return send_from_directory('../frontend', 'style.css')


# 查询城市并返回其坐标
@app.route('/get_coordinates', methods=['POST'])
def get_coordinates():
    start_time = time.time()

    # 获取请求的城市名称列表
    cities = request.json.get('cities', [])
    # 查询数据库中的城市坐标
    city_coordinates = []

    for city in cities:
        city_data = collection.find_one({"name": city}, {"_id": 0, "name": 1, "coordinates": 1})
        if city_data:
            city_coordinates.append({
                "name": city_data["name"],
                "coordinates": city_data["coordinates"]
            })

    end_time = time.time()
    total_time = end_time - start_time
    print(f"[INFO] Time taken to process the coordinates: {total_time:.4f} seconds")

    # 返回所有城市的坐标
    return jsonify({"coordinates": city_coordinates})


# 随机生成城市名的函数
def randomGenCities(count):
    # 获取所有城市的名称
    city_names = list(collection.find({}, {"_id": 0, "name": 1}))

    # 如果数据库中的城市数目少于请求的数量，返回所有城市
    if count > len(city_names):
        count = len(city_names)

    # 随机选择 count 个城市
    random_cities = random.sample(city_names, count)

    # 返回城市名称列表
    return [city['name'] for city in random_cities]


# 定义 API 路由来获取随机城市名
@app.route('/random_cities/<int:count>', methods=['GET'])
def get_random_cities(count):
    cities = randomGenCities(count)
    return jsonify(cities)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3000)
