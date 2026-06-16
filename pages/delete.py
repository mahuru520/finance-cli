import streamlit as st
from db import delete_record, get_record


def render():
    st.header("删除账目")

    record_id = st.number_input("输入要删除的记录 ID", min_value=1, step=1)

    record = get_record(record_id)
    if record:
        st.write(f"**ID {record_id}**：{record['date']} | {record['category']} | ¥{abs(record['amount']):.2f} | {record['note']}")

    if st.button("删除"):
        if record:
            delete_record(record_id)
            st.success(f"已删除 ID={record_id}")
        else:
            st.error(f"未找到 ID={record_id}")
