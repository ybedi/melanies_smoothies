# Import python packages
import streamlit as st
import pandas as pd
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want.
  """
)

title = st.text_input("Name on your Smoothie")
st.write("The name on your smoothie will be: ", title)

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredient_list = st.multiselect('Select upto 5 ingredients',my_dataframe)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)

    if len(ingredient_list) > 5:
        st.write("""Please Enter upto 5 items only!!""")
        st.stop()
        
    ingredients_str = ''
    for item in ingredient_list:
        ingredients_str += item + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == item, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', item,' is ', search_on, '.')
        #st.write(ingredients_str)
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        st.subheader(item + ' Nutrient Information')
        st_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
  
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_str + """','""" + title + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is Ordered! '+ title,icon=":material/thumb_up:")





