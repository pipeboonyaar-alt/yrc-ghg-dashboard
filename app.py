import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="YRC GHG Dashboard", layout="wide", page_icon="🌍")

# 2. ตกแต่งสีสันกล่องข้อความ
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

# 3. โหลดข้อมูลดิบแบบละเอียดของปี 2024 และ 2025
@st.cache_data
def load_data():
    csv_data = """Year,Scope,Activity_Source,Emission_tCO2e
2024,Scope 1,1.1 Diesel Stationary,4.21
2024,Scope 1,1.2 Diesel Mobile combustion (on road),133.62
2024,Scope 1,1.3 Diesel Mobile combustion (off road),352.80
2024,Scope 1,1.4 LPG,7.21
2024,Scope 1,1.5 Refrigerant R-32,110.32
2024,Scope 1,1.5 Refrigerant R-410,70.73
2024,Scope 1,1.5 Refrigerant R-134A,18.64
2024,Scope 1,1.6 ถังดับเพลิง Fire Extinguishers,0.14
2024,Scope 1,1.7 ปริมาณของเสียจากห้องน้ำ,349.05
2024,Scope 1,1.8 ปริมาณน้ำเสียจากกระบวนการผลิต,1.93
2024,Scope 1,1.10 ปริมาณ Biomass (Palm Shell),1838.23
2024,Scope 1,1.10 ปริมาณ Biomass (Saw Dust),674.43
2024,Scope 1,1.11 ปริมาณน้ำมันเบนซินที่มีบิลมาเบิก,55.57
2024,Scope 1,1.12 ปริมาณน้ำมันดีเซลที่มีบิลมาเบิก,31.84
2024,Scope 2,2.1 Electricity PEA (Location-Based),36766.05
2024,Scope 3,3.1 การขนส่งของวัตถุดิบ เส้นด้าย และอื่นๆ,115.24
2024,Scope 3,3.2 ข้อมูลการเดินทางติดต่อธุรกิจ,16.81
2024,Scope 3,3.3 การเดินทางมาทำงานของพนักงาน,1878.63
2024,Scope 3,3.4 การขนส่งสินค้าไปยังลูกค้า,44.35
2024,Scope 3,3.5 การขนส่ง Waste ออกไปกำจัด,178.35
2024,Scope 3,4.1 ปริมาณเส้นด้าย,96085.06
2024,Scope 3,4.2 ปริมาณสี,356.04
2024,Scope 3,4.3 ปริมาณเคมีสำหรับกระบวนการผลิต,7221.06
2024,Scope 3,4.4 ปริมาณเคมีผลิต Soft RO/บำบัดน้ำเสีย,1283.86
2024,Scope 3,4.5 ปริมาณน้ำประปา,39.46
2024,Scope 3,4.6 น้ำมันเส้นด้าย,16.18
2024,Scope 3,4.7 น้ำมันเข็ม,13.14
2024,Scope 3,4.8 เหล็ก ท่อ Material,142.44
2024,Scope 3,4.9 กระดาษพิมพ์ลาย,275.94
2024,Scope 3,4.10 กระดาษ A3 A4 F14,33.15
2024,Scope 3,4.11 Paper,9.93
2024,Scope 3,4.12 Paper tube และ สายคาด,430.94
2024,Scope 3,4.13 Plastic poly bag,385.28
2024,Scope 3,4.14 ปริมาณขยะทุกชนิด,629.65
2024,Scope 3,4.15 Fuel and Energy related : ไฟฟ้า,7259.07
2024,Scope 3,4.15 Fuel and Energy related : กะลาปาล์ม,19806.94
2024,Scope 3,4.15 Fuel and Energy related : ขี้เลื่อย,1759.52
2024,Scope 3,4.15 Fuel and Energy related : ดีเซล,56.09
2024,Scope 3,4.15 Fuel and Energy related : เบนซีน,7.51
2024,Scope 3,4.15 Fuel and Energy related : LPG,0.99
2024,Scope 3,4.16 Capital goods,2631.86
2024,Scope 3,5.1 Processing of sold products,139989.11
2025,Scope 1,1.1 Diesel Stationary,2.18
2025,Scope 1,1.2 Diesel Mobile combustion (on road),136.28
2025,Scope 1,1.3 Diesel Mobile combustion (off road),343.61
2025,Scope 1,1.4 LPG,4.48
2025,Scope 1,1.5 Refrigerant R-32,160.19
2025,Scope 1,1.5 Refrigerant R-410,130.91
2025,Scope 1,1.5 Refrigerant R-134A,6.64
2025,Scope 1,1.6 ถังดับเพลิง Fire Extinguishers,0.11
2025,Scope 1,1.7 ปริมาณของเสียจากห้องน้ำ,322.73
2025,Scope 1,1.8 ปริมาณน้ำเสียจากกระบวนการผลิต,2.63
2025,Scope 1,1.10 ปริมาณ Biomass (Palm Shell),1871.29
2025,Scope 1,1.10 ปริมาณ Biomass (Saw Dust),469.47
2025,Scope 1,1.11 ปริมาณน้ำมันเบนซินที่มีบิลมาเบิก,49.55
2025,Scope 1,1.12 ปริมาณน้ำมันดีเซลที่มีบิลมาเบิก,27.59
2025,Scope 2,2.1 Electricity PEA - REC (Market-Based),28956.57
2025,Scope 3,3.1 การขนส่งของวัตถุดิบ เส้นด้าย และอื่นๆ,137.51
2025,Scope 3,3.2 ข้อมูลการเดินทางติดต่อธุรกิจ,19.92
2025,Scope 3,3.3 การเดินทางมาทำงานของพนักงาน,1812.43
2025,Scope 3,3.5 การขนส่ง Waste ออกไปกำจัด,79.22
2025,Scope 3,4.1 ปริมาณเส้นด้าย,107212.12
2025,Scope 3,4.2 ปริมาณสี,433.97
2025,Scope 3,4.3 ปริมาณเคมีสำหรับกระบวนการผลิต,8478.53
2025,Scope 3,4.4 ปริมาณเคมีผลิต Soft RO/บำบัดน้ำเสีย,1192.74
2025,Scope 3,4.5 ปริมาณน้ำประปา,37.78
2025,Scope 3,4.6 น้ำมันเส้นด้าย,22.00
2025,Scope 3,4.7 น้ำมันเข็ม,3.53
2025,Scope 3,4.8 เหล็ก ท่อ Material,81.10
2025,Scope 3,4.9 กระดาษพิมพ์ลาย,367.93
2025,Scope 3,4.10 กระดาษ A3 A4 F14,35.90
2025,Scope 3,4.11 Paper,12.36
2025,Scope 3,4.12 Paper tube และ สายคาด,472.77
2025,Scope 3,4.13 Plastic poly bag,409.26
2025,Scope 3,4.14 ปริมาณขยะทุกชนิด,710.04
2025,Scope 3,4.15 Fuel and Energy related : ไฟฟ้า,6395.41
2025,Scope 3,4.15 Fuel and Energy related : กะลาปาล์ม,21052.27
2025,Scope 3,4.15 Fuel and Energy related : ขี้เลื่อย,1880.73
2025,Scope 3,4.15 Fuel and Energy related : ดีเซล,58.32
2025,Scope 3,4.15 Fuel and Energy related : เบนซีน,6.69
2025,Scope 3,4.15 Fuel and Energy related : LPG,0.61
2025,Scope 3,4.16 Capital goods,2152.76
2025,Scope 3,5.1 Processing of sold products,84218.98
"""
    return pd.read_csv(io.StringIO(csv_data))

