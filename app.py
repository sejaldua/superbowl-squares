import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
st.set_page_config(layout="wide")

st.title("Lahoti Srivastava Dua Superbowl Squares :football:")
st.write("Hi family! Welcome to superbowl squares! The grid has been made using some randomization code to accommodate the number of squares that everyone has requested. Please note that the numbers 0-9 that you see on the top and left of the grid will be shuffled shortly before kickoff!")

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
  ('text-align', 'center'),
#   ('background-color', '#ffffff'),
  ('color', '#000')
  ]
                                 
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]

color_dict = {
    
	'Pushpa'		: '#97C1A9',
	'HDL'		    : '#B7CFB7',
	'Bhupesh'		: '#55CBCD',
	'Sarita'		: '#A3E1DC',
	'Sejal'		    : '#B5EAD6',
	'Rahul'		    : '#C7DBDA',
	'Ameet'		    : '#FFB8B1',
	'Eka'		    : '#FFDAC1',
	'Sanvi'		    : '#F4978E',
	'Sia'		    : '#F6EAC2',
	'Ace'		    : '#FFE1E9',
	'Sunil'		    : '#9AB7D3',
	'Abs'		    : '#F5D2D3',
	'Jayden'		: '#A2D2FF',
	'Milen'		    : '#DFCCF1',
	'Rowen'		    : '#BDE0FE',
}

# df = pd.read_csv('superbowl_squares.csv', index_col='Unnamed: 0')
df = pd.read_excel('superbowl_squares.xlsx', index_col=[0,1], header=[0,1]) 
df = df.reset_index().fillna(method='ffill', axis=0).set_index(['level_0', 'level_1'])
print(df.index) 
df.columns = pd.MultiIndex.from_tuples([(col[0], col[1]) if col[0] != 'level_1' else ('', col[1]) for col in df.columns])
for col in df.columns:
    df[col] = df[col].replace("Hanuman", "HDL")
s = df.style.set_table_styles(styles)
# st.dataframe(df.style.apply(lambda x: "background-color: red"))
s2 = s.applymap(lambda v: f'background-color: {color_dict[v]};')
st.table(s2)