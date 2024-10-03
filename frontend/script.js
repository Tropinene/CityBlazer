const map = L.map('map', {
    center: [39.8283, -98.5795],
    zoom: 5,                       // 初始缩放级别
    minZoom: 5,                   // 最小缩放级别
    maxZoom: 18,                  // 最大缩放级别
    worldCopyJump: true           // 启用世界复制跳跃，防止地图重复
});

// 使用 CartoDB Positron 地图样式
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 20,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
}).addTo(map);

// 处理城市输入并高亮显示
document.getElementById('highlightBtn').addEventListener('click', () => {
    const cityName = document.getElementById('cityInput').value;
    sendCityToBackend(cityName);
});

// 监听回车键事件
document.getElementById('cityInput').addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        const cityName = document.getElementById('cityInput').value;
        sendCityToBackend(cityName);
    }
});

// 发送多个城市名称到后端并接收坐标数据
function sendCityToBackend(cityNames) {
    const url = `http://127.0.0.1:5000/get_coordinates`;
    cityNames = cityNames.split(/\s*,\s*/);

    // 使用 fetch 发送 POST 请求到后端
    fetch(url, {
        method: 'POST',  // 使用 POST 方法
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cities: cityNames })  // 发送城市名称数组
    })
    .then(response => response.json())  // 解析 JSON 响应
    .then(data => {
        if (data.coordinates) {
            // 如果找到了坐标数据，调用高亮显示函数
            data.coordinates.forEach(cityData => {
                highlightCityOnMap(cityData.name, cityData.coordinates);
            });
        } else {
            // 如果没有找到城市，显示错误提示
            console.log('Fail to find data!');
        }
    })
    .catch(error => {
        console.error('[Error]:', error);
        alert('Something failed!');
    });
}

// 高亮显示多个城市
function highlightCityOnMap(cityName, coordinates) {
    // 验证 coordinates 是否是 GeoJSON 格式的多边形
    if (!coordinates || !Array.isArray(coordinates) || coordinates.length === 0) {
        console.error(`[Error] Invalid coordinates for city: ${cityName}`, coordinates);
        return;
    }

    // 如果之前已经有高亮的城市，先移除
    if (window.highlightedLayers && window.highlightedLayers[cityName]) {
        map.removeLayer(window.highlightedLayers[cityName]);
    }

    // 将数据包装成 GeoJSON 格式
    const geojsonData = {
        "type": "Feature",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": coordinates  // 直接使用从后端获取的多边形坐标
        },
        "properties": {
            "name": cityName
        }
    };

    // 使用 L.geoJSON 创建一个新的多边形，并设置样式
    const geojsonLayer = L.geoJSON(geojsonData, {
        style: {
            color: 'blue',       // 多边形边框颜色
            weight: 3,           // 边框宽度
            opacity: 0.7,        // 边框透明度
            fillColor: 'blue',   // 填充颜色
            fillOpacity: 0.3     // 填充透明度
        }
    }).addTo(map);

    // 保存高亮层到全局变量，以便后续移除
    if (!window.highlightedLayers) {
        window.highlightedLayers = {};
    }
    window.highlightedLayers[cityName] = geojsonLayer;

    // 自动调整地图视野，以适应多边形区域
    map.fitBounds(geojsonLayer.getBounds());
}