df = load_data()

# 4. ส่วนหัว (Header) และ Export Button
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🖥️ YRC GHG Dashboard Overview")
with col2:
    st.write("")
    st.write("")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='GHG_Data_Details', index=False)
    
    st.download_button(
        label="📥 Export รายละเอียด (Excel)",
        data=buffer.getvalue(),
        file_name="YRC_GHG_Detailed_Report.xlsx",
        mime="application/vnd.ms-excel"
    )

# ตัวกรองปี (Filter Year)
st.markdown("##### เลือกปีรายงาน")
selected_year = st.selectbox("", sorted(df['Year'].unique(), reverse=True))
df_filtered = df[df['Year'] == selected_year]

st.markdown("---")

# 5. สรุปตัวเลข KPI (แยกตาม Scope)
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

# 6. กราฟภาพรวมแบบกว้างๆ
col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    st.markdown("**เปรียบเทียบการปล่อยก๊าซเรือนกระจกแต่ละ Scope**")
    fig_bar = px.bar(df_filtered, x='Scope', y='Emission_tCO2e', color='Scope',
                     color_discrete_map={'Scope 1': '#2196F3', 'Scope 2': '#FF9800', 'Scope 3': '#9C27B0'})
    fig_bar.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart2:
    st.markdown("**สัดส่วนการปล่อยก๊าซเรือนกระจกรวม**")
    fig_pie = px.pie(df_filtered, values='Emission_tCO2e', names='Scope', hole=0.4,
                     color='Scope', color_discrete_map={'Scope 1': '#2196F3', 'Scope 2': '#FF9800', 'Scope 3': '#9C27B0'})
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# ==========================================
# 7. ส่วนเพิ่มใหม่: เจาะลึกรายละเอียดระดับรายการ (Drill-down Details)
# ==========================================
st.markdown("### 📋 เจาะลึกรายละเอียดแหล่งปล่อยก๊าซเรือนกระจก (Activity Sources)")

col_filter1, col_filter2 = st.columns([1, 2])
with col_filter1:
    selected_scope = st.radio("ดูรายละเอียดเฉพาะ:", ["แสดงทั้งหมด", "Scope 1", "Scope 2", "Scope 3"])

if selected_scope == "แสดงทั้งหมด":
    df_details = df_filtered
else:
    df_details = df_filtered[df_filtered['Scope'] == selected_scope]

col_detail1, col_detail2 = st.columns([1.5, 2])

# กราฟจัดอันดับ Top 10 แหล่งปล่อย
with col_detail2:
    st.markdown(f"**📊 10 อันดับรายการที่ปล่อยก๊าซสูงสุด ({selected_scope})**")
    top10 = df_details.nlargest(10, 'Emission_tCO2e').sort_values(by='Emission_tCO2e', ascending=True)
    fig_top10 = px.bar(top10, x='Emission_tCO2e', y='Activity_Source', orientation='h', 
                       color='Scope', color_discrete_map={'Scope 1': '#2196F3', 'Scope 2': '#FF9800', 'Scope 3': '#9C27B0'})
    fig_top10.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", yaxis_title="")
    st.plotly_chart(fig_top10, use_container_width=True)

# ตารางข้อมูลดิบ
with col_detail1:
    st.markdown("**ตารางสรุปตัวเลขรายกิจกรรม**")
    display_df = df_details[['Activity_Source', 'Emission_tCO2e']].sort_values(by='Emission_tCO2e', ascending=False)
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Activity_Source": st.column_config.TextColumn("รายการ/กิจกรรม"),
            "Emission_tCO2e": st.column_config.NumberColumn("ปริมาณ (tCO2e)", format="%,.2f")
        },
        height=400
    )
