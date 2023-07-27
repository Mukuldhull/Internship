import streamlit as st
import pandas as pd
from datetime import date
import uuid                         #universal unique indentifier for invoice number
import pymysql
import json  # Import the json module to convert the list to a JSON string

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Establish a connection with your MySQL database
# Create a table if it does not exist in the database

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="mukuldhull",
    database="Invoice"
)

cursor = connection.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS Invoice_Data (id INT AUTO_INCREMENT PRIMARY KEY,Customer_Name VARCHAR(100),Phone_No VARCHAR(20),EmailID VARCHAR(20),Address TEXT,Invoice_Number VARCHAR(20),
                                         Invoice_Date DATETIME,Total_BIll_Amount VARCHAR(20),MOP VARCHAR(100), Feedback VARCHAR(1000), Item_Details VARCHAR(1000)
                                        )
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

st.title("Enter Details for Invoice")
# Get the current date for the invoice
invoice_date = date.today()
# Generate a unique invoice number using UUID
invoice_num = str(uuid.uuid4().int)[:8]
# Get user input for customer details
name = st.text_input('Your Name')
phno = st.text_input('Enter your Phone Number')
email = st.text_input('Enter Your Email-ID')
ad = st.text_area("Billing Address")
# Get the number of items and their details for the invoice
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
# Create a DataFrame from the invoice item data
df = pd.DataFrame(data,columns = ['item','price','quantity','total'])
# Display the invoice item table
st.table(df)
stotal = df['total'].sum()
# Get the mode of payment from the user
mop = st.selectbox('Mode of Payement',['Cash','Credit Card','Debit Card','UPI'])
feedback = st.text_input('Feedback')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# If the "Print Invoice" button is clicked
if(st.button('Print Invoice')):
    # Check if all required fields are filled
    if not name or not phno or not email or not ad or not num_items:
        st.error("Please fill in all the required fields.")
    else:
        # Execute the create table query
        cursor.execute(create_table_query)
        # Convert the data list to a JSON string
        data_json = json.dumps(data)
        # Insert the invoice data into the database
        insert_query = """INSERT INTO Invoice_Data (Customer_Name, Phone_No, EmailID, Address, Invoice_Number, Invoice_Date, Total_Bill_Amount, MOP, Feedback,Item_Details)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (name, phno, email, ad, invoice_num, invoice_date, stotal, mop, feedback, data_json)
        cursor.execute(insert_query, values)
        # Commit the changes and close the connection
        connection.commit()
        cursor.close()
        connection.close()
        
        # Display the invoice details in a formatted manner using Markdown
        st.markdown("""
        <style>
        .line-spacing {
            line-height: 0.5;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.title('Invoice')
        with col2:
            st.markdown(f'##### Invoice Number = {invoice_num}')
            st.markdown(f'##### Invoice Date = {invoice_date}')

        st.markdown("## Transtag Lifecycle pvt. ltd.")
        st.markdown('<p class="line-spacing">A-105, RIDGEWOOD ESTATE</p>', unsafe_allow_html=True)
        st.markdown('<p class="line-spacing"> DLF PHASE IV</p>', unsafe_allow_html=True)
        st.markdown('<p class="line-spacing">GURGAON - 122001</p>', unsafe_allow_html=True)
        st.markdown('<p class="line-spacing">Haryana</p>', unsafe_allow_html=True)
    
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
