import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Page Configuration (ตั้งค่าหน้าจอ Web App)
st.set_page_config(page_title="YRC GHG Dashboard", layout="wide", page_icon="🌍")

# 2. Custom CSS สำหรับตกแต่งสีสันและกล่องข้อความ
st.markdown("""
<style>
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 4px solid #4CAF50;
    }
    .metric-title {
        color: #666;
        font-size: 14px;
        font-weight: bold;
    }
    .metric-value {
        color: #333;
        font-size: 24px;
        font-weight: bold;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. โหลดข้อมูล GHG ของบริษัท วาย.อาร์.ซี. เท็กซ์ไทล์ จำกัด
@st.cache_data
def load_data():
    # ข้อมูลรวมจากการประเมินคาร์บอนฟุตพริ้นท์ ปี 2024 และ 2025
    data = {
        'Year': [2024, 2024, 2024, 2025, 2025, 2025],
        'Scope': ['Scope 1', 'Scope 2', 'Scope 3', 'Scope 1', 'Scope 2', 'Scope 3'],
        'Emission_tCO2e': [3648.71, 33866.63, 280666.61, 3527.67, 28956.57, 237284.88]
    }
    return pd.DataFrame(data)

df = load_data()

# 4. Header และระบบ Filter
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🖥️ Dashboard Overview")
with col2:
    st.write("")
    st.write("")
    # ฟังก์ชันปุ่ม Export ไฟล์ Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='GHG_Data', index=False)
    
    st.download_button(
        label="📥 Export to Excel",
        data=buffer.getvalue(),
        file_name="YRC_GHG_Report_Export.xlsx",
        mime="application/vnd.ms-excel"
    )

st.markdown("##### ปีรายงาน")
selected_year = st.selectbox("เลือกปีที่ต้องการแสดงผล", sorted(df['Year'].unique(), reverse=True))

# กรองข้อมูลตามปีที่เลือก
df_filtered = df[df['Year'] == selected_year]

st.markdown("---")

# 5. ส่วนแสดงตัวเลขสรุป (KPI Cards)
total_emission = df_filtered['Emission_tCO2e'].sum()
scope1_emission = df_filtered[df_filtered['Scope'] == 'Scope 1']['Emission_tCO2e'].sum()
scope2_emission = df_filtered[df_filtered['Scope'] == 'Scope 2']['Emission_tCO2e'].sum()
scope3_emission = df_filtered[df_filtered['Scope'] == 'Scope 3']['Emission_tCO2e'].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">⏱️ Total Emission</div><div class="metric-value">{total_emission:,.0f} tCO2e</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card" style="border-top-color:#2196F3;"><div class="metric-title">🏭 Scope 1</div><div class="metric-value">{scope1_emission:,.0f} tCO2e</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card" style="border-top-color:#FF9800;"><div class="metric-title">⚡ Scope 2</div><div class="metric-value">{scope2_emission:,.0f} tCO2e</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card" style="border-top-color:#9C27B0;"><div class="metric-title">✈️ Scope 3</div><div class="metric-value">{scope3_emission:,.0f} tCO2e</div></div>', unsafe_allow_html=True)

st.write("") 
st.write("")

# 6. ส่วนแสดงกราฟ 
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("**เปรียบเทียบการปล่อยก๊าซเรือนกระจกแต่ละ Scope**")
    fig_bar = px.bar(
        df_filtered, 
        x='Scope', 
        y='Emission_tCO2e', 
        color='Scope',
        color_discrete_map={'Scope 1': '#2196F3', 'Scope 2': '#FF9800', 'Scope 3': '#9C27B0'}
    )
    fig_bar.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart2:
    st.markdown("**สัดส่วนการปล่อยก๊าซเรือนกระจก**")
    fig_pie = px.pie(
        df_filtered, 
        values='Emission_tCO2e', 
        names='Scope',
        hole=0.4, # Donut Chart
        color='Scope',
        color_discrete_map={'Scope 1': '#2196F3', 'Scope 2': '#FF9800', 'Scope 3': '#9C27B0'}
    )
    st.plotly_chart(fig_pie, use_container_width=True)
