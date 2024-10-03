from flask import Flask, request, jsonify, render_template, send_from_directory
from pymongo import MongoClient
from dotenv import load_dotenv
import os

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


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
