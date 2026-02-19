import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="기후변화 탐사선", layout="wide")

# ✅ 해결책 1: 데이터를 캐시에 박제 (값이 변하지 않게 함)
@st.cache_data
def get_fixed_data():
    # 난수 시드를 고정하여 매번 같은 값이 나오게 함
    np.random.seed(42) 
    years = np.repeat(range(2000, 2025), 5)
    data = pd.DataFrame({
        '연도': years,
        '평균기온': np.linspace(12.0, 15.5, len(years)) + np.random.normal(0, 0.2, len(years)),
        '발견횟수': np.linspace(100, 20, len(years)) + np.random.normal(0, 5, len(years)),
        'lat': np.random.uniform(35.0, 38.0, len(years)),
        'lon': np.random.uniform(126.5, 129.0, len(years))
    })
    return data

df = get_fixed_data()

st.title("🌡️ 기후변화에 따른 생물 종 분포 변화")

# 사이드바
selected_year = st.sidebar.slider("관찰 연도 선택", 2000, 2024, 2013)

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📈 {selected_year}년 데이터 추이")
    fig = px.line(df, x='연도', y=['평균기온', '발견횟수'])
    fig.add_vline(x=selected_year, line_dash="dash", line_color="red")
    # ✅ 해결책 2: Plotly 정적 출력 (깜빡임 감소)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.subheader(f"📍 {selected_year}년 발견 위치")
    filtered_df = df[df['연도'] == selected_year]
    
    # 지도를 함수 밖에서 정의하지 않고 필요할 때만 생성
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    for _, row in filtered_df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=8, color='blue', fill=True
        ).add_to(m)
    
    # ✅ 해결책 3: 'returned_objects'를 비워서 불필요한 재실행 방지
    st_folium(m, width=700, height=400, key="main_map", returned_objects=[])
