import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")
from urllib.request import urlopen
from bs4 import BeautifulSoup
from optimizer import *

st.title("Superbowl Squares Generator :football:")
st.caption("""
The intent of this application is to alleviate the burden of making a Super Bowl squares grid for groups of 
people that are engaging in some friendly betting fun! The program has been made using some linear optimization 
code to accommodate the number of squares that everyone has requested.
""")

mode = st.sidebar.selectbox('Please select how you would like to enter your participant information', ['Manual Entry', 'Information Upload'])
players = []
squares = []
if mode == 'Manual Entry':
  num_participants = st.sidebar.number_input('How many players do you have?', value=None if 'num_participants' not in st.session_state else st.session_state['num_participants'], min_value=2, max_value=100)
  if num_participants is not None:
    default_squares = 100 // num_participants
    init_df = pd.DataFrame(list(zip(['']*num_participants, [default_squares]*num_participants)), columns=['Name', 'Squares'])
    init_df.index = init_df.index + 1
    st.sidebar.caption('Equal distributions of squares is assumed, but you are welcome to modify the table below.')
    st.session_state['info_df'] = st.sidebar.data_editor(init_df, use_container_width=True)
    if st.session_state['info_df']['Name'].nunique() == num_participants:
      players = st.session_state['info_df']['Name'].to_list()
      squares = st.session_state['info_df']['Squares'].to_list()
elif mode == 'Information Upload':
  st.sidebar.caption('Please enter a 2-column CSV or XLSX file containing columns named "Name" and "Squares" (see example below)')
  st.sidebar.markdown('''
  | Name | Squares |
  |:---:|:---|
  | Adam | 10      |
  | Bob  | 20      |
  | Chad | 5       |\          
''')
  st.sidebar.markdown(" ")
  f = st.sidebar.file_uploader('', accept_multiple_files=False)
  if f is not None:
    if f.name.endswith('.csv'):
      info = pd.read_csv(f)
    elif f.name.endswith('.xlsx'):
      info = pd.read_excel(f)
    else:
      st.sidebar.error('The file that was uploaded could not be parsed. Please upload a CSV or Excel file.')
    
    info_df = st.sidebar.data_editor(info)
    players = info_df['Name'].to_list()
    squares = info_df['Squares'].to_list()

# style
th_props = [
  ('font-size', '14px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#6d6d6d'),
  ('background-color', '#f7ffff'),
  ('width', '100px'),
   ('font-family', ' Avenir Medium'),
  ]
                               
td_props = [
  ('font-size', '14px'),
  ('text-align', 'center'),
  ('font-family', 'Avenir'),
  ('color', '#000')
  ]
                                 
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]

palette = ['#FDD8B1', '#FFE5DE', '#F8BBD0', '#C1F0F3', '#BDF7D3', '#DEF5F5', '#DCDCFE', '#EAF2D3', '#FC86A1', '#87CEEB',
'#ADBCA5', '#EAD637', '#A2D3C2', '#A499B3', '#9183EC', '#4CBDBB', '#F58266', '#38AECC', '#E5F98B', '#BCA89F', '#F4978E']
color_dict = {p: v for p, v in zip(players, palette[:len(players)])}
color_dict['WILD'] = '#FFFFFF'
  
if len(players) == num_participants and '' not in players and len(squares) == num_participants:
  if st.sidebar.button('Generate Squares', use_container_width=True, type="primary"):
    matrix = get_squares(players, squares)
    df = pd.DataFrame(matrix, columns = list(range(10)))
    df.index = [f'SF {x}' for x in df.index]
    df.columns = [f'KC {x}' for x in df.columns]
    if num_participants <= len(palette):
      s = df.style.applymap(lambda v: f'background-color: {color_dict[v]};').set_table_styles(styles)
    else:
      s = df

    st.dataframe(s, use_container_width=True)