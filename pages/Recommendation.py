import streamlit as st
import sqlite3
conn=sqlite3.connect('data.db',check_same_thread=False)
cur=conn.cursor()
st.title("Recommendations")
conn=sqlite3.connect('data.db',check_same_thread=False)
cur=conn.cursor()
cur.execute("select * from grocerydata")
data=cur.fetchall()
# st.write(data)
if (data==[]):
    st.write("No Data Found")
else:
    st.text("Name         Recommendations")
    for d in data:
        st.write(d[0],"------------->",d[1])
    st.title("Want to Remove any Data?")
    name=st.text_input("Enter the name")
    # st.write(cur.fetchone())
    if st.button('Delete'):
        cur.execute(f"DELETE FROM grocerydata where NAME='{name}'")
        conn.commit()
        st.experimental_rerun()