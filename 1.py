import requests

def get_weather_data():
    # API URL
    url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
    
    # API 参数
    params = {
        "dataType": "rhrread",  # 实时天气数据
        "lang": "en"            # 语言：英文
    }
    
    # 发送请求
    response = requests.get(url, params=params)
    
    # 检查响应状态码
    if response.status_code == 200:
        # 解析 JSON 数据
        data = response.json()
        
        # 获取温度数据的大小
        temperature_size = len(data['temperature']['data'])
        humidity_size = len(data['humidity']['data'])
        
        # 遍历温度数据
        for i in range(temperature_size):
            temperature = data['temperature']['data'][i]['value']
            location = data['temperature']['data'][i]['place']
            print(f"Location: {location}")
            print(f"Temperature: {temperature}°C")
        
        # 遍历湿度数据
        for i in range(humidity_size):
            humidity = data['humidity']['data'][i]['value']
            location = data['humidity']['data'][i]['place']
            print(f"Location: {location}")
            print(f"Humidity: {humidity}%")
        
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    get_weather_data()