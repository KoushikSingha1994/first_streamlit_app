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

streamlit.header('Frityvice Fruit Advice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowdtls"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The Fruit Load List contains:")
streamlit.dataframe(my_data_row)

add_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for adding ', add_fruit)
my_cur.execute("insert into fruit_load_list values('from streamlit')")
