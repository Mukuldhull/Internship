import streamlit as st
import pandas as pd
from datetime import date
import uuid                         #universal unique indentifier for invoice number

st.title("Enter Details for Invoice")
invoice_date = date.today()
invoice_num = str(uuid.uuid4().int)[:8]
name = st.text_input('Your Name')
phno = st.number_input('Enter your Phone Number',value=0, step=1)
email = st.text_input('Enter Your Email-ID')
ad = st.text_input('Your Address')
num_items = st.number_input('Number of items', min_value=0, step=1)
data = []
for i in range(num_items):
    item_key = f"item_{i}"
    price_key = f"price_{i}"
    quant_key = f"quant_{i}"
    item = st.text_input('Item', key = item_key)
    price = st.number_input('Price of item', key = price_key, min_value=0)
    quantity = st.number_input('Quantity of item', key = quant_key, min_value=0)
    total = price*quantity
    data.append([item,price,quantity,total])
df = pd.DataFrame(data,columns = ['item','price','quantity','total'])
st.table(df)
stotal = df['total'].sum()
#mop = st.selectbox('Mode of Payement',['Credit Card','Debit Card','UPI'])

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if(st.button('Print Invoice')):
    st.markdown("""
    <style>
    .line-spacing {
        line-height: 0.5;
    }
    </style>
    """, unsafe_allow_html=True)

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    col1, col2 = st.columns(2)
    with col1:
        st.title('Invoice')
    with col2:
        st.markdown(f'##### Invoice Number = {invoice_num}')
        st.markdown(f'##### Invoice Date = {invoice_date}')

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    st.markdown("## company name")
    st.markdown('<p class="line-spacing">xyz street</p>', unsafe_allow_html=True)
    st.markdown('<p class="line-spacing">gurugram, haryana</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="line-spacing">------------------------------------------------------------</p>', unsafe_allow_html=True)
    st.markdown("## Bill To")
    st.markdown(f'<p class="line-spacing">{name}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="line-spacing">{phno}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="line-spacing">{ad}</p>', unsafe_allow_html=True)
    st.table(df)

    col3, col4, col5 = st.columns(3)
    with col5:
        st.markdown(f'####  subtotal = {stotal}')
    with col3:
        st.markdown('## Thank You')
