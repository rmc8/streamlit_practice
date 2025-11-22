import streamlit as st

with st.echo():

    def hello():
        return "Hello Streamlit!"

    st.write(hello())
