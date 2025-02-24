import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import plotly.express as px

st.title( ":blue[Expense Tracker]")
st.markdown("#### :blue[Personal Expense Tracker is a project to analyse the expenses made by a person. Provide expense analysis based on various criteria to help understand the Finance Management in a better manner.]")  

mydb = pymysql.connect(
   host = "localhost",
   user = "root",
   password = "123456789",
   database= "expense_database",
   autocommit = True)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM expense")
data = mycursor.fetchall()
expensedf = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])

# Create tab titles
tab1, tab2, tab3 = st.tabs(["📊 Visualization"," 📈 Data Analysis", "🗃 Model Insights" ]) 

css = '''
    <style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.5rem;
    }
    </style>
    '''
st.markdown(css, unsafe_allow_html=True)

# Content for Tab 1
with tab1:
   st.write("###### Visualization of the analysis done on the Expense Tracker")
   df_grp1 = expensedf.groupby(['Category'])['Amount'].sum().reset_index()
   df_grp1 = df_grp1.sort_values(['Amount']).reset_index(drop=True)
   fig, ax = plt.subplots(figsize=(4,2))
   sns.barplot(df_grp1, x = 'Amount', y = 'Category', width = 0.3, ax=ax)
   plt.title('Total amount spent across all categories', fontsize=8)
   plt.xlabel('Total Amount', fontsize=8)
   plt.ylabel('Category', fontsize=8)
   plt.xticks(fontsize=8)
   plt.yticks(fontsize=8)   
   st.pyplot(fig)
     
   
   expensedf['Date'] = pd.to_datetime(expensedf['Date'])
   expensedf['Month'] = expensedf['Date'].dt.month
   expensedf['Month'] = expensedf['Date'].dt.strftime('%B')
   df_grp2 = expensedf.groupby(['Month'])['Amount'].sum().reset_index()
   df_grp2 = df_grp2.sort_values(['Amount']).reset_index(drop=True)
   fig, ax = plt.subplots(figsize=(4,2))
   sns.barplot(df_grp2, x = 'Amount', y = 'Month', ax=ax)
   plt.title('Monthly expenses', fontsize=8)
   plt.xlabel('Amount in INR', fontsize=8)
   plt.ylabel('Month', fontsize=8)
   plt.xticks(fontsize=8)
   plt.yticks(fontsize=8)   
   st.pyplot(fig)
 
   df_grp3 = expensedf.groupby(['Payment_Mode'])['Amount'].sum().reset_index()
   df_grp3 = df_grp3.sort_values(['Amount']).reset_index(drop=True)
   fig, ax = plt.subplots(figsize=(4,2))
   sns.barplot(df_grp3, x = 'Amount', y = 'Payment_Mode', width = 0.3, ax=ax)
   plt.title('Amount spent using different Payment Modes', fontsize=8)
   plt.xlabel('Amount in INR', fontsize=8)
   plt.ylabel('Payment Mode', fontsize=8)
   plt.xticks(fontsize=8)
   plt.yticks(fontsize=8)   
   st.pyplot(fig)

   df_grp4 = expensedf.groupby(['Month'])['Cashback'].sum().reset_index()
   df_grp4 = df_grp4.sort_values(['Cashback']).reset_index(drop=True)
   fig, ax = plt.subplots(figsize=(4,2))
   sns.barplot(df_grp4, x = 'Cashback', y = 'Month', width = 0.3, ax=ax)
   plt.title('Cashback Amount ', fontsize=8)
   plt.xlabel('Cashback in INR', fontsize=8)
   plt.ylabel('Month', fontsize=8)
   plt.xticks(fontsize=8)
   plt.yticks(fontsize=8)   
   st.pyplot(fig)

   df_grp6 = expensedf.groupby(['Category'])['Cashback'].sum().reset_index()
   df_grp6 = df_grp6.sort_values(['Cashback']).reset_index(drop=True)
   fig, ax = plt.subplots(figsize=(4,2))
   sns.barplot(df_grp6, x = 'Cashback', y = 'Category', width = 0.3, ax=ax)
   plt.title('Cashback as per the Category ', fontsize=8)
   plt.xlabel('Cashback in INR', fontsize=8)
   plt.ylabel('Category', fontsize=8)
   plt.xticks(fontsize=8)
   plt.yticks(fontsize=8)   
   st.pyplot(fig)

   df_grp5 = expensedf.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
   fig, ax = plt.subplots(figsize=(10,6))
   sns.barplot(df_grp5, x = 'Month', y = 'Amount', ax=ax, hue='Category')
   plt.title('Monthly expenses', fontsize=8)
   plt.xlabel('Month', fontsize=8)
   plt.ylabel('Amount', fontsize=8)
   plt.xticks(fontsize=8)
   plt.yticks(fontsize=8)   
   st.pyplot(fig)
   st.dataframe(df_grp5, width=600, use_container_width= False, hide_index= True)



