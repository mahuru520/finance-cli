import streamlit as st
import pandas as pd
from datetime import date
from db import query_records, CATEGORIES


def render():
    st.header("查看列表")

    col1, col2 = st.columns(2)
    with col1:
        selected_month = st.date_input("月份筛选", value=date.today(), format="YYYY-MM")
        year_month = selected_month.strftime("%Y-%m") if selected_month else None
    with col2:
        selected_categories = st.multiselect("分类筛选", CATEGORIES)

    records = query_records(
        year_month=year_month if year_month else None,
        categories=selected_categories if selected_categories else None,
    )

    if not records:
        st.info("暂无记录")
        return

    df = pd.DataFrame(records)
    df["amount"] = df["amount"].apply(lambda x: f"{'收入' if x > 0 else '支出'} ¥{abs(x):.2f}")
    df.rename(columns={"amount": "金额", "category": "分类", "date": "日期", "note": "备注"}, inplace=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
