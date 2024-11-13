import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

st.set_page_config(
    page_title="Proyek Analisis Data dengan Python",
    page_icon=""
)

st.title("Gardasvara Mistortoify | ML-45")
merged_df = pd.read_csv('dashboard/all_data.csv')

# Pertanyaan 1
state_sales_df = merged_df.groupby(by="customer_state").agg({
    "order_id": "nunique",  
    "price": "sum"       
}).reset_index()

state_sales_df.rename(columns={
    "order_id": "order_count",
    "price": "revenue"
}, inplace=True)

st.title("Analisis Performa Penjualan dan Revenue per Wilayah")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.barplot(
        x="revenue",
        y="customer_state",
        data=state_sales_df.sort_values(by="revenue", ascending=False),
        color="#fcba03"
    )
    plt.title("Total Revenue per State", loc="center", fontsize=14)
    plt.ylabel(None)
    plt.xlabel("Total Revenue", fontsize=10)
    plt.tick_params(axis='y', labelsize=8)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.barplot(
        x="order_count",
        y="customer_state",
        data=state_sales_df.sort_values(by="order_count", ascending=False),
        color="#fcba03"
    )
    plt.title("Total Number of Orders per State", loc="center", fontsize=14)
    plt.ylabel(None)
    plt.xlabel("Total Orders", fontsize=10)
    plt.tick_params(axis='y', labelsize=8)
    st.pyplot(fig)

# Pertanyaan 2
product_sales_by_state = merged_df.groupby(['seller_state', 'product_category_name_english']).agg({'order_item_id': 'count'}).reset_index()
product_sales_by_state.rename(columns={'order_item_id': 'product_sales_count'}, inplace=True)

def top_products_by_state(seller_state):
    return product_sales_by_state[product_sales_by_state['seller_state'] == seller_state].sort_values(by='product_sales_count', ascending=False).head(10)

st.title('Analisis Produk Paling Populer per Wilayah')

state_options = product_sales_by_state['seller_state'].unique()
selected_state = st.selectbox('Pilih Wilayah', state_options)

top_products = top_products_by_state(selected_state)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='product_sales_count', 
    y='product_category_name_english', 
    data=top_products, 
    color='Green'
)
plt.title(f'Top 10 Best Selling Products in {selected_state}', loc='center', fontsize=18)
plt.ylabel(None)
plt.xlabel('Number of Sales', fontsize=12)
plt.tick_params(axis='y', labelsize=10)
st.pyplot(fig)

# Pertanyaan 3
merged_df['order_purchase_timestamp'] = pd.to_datetime(merged_df['order_purchase_timestamp'])

monthly_sales_df = merged_df.resample('M', on='order_purchase_timestamp').agg({
    'order_id': 'nunique',  
    'price': 'sum'       
}).reset_index()

monthly_sales_df['order_purchase_timestamp'] = monthly_sales_df['order_purchase_timestamp'].dt.strftime('%B %Y')
monthly_sales_df.rename(columns={'order_id': 'order_count', 'price': 'total_sales'}, inplace=True)

st.title("Pola Penjualan dan Jumlah Pesanan Bulanan")

fig, axs = plt.subplots(1, 2, figsize=(16, 6))  

sns.barplot(
    x="order_purchase_timestamp",
    y="total_sales",
    hue="order_purchase_timestamp",
    data=monthly_sales_df,
    color="#0377fc",  
    legend=False,
    ax=axs[0]
)
axs[0].set_title("Total Sales per Month", loc="center", fontsize=14)
axs[0].tick_params(axis='x', rotation=45, labelsize=10)
axs[0].tick_params(axis='y', labelsize=10)
axs[0].set_ylabel("Total Sales", fontsize=12)
axs[0].set_xlabel("Month", fontsize=12)

sns.barplot(
    x="order_purchase_timestamp",
    y="order_count",
    hue="order_purchase_timestamp",
    data=monthly_sales_df,
    color="#0377fc",  
    legend=False,
    ax=axs[1]
)
axs[1].set_title("Order Count per Month", loc="center", fontsize=14)
axs[1].tick_params(axis='x', rotation=45, labelsize=10)
axs[1].tick_params(axis='y', labelsize=10)
axs[1].set_ylabel("Order Count", fontsize=12)
axs[1].set_xlabel("Month", fontsize=12)

plt.suptitle("Monthly Sales Trends", fontsize=16)  
st.pyplot(fig)

# Pertanyaan 4
from datetime import datetime

merged_df['order_purchase_timestamp'] = pd.to_datetime(merged_df['order_purchase_timestamp'])

def analyze_by_state(start_date, end_date):
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date = datetime.combine(end_date, datetime.max.time())
    
    filtered_data = merged_df[(merged_df['order_purchase_timestamp'] >= start_date) & (merged_df['order_purchase_timestamp'] <= end_date)]
    
    state_sales_df = filtered_data.groupby('customer_state').agg({
        'order_id': 'nunique',
        'price': 'sum'
    }).reset_index()
    
    return state_sales_df

st.title("Analisis Penjualan Rendah per Wilayah")

start_date = st.date_input("Tanggal Mulai", value=pd.to_datetime('2016-01-01').date())
end_date = st.date_input("Tanggal Akhir", value=pd.to_datetime('2018-12-31').date())

state_sales_df = analyze_by_state(start_date, end_date)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="price",
    y="customer_state",
    data=state_sales_df.sort_values(by="price", ascending=True).head(10),
    color="red",
    dodge=False
)
plt.title("Top 10 States with Lowest Sales Revenue", fontsize=18)
plt.ylabel(None)
plt.xlabel("Sales Revenue", fontsize=12)
plt.tick_params(axis='y', labelsize=10)
st.pyplot(fig)
