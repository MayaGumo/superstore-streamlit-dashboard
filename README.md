# 📊 Superstore Sales Dashboard

An interactive Streamlit web application for analyzing sales performance, profitability, and regional trends using data from the Superstore dataset. Built with Python, Pandas, Streamlit, and Plotly.

---

## 🚀 Features

- **Interactive Sidebar Filters**:
  - **Date Range Picker**: Filter data dynamically across custom date ranges.
  - **Multi-select Filters**: Filter by Product Category, Region, and Customer Segment.
- **Key Performance Indicators (KPIs)**:
  - Total Sales ($)
  - Total Profit ($)
  - Total Quantity Sold
  - Profit Margin (%)
- **Data Visualizations**:
  - 📈 **Sales Trend**: Monthly sales trend over time (Interactive Line Chart).
  - 📊 **Sales by Category**: Product category performance comparison (Bar Chart).
  - 📉 **Profit by Sub-Category**: Horizontal bar chart sorted by profit with gradient color mapping (`YlGn`).
  - 🍩 **Sales by Region**: Donut chart displaying regional market share with percentage breakdowns.
- **Data Inspection**:
  - **Expandable Data Table**: View and inspect the raw filtered dataset directly within the dashboard.
  - **Record Counter & Date Caption**: Dynamic summaries showing total visible records and date boundaries.

---

## 🛠️ Tech Stack

- **Frontend / App Framework**: [Streamlit](https://streamlit.io/)
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
- **Data Visualization**: [Plotly Express](https://plotly.com/python/plotly-express/)
- **Programming Language**: Python 3.x

---

## 📂 Project Structure

```text
├── Superstore.csv            # Dataset file
├── superstore.py             # Main Streamlit application script
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
