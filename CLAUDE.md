# CLAUDE.md — finance-cli 项目指南

## 项目概述

个人记账 Web 工具，技术栈：Python + Streamlit + SQLite3。

## 项目结构

```
finance-cli/
  app.py              # 入口：Streamlit 配置 + sidebar 导航 + 页面路由
  db.py               # 数据库层：连接、建表、CRUD 函数
  pages/
    add.py            # 添加账目页面
    list.py           # 查看列表页面
    delete.py         # 删除账目页面
    stats.py          # 分类统计页面
  requirements.txt    # 依赖声明
  .gitignore
```

- `db.py`：纯数据逻辑，不依赖 Streamlit
- `pages/*.py`：纯 UI 层，调用 `db.py` 的函数
- `app.py`：入口文件，sidebar 导航 + 调用各页面 render 函数

## 数据库

SQLite3 文件 `finance.db`，运行时自动创建。

```sql
CREATE TABLE IF NOT EXISTS records (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    amount  REAL NOT NULL,    -- 正数=收入，负数=支出
    category TEXT NOT NULL,   -- 餐饮、交通、购物、娱乐、居住、其他
    date    TEXT NOT NULL,    -- YYYY-MM-DD
    note    TEXT DEFAULT ''
);
```

## 功能

1. **添加账目**：收入/支出(radio) + 金额 + 分类(selectbox) + 日期 + 备注，支出自动存负数
2. **查看列表**：按月份+分类筛选，dataframe 展示
3. **删除账目**：输入 ID 删除
4. **分类统计**：柱状图 + 总收入/总支出/净额 + 每分类统计表

## 运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 编码约定

- 模块职责单一，不跨层调用（UI 不直接写 SQL）
- 分类硬编码 6 个，不做成可配置
- SQLite 连接使用 `with` 上下文管理器
