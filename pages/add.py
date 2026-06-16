import streamlit as st
from db import add_record, CATEGORIES


def render():
    st.header("添加账目")

    with st.form("add_record"):
        type_ = st.radio("类型", ["支出", "收入"], horizontal=True)
        amount = st.number_input("金额", min_value=0.01, step=0.01, format="%.2f")
        category = st.selectbox("分类", CATEGORIES)
        date = st.date_input("日期")
        note = st.text_input("备注")

        submitted = st.form_submit_button("添加")
        if submitted:
            signed_amount = amount if type_ == "收入" else -amount
            add_record(signed_amount, category, str(date), note)
            st.success(f"已添加：{type_} ¥{amount:.2f} - {category}")
