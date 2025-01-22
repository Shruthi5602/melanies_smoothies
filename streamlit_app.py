# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

##option = st.selectbox(
    ##"What is your favorite fruit?",
    ##("Banana", "Strawberries", "Peaches"),
##)

##st.write("Your favorite fruit is:", option)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    # Corrected SQL insert statement
    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients)
            VALUES ('""" + ingredients_string.strip() + """')"""

    #st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
import requests

# Replace 'your_api_key' with your actual API key
api_key = 'your_api_key'
fruit_name = 'watermelon'
url = f"https://www.fruityvice.com/api/fruit/{fruit_name}"

headers = {
    'Authorization': f'Bearer {api_key}'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    response_json = response.json()
    st.json(response_json)
else:
    st.text(f"Response {response.status_code}")
