import streamlit as st
import requests
import pandas as pd

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
        return response.json()
    else:
        st.error("Failed to retrieve data")
        return None

def main():
    st.title("Hong Kong Weather Data")
    
    data = get_weather_data()
    
    if data:
        # 用户输入位置
        location = st.text_input("Enter location to search for temperature:")
        
        if location:
            # 查找并显示温度
            found = False
            for temp in data['temperature']['data']:
                if temp['place'].lower() == location.lower():
                    st.write(f"Location: {temp['place']}, Temperature: {temp['value']}°C")
                    found = True
                    break
            if not found:
                st.write("Location not found.")
        else:
            st.write("Please enter a location to search.")
        
        # 显示所有位置的温度图表
        st.header("Temperature Chart for All Locations")
        temp_data = data['temperature']['data']
        df = pd.DataFrame(temp_data)
        df = df.rename(columns={"place": "Location", "value": "Temperature"})
        st.bar_chart(df.set_index("Location")["Temperature"])

if __name__ == "__main__":
    main()