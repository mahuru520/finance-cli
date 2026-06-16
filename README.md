# finance-cli

个人记账 Web 工具，基于 Python + Streamlit + SQLite3。

## 功能

- **添加账目** — 收入/支出、金额、分类、日期、备注
- **查看列表** — 按月份和分类筛选，表格展示
- **删除账目** — 输入 ID，删除前显示记录摘要
- **分类统计** — 柱状图 + 总收入/总支出/净额 + 每分类统计表

## 预设分类

餐饮、交通、购物、娱乐、居住、其他

## 快速开始

```bash
# 创建 conda 虚拟环境
conda create -n finance python=3.12 -y
conda activate finance

# 安装依赖
pip install -r requirements.txt

# 启动
streamlit run app.py
```

启动后浏览器访问 `http://localhost:8501`。

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
```

## 数据存储

SQLite3 文件 `finance.db`，运行时自动创建。支出金额存储为负数。
