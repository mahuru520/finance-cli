import streamlit as st
import pandas as pd
from datetime import date
from db import get_stats


def render():
    st.header("分类统计")

    selected_month = st.date_input("月份筛选", value=date.today(), format="YYYY-MM")
    year_month = selected_month.strftime("%Y-%m") if selected_month else None

    stats = get_stats(year_month=year_month)

    if not stats:
        st.info("暂无数据")
        return

    df = pd.DataFrame(stats)

    # 汇总
    total_income = df["income"].sum()
    total_expense = df["expense"].sum()
    col1, col2, col3 = st.columns(3)
    col1.metric("总收入", f"¥{total_income:.2f}")
    col2.metric("总支出", f"¥{total_expense:.2f}")
    col3.metric("净额", f"¥{total_income - total_expense:.2f}")

    # 柱状图（支出）
    chart_df = df[["category", "expense"]].rename(columns={"category": "分类", "expense": "支出"})
    chart_df = chart_df.set_index("分类")
    st.bar_chart(chart_df)

    # 统计表
    df.rename(columns={"category": "分类", "income": "收入", "expense": "支出", "count": "笔数"}, inplace=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