# Content for Tab 2
with tab2:
   st.write("Data analysis on Expense Tracker")
   

   option = st.selectbox(
    "Select the Analysis that you would like to perform from Expense Data",
    ("The Total amount invested during the year", "The Total Cashback recieved for the year", 
    "Amount spent in Vacations using Credit Card", 
    "No. of transactions using UPI payment mode across different categories", "Total Amount Spent across different categories using Credit Card",
    "The amount spent across different Categories", "Month wise expense across all categories", "Month wise expense on groceries", "Weekday expense on groceries", "Weekend expense on groceries",
    "The highest amount on a single transaction during the year", "Total expenses of the year", 
    "Month wise expense on bill", "Month wise expense on Stationary", "Month wise cashback Amount",
    "No. of Transactions on different Payment Mode", "No. of transactions using different payment modes across all categories"
       ),  
       )  

   st.write("You selected:", option)

   if option == "The Total amount invested during the year":
       sql = "SELECT SUM(Amount) As Amount FROM expense WHERE Category = 'Investement'"
       x_axis = None
       y_axis = 'Amount'
   elif option == "The Total Cashback recieved for the year":
       sql = "SELECT SUM(Cashback) As Amount FROM expense"
       x_axis= None
       y_axis = 'Amount'
   elif option == "Amount spent in Vacations using Credit Card":
       sql = "SELECT SUM(Amount) As Amount FROM expense where category = 'Vacation' AND Payment_Mode = 'OnlineCC' "
       x_axis = None
       y_axis = 'Amount'
   elif option == "No. of transactions using UPI payment mode across different categories":
       sql = "SELECT Category As Category, COUNT(*) As Count_UPI FROM expense WHERE Payment_Mode ='UPI' GROUP BY Category ORDER BY COUNT(*) DESC "
       y_axis = 'Count_UPI'
       x_axis = 'Category'
   elif option == "Total Amount Spent across different categories using Credit Card":
       sql = "SELECT Category As Category_CreditCard, SUM(Amount) As Amount FROM expense where Payment_Mode = 'OnlineCC' GROUP BY Category ORDER BY SUM(Amount) DESC"
       x_axis = 'Category_CreditCard'
       y_axis = 'Amount'
   elif option == "The amount spent across different Categories":
       sql = "SELECT Category, SUM(Amount) As Amount FROM expense GROUP BY Category ORDER BY SUM(Amount) DESC"
       x_axis = 'Category'
       y_axis = 'Amount'
   elif option == "Month wise expense on groceries":
       sql = "SELECT SUM(Amount) As Amount_Groceries, MONTH(Date) As Month from expense where category = 'Groceries' GROUP BY MONTH(Date) ORDER BY MONTH"
       x_axis = 'Month'
       y_axis = 'Amount_Groceries'
   elif option == "Weekday expense on groceries":
       sql = "SELECT SUM(Amount) As Amount FROM expense where weekday(Date) <= 5 and category = 'Groceries'"
       x_axis = None
       y_axis = 'Amount'
   elif option == "Weekend expense on groceries":
       sql = "SELECT SUM(Amount) As Amount FROM expense where weekday(Date) >= 6 and category = 'Groceries'"
       x_axis = None
       y_axis = 'Amount'
   elif option == "Month wise expense across all categories":
       sql = " SELECT SUM(Amount) As Amount, MONTH(Date) As Month from expense GROUP BY MONTH(Date) ORDER BY MONTH"
       x_axis = 'Month'
       y_axis = 'Amount'
   elif option == "The highest amount on a single transaction during the year":
       sql = " SELECT Category, max(Amount) As Max_Amount from expense GROUP BY Category ORDER BY max(Amount) DESC"
       x_axis = 'Category'
       y_axis = 'Max_Amount'
   elif option == "Total expenses of the year":
       sql = " SELECT SUM(Amount) As Amount from expense"
       x_axis = None
       y_axis = 'Amount' 
    #elif option == "Expense incurred in the month of Jan":
    #   sql = "SELECT SUM(Amount) As Amount_Jan from expense WHERE MONTH(Date) = 1 "
    #   x_axis = None
    #   y_axis = 'Amount_Jan'
   elif option == "Month wise expense on bill":
       sql = "SELECT SUM(Amount) As Amount_Bill, MONTH(Date) As Month from expense where category = 'Bill' GROUP BY MONTH(Date) ORDER BY MONTH"
       x_axis = 'Month'
       y_axis = 'Amount_Bill'
   elif option == "Month wise expense on Stationary":
       sql = "SELECT SUM(Amount) As Amount_Stationary, MONTH(Date) As Month from expense where category = 'Stationary' GROUP BY MONTH(Date) ORDER BY MONTH"
       x_axis = 'Month'
       y_axis = 'Amount_Stationary'
   elif option == "Month wise cashback Amount":
       sql = "SELECT MONTH(Date) As Month, SUM(Cashback) As Cashback from expense GROUP BY MONTH(Date) ORDER BY MONTH"
       x_axis ='Month'
       y_axis = 'Cashback'
   elif option == "No. of Transactions on different Payment Mode":
       sql = "SELECT Payment_mode, COUNT(*) As Count_Transaction from expense GROUP BY Payment_Mode"
       x_axis = 'Payment_mode'
       y_axis = 'Count_Transaction'
   elif option == "No. of transactions using different payment modes across all categories":
       sql = "SELECT Category, Payment_Mode , COUNT(*) As Count_Transaction  FROM expense_database.expense GROUP BY Category, Payment_Mode ORDER BY Category"
       x_axis= 'Category'
       y_axis = 'Count_Transaction'

   with mydb.cursor() as mycursor:
       mycursor.execute(sql)
       result = mycursor.fetchall()
       df = pd.DataFrame(result, columns=[desc[0] for desc in mycursor.description], index=None)
       mycursor.close()
       mydb.close()
       st.dataframe(df, width= 400, hide_index= True)
       st.line_chart(df ,x= x_axis, y=y_axis)
         

