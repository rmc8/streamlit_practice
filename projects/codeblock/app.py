import streamlit as st

code = """
function hello() {
    console.log("Hello Streamlit!");
}
"""
st.code(
    code,
    language="javascript",
    line_numbers=True,
)
