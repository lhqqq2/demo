import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def get_weather_data(date):
    # API URL
    url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
    
    # API 参数
    params = {
        "dataType": "rhrread",  # 实时天气数据
        "lang": "en",           # 语言：英文
        "year": date.year,
        "month": date.month,
        "day": date.day
    }
    
    # 发送请求
    response = requests.get(url, params=params)
    
    # 检查响应状态码
    if response.status_code == 200:
        # 解析 JSON 数据
        return response.json()
    else:
        st.error("Failed to retrieve data")
        return None

def main():
    st.title("Hong Kong Weather Data")
    
    # 添加日期选择器
    date = st.date_input("Select a date", datetime.now())
    
    data = get_weather_data(date)
    
    if data:
        # 获取所有地区名称
        locations = [temp['place'] for temp in data['temperature']['data']]
        
        # 添加地区选择器
        selected_location = st.selectbox("Select a location", locations)
        
        # 添加下拉菜单选择天气指标
        metric = st.selectbox("Select a weather metric", ["Temperature", "Humidity", "UV Index"])
        
        # 查找并显示选定地区的天气数据
        found = False
        if metric == "Temperature":
            for temp in data['temperature']['data']:
                if temp['place'] == selected_location:
                    st.write(f"Location: {temp['place']}, Temperature: {temp['value']}°C")
                    found = True
                    break
        elif metric == "Humidity":
            for hum in data['humidity']['data']:
                if hum['place'] == selected_location:
                    st.write(f"Location: {hum['place']}, Humidity: {hum['value']}%")
                    found = True
                    break
        elif metric == "UV Index" and 'uvindex' in data:
            for uv in data['uvindex']['data']:
                if uv['place'] == selected_location:
                    st.write(f"Location: {uv['place']}, UV Index: {uv['value']}")
                    found = True
                    break
        
        if not found:
            st.write("Data not found for the selected location.")
        
        # 显示所有位置的温度图表
        st.header(f"{metric} Chart for All Locations")
        if metric == "Temperature":
            temp_data = data['temperature']['data']
            df = pd.DataFrame(temp_data)
            df = df.rename(columns={"place": "Location", "value": "Temperature"})
            st.bar_chart(df.set_index("Location")["Temperature"])
        elif metric == "Humidity":
            hum_data = data['humidity']['data']
            df = pd.DataFrame(hum_data)
            df = df.rename(columns={"place": "Location", "value": "Humidity"})
            st.bar_chart(df.set_index("Location")["Humidity"])
        elif metric == "UV Index" and 'uvindex' in data:
            uv_data = data['uvindex']['data']
            df = pd.DataFrame(uv_data)
            df = df.rename(columns={"place": "Location", "value": "UV Index"})
            st.bar_chart(df.set_index("Location")["UV Index"])

if __name__ == "__main__":
    main()