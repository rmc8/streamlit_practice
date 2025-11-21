import time

import numpy as np
import pandas as pd
import streamlit as st


def stream_data(*itrs, sleep_time: float = 0.025):
    def inner():
        for itr in itrs:
            if isinstance(itr, str):
                for char in itr:
                    yield char
                    time.sleep(sleep_time)
            else:
                yield itr
                time.sleep(sleep_time)

    return inner


text = "Streamlit is convenient because you can develop both the backend and frontend using only Python!"
df = pd.DataFrame(
    np.random.randn(5, 10),
    columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
)
additional_text = "You can also display **Pandas DataFrames** in a **tabular format** like the one above."
if st.button("Stream data"):
    st.write_stream(stream_data(text, df, additional_text))
