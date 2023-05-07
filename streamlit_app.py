import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.header('Hello Folks')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
fruit_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
if not fruit_selected:
  fruit_to_show = my_fruit_list
else:
  fruit_to_show = my_fruit_list.loc[fruit_selected]
streamlit.dataframe(fruit_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header('Frityvice Fruit Advice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruit_result=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruit_result)
except URLError as e:
  streamlit.error()

streamlit.header("The Fruit Load List Contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
  
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowdtls"])
  my_data_rows=get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values(new_fruit)")
    return new_fruit+" Added Successfully!!"
try:
  add_fruit = streamlit.text_input('What fruit would you like to add?')
  if not add_fruit:
    streamlit.error("Please enter fruit name to insert")
  else:
    my_result = insert_row_snowflake(add_fruit)
    streamlit.write(my_result)
except URLError as e:
  streamlit.error()
