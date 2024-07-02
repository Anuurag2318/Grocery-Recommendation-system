import streamlit as st
import pickle
import difflib
import os
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
conn=sqlite3.connect('data.db',check_same_thread=False)
cur=conn.cursor()
def recommend(product):
    if(name==""):
        st.write("Please Write your name")
    else:
        grocery_data=pickle.load(open('groceryitems.pkl','rb'))
        selected_features=['Type']
        for feature in selected_features:
            grocery_data[feature]=grocery_data[feature].fillna('')
        combined_features=grocery_data['Type']
        vectorizer=TfidfVectorizer()
        feature_vector=vectorizer.fit_transform(combined_features)
        similarity=cosine_similarity(feature_vector)
        list_of_all_product=grocery_data['Productname'].tolist()
        find_close_match=difflib.get_close_matches(product,list_of_all_product)
        close_match=find_close_match[0]
        index_of_the_product=grocery_data[grocery_data.Productname==close_match]['ID'].values[0]
        similarity_score=list(enumerate(similarity[index_of_the_product]))
        sorted_similar_product=sorted(similarity_score,key= lambda x:x[1],reverse=True)
        i=1
        for product in sorted_similar_product:
            index=product[0]
            name_from_index=grocery_data[grocery_data.ID==index]['Productname'].values[0]
            description_from_index=grocery_data[grocery_data.index==index]['Description'].values[0]
            if(i<=5):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("You may also like: ")
                    st.write(i,name_from_index)
                    addData(name,name_from_index)
                    f = open(r"C:\Grocery Recommendation System\\"+description_from_index, "r")
                    st.write("Description:- "+f.read())

                i+=1
def addData(a,b):
    cur.execute("""CREATE TABLE IF NOT EXISTS grocerydata(NAME TEXT(50),RECOMMENDATIONS TEXT(50));""")
    cur.execute("INSERT INTO grocerydata VALUES(?,?)",(a,b))
    conn.commit()
grocery_list=pickle.load(open('groceryitems.pkl','rb'))
grocery_list=grocery_list['Productname'].values
st.title('Grocery Recommendation system')
name=st.text_input("Enter Your Name: ")
selected_product_name=st.selectbox('Enter the product item you have purchased',(grocery_list))
if st.button('Recommend'):
    recommend(selected_product_name)