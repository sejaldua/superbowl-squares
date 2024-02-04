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
  num_participants = st.sidebar.number_input('How many players do you have?', value=None, min_value=2, max_value=100)
  if num_participants is not None:
    col1, col2 = st.sidebar.columns(2)
    for i in range(num_participants):
      players.append(col1.text_input(f'Player {i+1}'))
      squares.append(col2.number_input(f'P{i+1} Squares', value=100//num_participants, min_value=1, max_value=99))
print(players)

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
  # ('border-color', 'transparent'),
#   ('background-color', '#ffffff'),
  ('color', '#000')
  ]
                                 
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]

palette = ['#FDD8B1', '#FFE5DE', '#F8BBD0', '#C1F0F3', '#DEF5F5', '#DCDCFE', '#EAF2D3', '#FC86A1', '#87CEEB', '#BDF7D3',
'#ADBCA5', '#EAD637', '#A2D3C2', '#A499B3', '#9183EC', '#4CBDBB', '#F58266', '#38AECC', '#E5F98B']
color_dict = {p: v for p, v in zip(players, palette[:len(players)])}
color_dict['X'] = '#FFFFFF'
print(color_dict)
# color_dict = {
    
# 	'Pushpa'		: '#97C1A9',
# 	'Hanuman Das Lahoti'		    : '#B7CFB7',
# 	'Bhupesh'		: '#55CBCD',
# 	'Sarita'		: '#A3E1DC',
# 	'Sejal'		    : '#B5EAD6',
# 	'Rahul'		    : '#C7DBDA',
# 	'Ameet'		    : '#FFB8B1',
# 	'Eka'		    : '#FFDAC1',
# 	'Sanvi'		    : '#F4978E',
# 	'Sia'		    : '#F6EAC2',
# 	# 'Ace'		    : '#BCA89F',
# 	'Sunil'		    : '#9AB7D3',
# 	'Abs'		    : '#F5D2D3',
# 	'Jayden'		: '#A2D2FF',
# 	'Milen'		    : '#DFCCF1',
# 	'Rowen'		    : '#BDE0FE',
# }

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

# df = pd.read_csv('superbowl_squares.csv', index_col='Unnamed: 0')
# df = pd.read_excel('superbowl_squares.xlsx', index_col=[0,1], header=[0,1]) 
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