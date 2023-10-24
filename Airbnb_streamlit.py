import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Setting Webpage Configurations
st.set_page_config(page_title="Airbnb", layout="wide")

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title(':violet[AirBnb Geospatial Analysis]')

data = pd.read_csv(r'D:\Data_Excel\airbnb_excel.csv')

aggregated = data.groupby(['country','market']).count()

tab1,tab2 = st.tabs(['Geospatial Analysis ','Exploratory Data Analysis '])

with tab1:
    country_in = st.selectbox('Select a Country',options=data['country'].unique())

    Room = st.selectbox('Select a Room type',options=data['room_type'].unique()) 



    st.divider() 

    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)

    if country_in and Room:
        try:
           # query_df = data.query(f'country == "{country_in}" and city == "{city_in}" and price>={min_price} and price<={max_price}')
            query_df = data.query(f'country == "{country_in}" and city == "{Room}')
            reset_index = query_df.reset_index(drop = True)
        
            # Creating map using folium
            base_latitude = reset_index.loc[0,'latitude']
            base_longitude = reset_index.loc[0,'longitude']

            base_map = folium.Map(location=[base_latitude,base_longitude], zoom_start=12)

            for index, row in reset_index.iterrows():
                lat,lon = row['latitude'],row['longitude']
                id = row['id']
                name = row['name']
                price = row['price']
                review = row['review_score']
                #popup_text = f"ID: {id} | Name: {name} | Price: ${price}"
                popup_text = f"ID: {id} | Name: {name} | Price: ${price} | Rating: {review}/10"
                folium.Marker(location=[lat, lon], popup=popup_text).add_to(base_map)

            # call to render Folium map in Streamlit
            st_data = st_folium(base_map, width=1200,height = 600)

            st.divider()

            st.subheader(':blue[Top Hotels Recommendations]')
            
            df = reset_index.sort_values(by=['price','review_scores'],ascending = False)

            new_df = df[['id','url','name','market','country','amenities','price','review_scores','number_of_reviews']]

            st.dataframe(new_df.head(),hide_index = True,width=1175,height=218)

            st.divider() 

            st.subheader(':blue[Top Hotels by Price ] ')

            query_top = data.query(f'country == "{country_in}" and city == "{Room}"')

            query_1 = query_top.sort_values(by = ['price'],ascending = False)

            new_df1 = query_1[['id','url','name','market','country','amenities','price','review_scores','number_of_reviews']]

            st.dataframe(new_df1.head(),hide_index=True,width = 1175, height = 220)

            st.divider()

            st.subheader(':blue[Enter the ID to know more about the Hotel and Availability] ')

            id_input = st.text_input('Enter a ID')

            if id_input:
                new_query = reset_index.query(f'country == "{country_in}" and city == "{Room}" and id == {id_input}')
                new_table = new_query[['id','url','name','amenities','price','availability_30','availability_60','availability_90','availability_365']] 
                st.dataframe(new_table,hide_index = True, width = 1175, height = 78)

                st.divider()

        except:
            st.info('No results found')


# Exploratory Data Analysis

with tab2:

    col1,col2 = st.columns(2)

    option = st.selectbox('Exploratory Data Analysis',('Select an Analysis','Price Analysis by Country', 'Distribution of Price by Country', 'Distribution of Price using Box Plot','Scatter Plot by Price and Availability'))

    st.divider() 
    # 1. Categorical Data -- country, city, review_score

    if option == 'Price Analysis by Country':
        fig = px.histogram(data,x = 'market',animation_frame='country',color = 'country')
        fig.update_layout(width=1200,height=500, title="Animated Histogram by City",xaxis_title="City",yaxis_title="Count")
        st.plotly_chart(fig)

        col1,col2 = st.columns(2)

        with col1:
        
            country_df = data[['country','market']].value_counts()
            new_country_df = pd.DataFrame(country_df,columns = ['Number of Hotels'])
            st.dataframe(new_country_df,width=450,height=528)

        with col2:
       
            grouped = data.groupby(['country','market']).agg({'price':'mean','review_scores':'mean'}).sort_values(by=['price','review_scores'],ascending = False)
            grouped = grouped.round()
            st.dataframe(grouped,width = 600,height = 528)
        st.divider() 

    # 2. Numerical Data - Price

    elif option == 'Distribution of Price by Country':
        # Distribution of Data in a Numerical Columns
        country = st.selectbox('Select any Country',options=data['country'].unique())

        if country == 'Australia':
            city = st.selectbox('Select any City',options=['Sydney'])

        elif country == 'Brazil':
            city = st.selectbox('Select any City',options=['Rio De Janeiro'])

        elif country == 'Canada':
            city = st.selectbox('Select any City',options=['Montreal'])

        elif country == 'China':
            city = st.selectbox('Select any City',options=['Hong Kong'])

        elif country == 'Hong Kong':
            city = st.selectbox('Select any City',options=['Hong Kong'])

        elif country == 'Portugal':
            city = st.selectbox('Select any City',options=['Porto'])

        elif country == 'Spain':
            city = st.selectbox('Select any City',options=['Barcelona'])

        elif country == 'Turkey':
            city = st.selectbox('Select any City',options=['Istanbul'])

        elif country == 'United States':
            city = st.selectbox('Select any City',options=['Kauai','Maui','New York','Oahu','The Big Island'])

        st.divider() 

        country_price_wise = data.query(f'country == "{country}" and market == "{city}"')

        plt.figure(figsize=(8,3.5))
        fig1 = sns.distplot(country_price_wise['price'])
        st.pyplot()

        if country_price_wise["price"].skew() > 0:
            st.write(f'Since the value is Positive : {country_price_wise["price"].skew()}, the curve is skewed Positively to the right side')
        elif country_price_wise["price"].skew() < 0:
            st.write(f'Since the value is Negative : {country_price_wise["price"].skew()}, the curve is skewed Negatively to the left side')
        
        st.divider() 

    elif option == 'Distribution of Price using Box Plot':
        # Box_plot
        fig2 = px.box(data,x = 'country', y = 'price',color = 'country',width=1200, height=650)
        st.plotly_chart(fig2)

        st.divider() 

    elif option == 'Scatter Plot by Price and Availability':
        # 3. Scatter Plot (Numerical - Numerical) - (Price - Availability)
        subplots = make_subplots(rows=4, cols=1,subplot_titles = ('Availability 30', 'Availability 60', 'Availability 90', 'Availability 365'))
        scatter_plots1 = go.Scatter(x = data['price'],y = data['availability_30'],mode='markers', name = 'Availability 30')
        subplots.add_trace(scatter_plots1, row=1, col=1)
        
        scatter_plots2 = go.Scatter(x = data['price'],y = data['availability_60'],mode='markers',name = 'Availability 60')
        subplots.add_trace(scatter_plots2, row=2, col=1)

        scatter_plots3 = go.Scatter(x = data['price'],y = data['availability_90'],mode='markers',name = 'Availability 90')
        subplots.add_trace(scatter_plots3, row=3, col=1)

        scatter_plots4 = go.Scatter(x = data['price'],y = data['availability_365'],mode='markers',name = 'Availability 365')
        subplots.add_trace(scatter_plots4, row=4, col=1)

        subplots.update_layout(height=750,width = 1200) 
        st.plotly_chart(subplots)

        st.divider() 


    