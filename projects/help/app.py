import streamlit as st


class Dog:
    """A typical dog."""

    def __init__(self, breed, color):
        self.breed = breed
        self.color = color

    def bark(self):
        return "Woof!"


dog = Dog(breed="Golden Retriever", color="Brown")
st.help(dog)
st.help(dict)
