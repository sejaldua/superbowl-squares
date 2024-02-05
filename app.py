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

def update_initial_df():
  # print(st.session_state)
  if 'info_df' in st.session_state and 'num_participants' in st.session_state and st.session_state['num_participants'] is not None:
    print('updating initial df')
    print('num participants update', st.session_state['num_participants'])
    old_df = st.session_state['info_df'].copy()
    print(old_df)
    old_names = old_df['Name'].to_list()
    print(old_names)
    if len(old_names) <= int(st.session_state['num_participants']):
      print('incremented count')
      names = [*old_names, *(['']*(st.session_state['num_participants'] - len(old_names)))]
    else:
      print('decremented count')
      names = old_names[:st.session_state['num_participants']]
      
    print(names)
    default_squares = 100 // st.session_state['num_participants']
    new_df = pd.DataFrame(list(zip(names, [default_squares]*st.session_state['num_participants'])), columns=['Name', 'Squares'])
    new_df.index = new_df.index + 1
    print('new df')
    print(new_df)
    st.session_state['init_df'] = new_df

mode = st.sidebar.selectbox('Please select how you would like to enter your participant information', ['Manual Entry', 'Information Upload'])
players = []
squares = []
if mode == 'Manual Entry':
  num_participants = st.sidebar.number_input('How many players do you have?', value=None if 'num_participants' not in st.session_state else st.session_state['num_participants'], min_value=2, max_value=100)
  if 'num_participants' in st.session_state and st.session_state['num_participants'] != num_participants:
      st.session_state['num_participants'] = num_participants
      update_initial_df()
  else:
    st.session_state['num_participants'] = num_participants
  print('num participants', st.session_state['num_participants'])
  num_participants = st.session_state['num_participants']
  print(st.session_state['num_participants'])
  # st.session_state['num_participants'] = num_participants
  if num_participants is not None:
    default_squares = 100 // num_participants
    if 'init_df' not in st.session_state:
      init_df = pd.DataFrame(list(zip(['']*num_participants, [default_squares]*num_participants)), columns=['Name', 'Squares'])
      print('resetting df')
      init_flag = True
      st.session_state['init_df'] = init_df
    st.session_state['info_df'] = st.sidebar.data_editor(st.session_state['init_df'], use_container_width=True)
    print(st.session_state['info_df'])
    if st.session_state['info_df']['Name'].nunique() == num_participants:
      players = st.session_state['info_df']['Name'].to_list()
      squares = st.session_state['info_df']['Squares'].to_list()
elif mode == 'Information Upload':
  print('here')
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
# print(players)

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
color_dict['X'] = '#FFFFFF'

def get_current_score():
  url = 'https://www.pro-football-reference.com/boxscores/202302120phi.htm'
  # url = "https://www.pro-football-reference.com/boxscores/202301290phi.htm"
  # Open URL and pass to BeautifulSoup
  html = urlopen(url)
  try:
    soup = BeautifulSoup(html)
    scorebox = soup.find("div", class_="scorebox")
    scores = scorebox.find_all("div", class_="score")
    teams = ['San Francisco 49ers', 'Kansas City Chiefs']
    live_scores = [score.text for score in scores][::-1]
    return {t: int(s) for t, s in zip(teams, live_scores)}
  except:
    return {}
  
def get_possible_scores(score):
  team_indices = {team: [] for team in list(score.keys())}
  for team, score in zip(list(score.keys()), list(score.values())):
    team_indices[team].append((team, int(str(score)[-1:])))
    team_indices[team].append((team, int(str(score + 3)[-1:])))
    team_indices[team].append((team, int(str(score + 7)[-1:])))
  return team_indices

def style_specific_cell(x, outcomes):
    index1, index2 = outcomes.values()
    print("outcomes", outcomes)
    curr_color = 'border: 2px solid black;'
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    df1.loc[index1[0], index2[0]] = curr_color
    possible_color = 'border: 2px dashed green;'
    for combo in [(0, 1), (0, 2), (1, 0), (2, 0)]:
      df1.loc[index1[combo[0]], index2[combo[1]]] = possible_color
    return df1

if len(players) == num_participants and '' not in players and len(squares) == num_participants:
  if st.sidebar.button('Generate Squares', use_container_width=True, type="primary"):
    matrix = get_squares(players, squares)
    df = pd.DataFrame(matrix, columns = list(range(10)))
    df.index = [f'SF {x}' for x in df.index]
    df.columns = [f'KC {x}' for x in df.columns]
    print(df)
    # s2 = pd.concat({'Foo': df}, names=['Firstlevel'])
    s = df.style.applymap(lambda v: f'background-color: {color_dict[v]};').set_table_styles(styles)

    # print(s)
    # st.dataframe(df.style.apply(lambda x: "border-color: red" if ))
    # s2 = s.applymap(lambda v: f'background-color: {color_dict[v]};')
    # gamescore = get_current_score()
    # if gamescore != {}:
    #   print(gamescore)
    #   indices = get_possible_scores(gamescore)
    #   print(indices)
    #   s3 = s.apply(lambda x: style_specific_cell(x, indices), axis=None)
    #   st.table(s3)
    # else:
    st.dataframe(s, use_container_width=True)