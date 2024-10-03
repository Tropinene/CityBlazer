from flask import Flask, request, jsonify, render_template, send_from_directory
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import random

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
    cities = request.json.get('cities', [])
    print(f"[*] Get city name. {cities}")

    if not cities:
        return jsonify({"[Error]": "城市名称不能为空"}), 400

    # 查找所有城市的坐标
    coordinates_data = []
    for city_name in cities:
        city = collection.find_one({"name": city_name})
        if city:
            coordinates_data.append({
                "name": city_name,
                "coordinates": city.get("coordinates")
            })
        else:
            coordinates_data.append({
                "name": city_name,
                "coordinates": None
            })
    print(f"[*] Get city coordinates.")
    print(coordinates_data[0])
    return jsonify({"coordinates": coordinates_data}), 200


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
    app.run(host='127.0.0.1', port=5000)
