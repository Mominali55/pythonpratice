import streamlit as st
import sqlite3
#Title 
st.title("Unit Converter Hub")



#databse table

def database_table():
    connnecter = sqlite3.connect('history.db')
    table1 = connnecter.cursor()

    table1.execute(""" 
        CREATE TABLE conversion_history (
            id INTEGER PRIMARY KEY,
            user_input REAL,
            from_unit TEXT,
            to_unit TEXT,
            result REAL
        )   
    """)
    connnecter.commit()
    connnecter.close()

# Only running thsi function ones for creating the database table
# database_table()

#Conversion selection 
conversion_type = st.multiselect(
    "Select a parametter",["kilometers to miles",
                           "Meters to feet",
                           "kilograms to pounds",
                           "Celsius to Fehrenheit",
                           "INR to Dollar"
                           ])


def main():
    if len(conversion_type) > 0:
        calling_function(conversion_type)

def calling_function(conversion_type):

    #calling function according to the user
    for cnv_type in conversion_type:
        if cnv_type == "kilometers to miles":
            kilometers_to_miles()
        elif cnv_type == "Meters to feet":
            Meters_to_feet()        
        elif cnv_type == "Celsius to Fehrenheit":
            Celsius_to_Fehrenheit()
        elif cnv_type == "kilograms to pounds":
            kilograms_to_pounds()        
        else:
            INR_to_Dollar()


# Variables in this function has to be unique as it can lead to error if same variable is used in different function.
def kilometers_to_miles():
    var1 = st.number_input("Enter value:",value=0.0, step =None,key="km_to_miles")
    if st.button("Convert",key="km_to_miles_btn"):
        result = var1 * 0.621371
        st.write(f"{var1} kilometers is equal to {result} miles")
        safe_conversation(var1,"kilometer","miles",result)

def Meters_to_feet():
    var2 = st.number_input("Enter value:",value=0.0, step =None,key="m_to_feet")
    if st.button("Convert",key="m_to_feet_btn"):
        result = var2 * 3.28084
        st.write(f"{var2} meters is equal to {result} feet")
        safe_conversation(var2,"Meters","feet",result)

def Celsius_to_Fehrenheit():
    var3 = st.number_input("Enter value:",value=0.0, step =None,key="c_to_f")
    if st.button("Convert",key="c_to_f_btn"):
        result = (var3*9/5)+32
        st.write(f"{var3} Celsius is equal to {result} Fehrenheit")
        safe_conversation(var3,"Celsius","Fehrenheit",result)

def kilograms_to_pounds():
    var4 = st.number_input("Enter value:",value=0.0, step =None,key="kg_to_lbs")
    if st.button("Convert",key="kg_to_lbs_btn"):
        result = var4 * 2.20462
        st.write(f"{var4} kilograms is equal to {result} pounds")
        safe_conversation(var4,"kilograms","pounds",result)

def INR_to_Dollar():
    var5 = st.number_input("Enter value:",value=0.0, step =None,key="inr_to_dollar")
    if st.button("Convert",key="inr_to_dollar_btn"):
        result = var5 * 0.012
        st.write(f"{var5} INR is equal to {result} Dollar")
        safe_conversation(var5,"INR","Dollar",result)



#Saving conversations
def safe_conversation(user_input,from_unit,to_unit,result):
    connectors=sqlite3.connect('history.db')
    inserter = connectors.cursor()

    inserter.execute('''
        INSERT INTO conversion_history (user_input,from_unit,to_unit,result)
                     VALUES (?,?,?,?)
    ''',(user_input,from_unit,to_unit,result))

    connectors.commit()
    connectors.close()


main()


st.write("----")
st.header("Conversation history")

display_conv = sqlite3.connect("history.db")

#have tu use pandas for diplaying the table
import pandas as pd
table_displayer = pd.read_sql_query("SELECT * FROM conversion_history",display_conv)
display_conv.close()

#display table in streamlit
st.dataframe(table_displayer)



    
