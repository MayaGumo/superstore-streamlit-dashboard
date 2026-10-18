import streamlit as st
import pandas as pd
import plotly.express as px


#load and prepare the data
@st.cache_data
def load_data():
    df = pd.read_csv('Superstore.csv',encoding='latin1')

    df['Order Date'] = pd.to_datetime(df['Order Date'],errors='coerce')

    for col in['Sales', 'Profit', 'Quantity']:
        df['col'] = pd.to_numeric(df[col],errors='coerce')

    df =df.dropna(subset=['Sales', 'Profit', 'Quantity','Order Date']) 

    return df

df = load_data()


#Dashboard Title
st.title('Superstore Sales Dashboard')
st.caption('Monitor sales performance, profitability and regional trends')

#Sidebars slicers
st.sidebar.header('Dashboard Filters')

min_date = df['Order Date'].min().date()
max_date = df['Order Date'].max().date()

date_range = st.sidebar.date_input(
    'Order Date Range',
    value = (min_date,max_date),
    min_value = min_date,
    max_value = max_date
)

categories = sorted(df['Category'].dropna().unique())

regions = sorted(df['Region'].dropna().unique())

segments = sorted(df['Segment'].dropna().unique())

selected_categories = st.sidebar.multiselect('Category', categories, default=categories)

selected_regions = st.sidebar.multiselect('Regions', regions, default=regions)

selected_segments = st.sidebar.multiselect('Segments',segments,default=segments)

#Apply filters
filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df['Order Date'].dt.date >= start_date) & (filtered_df['Order Date'].dt.date<= end_date)
    ]

filtered_df = filtered_df[
    filtered_df['Category'].isin(selected_categories)
    &
    filtered_df['Region'].isin(selected_regions)
    &
    filtered_df['Segment'].isin(selected_segments)
]

if filtered_df.empty:
    st.warning('No data matches your selected filters')
#st.stop()

#KPI cards
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_quantity = filtered_df['Quantity'].sum()

profit_margin =(
    total_profit / total_sales *100
    if total_sales != 0 else 0
)

st.subheader ('Performance Overview')

col1, col2, col3, col4 = st.columns(4)

col1.metric('Total Sales', f'${total_sales:,.0f}')
col2.metric('Total Profit', f'${total_profit:.0f}')
col3.metric('Quantity Sold', total_quantity)
col4.metric('Profit Margin',f'{profit_margin:.1f}%')

st.divider()

# Prepare chart data
monthly_sales  = (
    filtered_df.groupby(pd.Grouper(key='Order Date', freq='MS'),as_index=False)['Sales'].sum()
)

category_sales = (
    filtered_df.groupby('Category', as_index=False)['Sales'].sum()
    .sort_values('Sales',ascending=False)
)

subcategory_profit =(
    filtered_df.groupby('Sub-Category', as_index=False)['Profit'].sum()
    .sort_values('Profit', ascending=False)
    )

region_sales = (
    filtered_df.groupby('Region', as_index=False)['Sales'].sum()
    .sort_values('Sales', ascending=False)
)

# Chart 1 : Sales Trend

left,right = st.columns(2, gap= 'large')

with left:
    fig1 = px.line(
        data_frame=monthly_sales,
          x='Order Date', 
          y='Sales', 
          markers=True,
          title='Monthly Sales',
        labels = {
            'Order Date':'Month',
            'Sales': 'Sales($)'
        },
        template= 'plotly_white'
    )
    fig1.update_traces(
        line=dict(width=3),
        hovertemplate=(
            '%{x|%b %y}<br>'
            'Sales: $%{y:,.2f}'
            '<extra></extra>'
        )
    )

    fig1.update_layout(
        height=360,
        margin=dict(l=10, r=10, t=55,b=10),
        xaxis=dict(tickformat='%b %Y'),
        yaxis = dict(tickprefix='$', tickformat=',.0f'),
        showlegend = False
)

st.plotly_chart(
    fig1,use_container_width=True,key='monthly_sales_chart'
)
# Chart 2: sales by category
fig2 = px.bar(
    data_frame=category_sales,
    x='Category',
    y='Sales',
    title='Sales by Category',
    labels={'Category':'Product Category', 'Sales': 'Sales($)'},
    template='plotly_white'
)

fig2.update_layout(
    height=360,
    margin=dict(l=10,r=10,t=55,b=10),
    yaxis=dict(tickprefix="$", tickformat=",.0f"),
    showlegend=False
)

st.plotly_chart(
    fig2,use_container_width=True,
    key="category_sales_chart"
)


# Chart3: Profit by Sub category
fig3 = px.bar(
    data_frame=subcategory_profit.sort_values('Profit', ascending=True),
    x='Profit',
    y='Sub-Category',
    orientation='h',
    title='Profit by Sub-Category',
    labels={'Sub-Category': 'Sub-Category', 'Profit': 'Profit ($)'},
    color='Profit',
    color_continuous_scale='YlGn',  # Yellow-Green gradient color scale matching the style
    template='plotly_white'
)

fig3.update_layout(
    height=480,
    margin=dict(l=10, r=10, t=55, b=10),
    xaxis=dict(tickprefix="$", tickformat=",.0f"),
    yaxis=dict(categoryorder='total ascending'),
    showlegend=False,
    coloraxis_showscale=False  # Hides the color legend bar on the side for a cleaner look
)

st.plotly_chart(
    fig3,
    use_container_width=True,
    key="subcategory_profit_chart"
)


# Chart 4: Sales by Region (Donut Chart)
fig4 = px.pie(
    data_frame=region_sales,
    names='Region',
    values='Sales',
    title='Sales by Region',
    hole=0.4,  # Creates the donut hole in the center
    template='plotly_white'
)

fig4.update_traces(
    textinfo='percent+label',  # Shows both the region name and percentage
    textposition='inside'
)

fig4.update_layout(
    height=360,
    margin=dict(l=10, r=10, t=55, b=10),
    showlegend=False
)

st.plotly_chart(
    fig4,
    use_container_width=True,
    key="region_sales_chart"
)

with st.expander("View Filtered Data"):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

st.caption(
    f"Showing {len(filtered_df):,} records "
    f"from {filtered_df['Order Date'].min():%d %b %Y} "
    f"to {filtered_df['Order Date'].max():%d %b %Y}."
)