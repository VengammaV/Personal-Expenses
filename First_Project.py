import streamlit as st
import pandas
import pymysql

st.title("Expense Tracker")
st.subheader("Personal Expense Tracker is a project to analyse the expenses made by a person. Provide expenses based on various criteria to help understand the Finance Management in a better manner.")

mydb = pymysql.connect(
        host = "localhost",
        user = "root",
        password = "123456789",
        database= "expense_database",
        autocommit = True)
mycursor = mydb.cursor()

option = st.selectbox(
    "Select the Analysis that you would like to perform from Expense Data",
    ("The Total amount invested during the year", "The Total Cashback recieved for the year", 
     "Amount spent in Vacations using Credit Card", 
    "No. of transactions using UPI payment mode across different categories", "Total Amount Spent across different categories using Credit Card",
    "The amount spent across different Categories", "Month wise expense across all categories", "Month wise expense on groceries",
    "The highest amount on a single transaction during the year", "Total expenses of the year", "Expense incurred in the month of Jan",
     "Month wise expense on bill", "Month wise expense on Stationary", "Month wise cashback Amount",
     "No. of Transactions on different Payment Mode", "No. of transactions using different payment modes across all categories"
     ),
)

st.write("You selected:", option)

if option == "The Total amount invested during the year":
    sql = "SELECT SUM(Amount) As A FROM expense WHERE Category = 'Investement'"
elif option == "The Total Cashback recieved for the year":
    sql = "SELECT SUM(Cashback) FROM expense"
elif option == "Amount spent in Vacations using Credit Card":
    sql = "SELECT SUM(Amount) FROM expense where category = 'Vacation' AND Payment_Mode = 'OnlineCC' "
elif option == "No. of transactions using UPI payment mode across different categories":
    sql = "SELECT Category, COUNT(*) FROM expense WHERE Payment_Mode ='UPI' GROUP BY Category"
elif option == "Total Amount Spent across different categories using Credit Card":
    sql = "SELECT Category, SUM(Amount) FROM expense where Payment_Mode = 'OnlineCC' GROUP BY Category"
elif option == "The amount spent across different Categories":
    sql = "SELECT Category, SUM(Amount) FROM expense GROUP BY Category"
elif option == "Month wise expense on groceries":
    sql = "SELECT SUM(Amount), MONTH(Date) from expense where category = 'Groceries' GROUP BY MONTH(Date)"
elif option == "Month wise expense across all categories":
    sql = " SELECT SUM(Amount), MONTH(Date) from expense GROUP BY MONTH(Date)"
elif option == "The highest amount on a single transaction during the year":
    sql = " SELECT Category, max(Amount) from expense GROUP BY Category"
elif option == "Total expenses of the year":
    sql = " SELECT SUM(Amount) from expense"
elif option == "Expense incurred in the month of Jan":
    sql = "SELECT SUM(Amount) from expense WHERE MONTH(Date) = 1 "
elif option == "Month wise expense on bill":
    sql = "SELECT SUM(Amount), MONTH(Date) from expense where category = 'Bill' GROUP BY MONTH(Date)"
elif option == "Month wise expense on Stationary":
    sql = "SELECT SUM(Amount), MONTH(Date) from expense where category = 'Stationary' GROUP BY MONTH(Date)"
elif option == "Month wise cashback Amount":
    sql = "SELECT MONTH(Date), SUM(Cashback) from expense GROUP BY MONTH(Date)"
elif option == "No. of Transactions on different Payment Mode":
    sql = "SELECT Payment_mode, COUNT(*) from expense GROUP BY Payment_Mode"
elif option == "No. of transactions using different payment modes across all categories":
    sql = "SELECT Category, Payment_Mode , COUNT(*)  FROM expense_database.expense GROUP BY Category, Payment_Mode"


with mydb.cursor() as mycursor:
    mycursor.execute(sql)
    result = mycursor.fetchall()
st.dataframe(result)