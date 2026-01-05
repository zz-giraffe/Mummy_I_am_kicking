import streamlit as st
import pandas as pd
from datetime import datetime
import random
import os

st.set_page_config(page_title="Baby Kick Tracker", page_icon="👶")

# --- 隐藏 Streamlit 默认的菜单和页脚 ---
hide_st_style = """
            <style>
            /* 1. 基础隐藏：菜单、头部、底部 */
            #MainMenu {visibility: hidden; display: none !important;}
            header {visibility: hidden; display: none !important;}
            footer {visibility: hidden; display: none !important;}
            
            /* 2. 🎯 核心狙击：隐藏那个红色的皇冠按钮 (Status Widget) */
            [data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}
            
            /* 3. 补充隐藏：隐藏工具栏和装饰元素 */
            [data-testid="stToolbar"] {visibility: hidden; display: none !important;}
            [data-testid="stDecoration"] {visibility: hidden; display: none !important;}
            
            /* 4. 调整布局：去掉顶部和底部的多余空白 */
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 0rem !important;
            }
            
            /* 5. 如果它还没死，隐藏右下角所有 fixed 定位的 viewer badge */
            div[class^='viewerBadge_'] {display: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 2. 定义数据文件和可爱的消息库 ---
DATA_FILE = "kick_log.csv"
MESSAGES = [
    "I love mummy! ❤️", 
    "I love daddy! 💙", 
    "I am a cute baby! 👶",
    "Hello world! 🌍", 
    "Strong kick! 💪", 
    "Did you feel that? ✨",
    "Playing soccer inside! ⚽", 
    "Sending love! 💌"
]

# --- 3. 函数：加载和保存数据 ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Timestamp", "Message", "Date", "Time"])

def save_kick(msg):
    now = datetime.now()
    new_data = pd.DataFrame({
        "Timestamp": [now],
        "Message": [msg],
        "Date": [now.date()],
        "Time": [now.strftime("%H:%M:%S")]
    })
    # 如果文件不存在就写入表头，否则追加模式
    new_data.to_csv(DATA_FILE, mode='a', header=not os.path.exists(DATA_FILE), index=False)

# --- 4. App 界面设计 ---
st.title("👶 Baby Kick Tracker")
st.write("Click the button when you feel a kick!")

# 为了让按钮在手机上更好按，我们要把它居中
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 这是一个红色的大按钮
    if st.button("👣 KICK!", width='stretch', type="primary"):
        # 核心逻辑：随机选一句话 -> 保存 -> 撒花庆祝
        selected_msg = random.choice(MESSAGES)
        save_kick(selected_msg)
        
        st.balloons()  # 🎈 动画效果
        st.success(f"**Baby says:** {selected_msg}")

# --- 5. 数据展示区 ---
st.divider()
st.subheader("📝 Activity Log")

df = load_data()

if not df.empty:
    # 按照时间倒序排列，最新的在最上面
    df = df.sort_values(by="Timestamp", ascending=False)
    
    # 简单的统计
    st.markdown(f"**Total Kicks:** {len(df)}")
    
    # 展示数据表
    st.dataframe(df[["Date", "Time", "Message"]], width='stretch')
else:
    st.info("Waiting for the first kick...")