# Content for Tab 3
   with tab3:
    st.markdown("##### :blue[The Project aims to simulate an expense tracker for an individual. The tracker will highlight expenses across categories like bills, groceries, subscriptions, and personal spending, providing a comprehensive overview of financial habits over a year.]")
    st.write('##### :blue[Based on the Analysis done on the data, we have given an overview of the insights:]')
    st.write('###### :orange[1. Maximum Amount was Spent on the Bill Category (Water bill or Eelectricy bill or House Rent or Gas Bill) - 90,955.7500/-]')
    fig = px.pie(df_grp1, values = 'Amount', names= 'Category')
    st.plotly_chart(fig)
    st.write('###### :orange[2. Maximum Amount was Spent in the Month of March - 61,732.5600/-]')
    fig = px.pie(df_grp2, values = 'Amount', names= 'Month')
    st.plotly_chart(fig)
    st.write('###### :orange[3. Maximum number of transactions was done using Online Debit Card]')
    fig = px.pie(df_grp3, values = 'Amount', names= 'Payment_Mode')
    st.plotly_chart(fig)
    st.write('###### :orange[4. Highest Cashback was recieved in the month of January - 2971.59/- ]')
    fig = px.pie(df_grp4, values = 'Cashback', names= 'Month')
    st.plotly_chart(fig)
    st.write('###### :orange[5. Max Cashback was recieved for the Category - Bill ]')
    fig = px.pie(df_grp6, values = 'Cashback', names= 'Category')
    st.plotly_chart(fig)
    st.write('###### :orange[6. Monthly spending across all the categories ]')
    fig = px.scatter(df_grp5, x = 'Month', y='Amount', color='Category')
    st.plotly_chart(fig)
    st.write('###### :orange[7. The Overall Spending pattern has mostly remained stable:]')
    #fig = px.line(df_grp2, x = 'Month', y = 'Amount')
    #st.plotly_chart(fig)
    st.line_chart(df_grp2, x = 'Month', y= 'Amount')

    
    