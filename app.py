import streamlit as st
import pandas as pd
import duckdb
from duckdb.duckdb import ParserException, CatalogException, BinderException

st.write("Hello world!")
data = {"a":[1, 2, 3], "b":[4, 5, 6]}
df = pd.DataFrame(data)

input_text = st.text_area(label="Entrez votre texte")
st.write(input_text)
try:
    df_request = duckdb.sql(input_text).df()
except AttributeError:
    df_request = df
except ParserException:
    df_request = df
    st.write("Bad request")
except CatalogException:
    df_request = df
    st.write("Bad table name")
except BinderException:
    df_request = df
    st.write("Bad column name")

try:
    st.dataframe(df_request)
except NameError:
    pass
