import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
st.set_page_config(layout="wide")

st.title("Lahoti Srivastava Dua Superbowl Squares :football:")

# style
th_props = [
  ('font-size', '14px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#6d6d6d'),
  ('background-color', '#f7ffff')
  ]
                               
td_props = [
  ('font-size', '14px'),
  ('text-align', 'center')
  ]
                                 
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]


# df = pd.read_csv('superbowl_squares.csv', index_col='Unnamed: 0')
df = pd.read_excel('superbowl_squares.xlsx', index_col=[0,1], header=[0,1])  
df = df.reset_index().fillna(method='ffill', axis=0).set_index('level_0')
print(df.columns)
df.columns = pd.MultiIndex.from_tuples([(col[0], col[1]) if col[0] != 'level_1' else ('', col[1]) for col in df.columns])
# st.dataframe(df.style.apply(lambda x: "background-color: red"))
st.table(df.style.set_table_styles(styles))