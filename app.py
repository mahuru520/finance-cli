import streamlit as st
from db import init_db
from pages import add, list, delete, stats

st.set_page_config(page_title="记账工具", layout="wide")

init_db()

page = st.sidebar.radio("导航", ["添加账目", "查看列表", "删除账目", "分类统计"])

pages = {
    "添加账目": add,
    "查看列表": list,
    "删除账目": delete,
    "分类统计": stats,
}

pages[page].render()
