import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium

# 1. 앱 페이지 설정
st.set_page_config(page_title="기후변화와 생물다양성 탐사선", layout="wide")

st.title("🌡️ 기후변화에 따른 생물 종 분포 변화 관찰")
st.markdown("""
이 앱은 기온 상승에 따라 생물들의 서식지가 어떻게 변하는지 시뮬레이션하고 관찰합니다.
""")

# 2. 가상의 데이터 생성 (실제 데이터 대신 학습용으로 생성)
def load_sample_data():
    data = pd.DataFrame({
        '연도': np.repeat(range(2000, 2025), 5),
        '평균기온': np.linspace(12.0, 15.5, 125) + np.random.normal(0, 0.2, 125),
        '발견횟수': np.linspace(100, 20, 125) + np.random.normal(0, 5, 125), # 온도가 오를수록 줄어드는 종 가정
        'lat': np.random.uniform(35.0, 38.0, 125),
        'lon': np.random.uniform(126.5, 129.0, 125)
    })
    return data

df = load_sample_data()

# 3. 사이드바 - 인터랙션 설정
st.sidebar.header("설정 메뉴")
selected_year = st.sidebar.slider("관찰 연도 선택", 2000, 2024, 2024)
species = st.sidebar.selectbox("관찰 종 선택", ["꿀벌 (기온 민감종)", "등검은말벌 (외래 침입종)"])

# 4. 메인 대시보드 구성
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📈 {selected_year}년 기온 vs 개체수 추이")
    # Plotly를 이용한 인터랙티브 차트
    fig = px.line(df, x='연도', y=['평균기온', '발견횟수'], 
                  title="기온 상승에 따른 발견 빈도 변화")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader(f"📍 {selected_year}년 발견 위치 지도")
    # 선택한 연도의 데이터만 필터링
    filtered_df = df[df['연도'] == selected_year]
    
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    for auth, row in filtered_df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            color='red' if species == "등검은말벌 (외래 침입종)" else 'blue',
            fill=True
        ).add_to(m)
    
    st_folium(m, width=700, height=400)

# 5. 교육용 메시지
st.info(f"""
**💡 관찰 결과:** {selected_year}년 기준으로 기온이 상승함에 따라 해당 종의 발견 횟수가 변화하고 있습니다. 
이는 기후 변화가 생물의 생태 사이클에 직접적인 영향을 미치고 있음을 시사합니다.
""")
