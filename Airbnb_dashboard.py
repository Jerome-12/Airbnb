# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Setting up page configuration
st.set_page_config(page_title= "Airbnb Data Visualization",layout= "wide")

st.title('Airbnb Data Analysis')

url='https://public.tableau.com/app/profile/jerome.4022/viz/AirbnbData_visualisation/Dashboard1'


with st.sidebar:
        option = option_menu(menu_title='',options=['Exploratory Data Analysis', 'Geo-visualisation'])
        col1, col2 = st.columns([0.26, 0.48])
        st.markdown(f''' <a href={url}><button style="background-color:LightBlue;">Tableau Dashboard</button></a> ''', unsafe_allow_html=True)

        

#Read the data
df = pd.read_csv(r'D:\Data_Excel\airbnb_excel.csv')

country = st.sidebar.multiselect('Select the Country',sorted(df.country.unique()),sorted(df.country.unique()))
prop = st.sidebar.multiselect('Select Property type',sorted(df.property_type.unique()),sorted(df.property_type.unique()))
room = st.sidebar.multiselect('Select Room type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))

if option=='Exploratory Data Analysis':

    st.subheader(':violet[Exploratory Data Analysis]')

    query = f'country in {country} & room_type in {room} & property_type in {prop}'

    col1,col2=st.columns([1,1],gap='large')
      
    with col1:

        #Top 10 Property Types
        df1 = df.query(query).groupby(["property_type"]).size().reset_index(name="count").sort_values(by='count',ascending=False)[:10]
        fig = px.bar(df1,
                         title='Top 10 Property Types',
                         x='property_type',
                         y='count',
                         orientation='v',
                         color='count',
                         color_continuous_scale=px.colors.sequential.Oryel)
        st.plotly_chart(fig,use_container_width=True) 


        #Property types and Number_Of_Reviews
        df1= df.query(query).groupby(["property_type"]).size().reset_index(name="number_of_reviews")
        fig = px.bar(df1,
                             title='Property types and Number_Of_Reviews',
                             x="property_type",
                             y="number_of_reviews",
                             text="property_type",
                             orientation='v',
                             color='number_of_reviews',
                             color_continuous_scale=px.colors.sequential.Bluyl)
        fig.update_traces( textposition='outside')
        st.plotly_chart(fig,use_container_width=True)   

        df1= df1= df.query(query).groupby("property_type",as_index=False)['price'].mean()
        fig = px.bar(df1,
                             title=' Property - Average Price ',
                             x="property_type",
                             y="price",
                             text="price",
                             orientation='v',
                             color='price',
                             color_continuous_scale=px.colors.sequential.Magenta)
        st.plotly_chart(fig,use_container_width=True)     


        #Bed type counts
        df1= df.query(query).groupby(["bed_type"]).size().reset_index(name="count").sort_values(by='count',ascending=False)[:10]
        fig = px.line(df1,
                             title=' Bed_Type Counts',
                             x='bed_type',
                             y='count',text='count',markers=True)
        fig.update_traces(textposition="top center")                    
        st.plotly_chart(fig,use_container_width=True)


        # Top 10 hosts
        df1= df.query(query).groupby('host_name',as_index=False)['number_of_reviews'].sum().sort_values(by='number_of_reviews',ascending=False)[:10]
       # df1 = df.query(query).groupby(["host_name"]).size().reset_index(name="number_of_reviews").sort_values(by='number_of_reviews',ascending=False)[:10]
        fig = px.bar(df1,
                         title='Top 10 Hosts',
                         x='number_of_reviews',
                         y='host_name',
                         orientation='h',
                         color='number_of_reviews',
                         color_continuous_scale=px.colors.sequential.Purp)
        st.plotly_chart(fig,use_container_width=True) 

    with col2:    


        #Room type with price
        df1= df.query(query).groupby('room_type',as_index=False)['price'].mean()
        #df1= df.query(query).groupby(["room_type"]).size().reset_index(name="price").sort_values(by='price',ascending=False)[:10]
        fig = px.pie(df1,
                             title=' Room_Type With Price',
                             values='price',
                             names="room_type")
        fig.update_traces(textposition='inside', textinfo='value+label')
        st.plotly_chart(fig,use_container_width=True)
        
        #Room types with no. of reviews
        df1= df.query(query).groupby(["room_type"]).size().reset_index(name="number_of_reviews")
        fig = px.bar(df1,
                             title='Room Types and Number_Of_Reviews',
                             x="room_type",
                             y="number_of_reviews",
                             text="room_type",
                             orientation='v',
                             color='number_of_reviews',
                             color_continuous_scale=px.colors.sequential.Tealgrn)
        fig.update_traces( textposition='outside')
        st.plotly_chart(fig,use_container_width=True)


        #Cancellation policy
        df1= df.query(query).groupby(["cancellation_policy"]).size().reset_index(name="count")
        #df1= df.query(query).groupby(["cancellation_policy"]).size().reset_index(name="count").sort_values(by='count',ascending=False)[:10]
        fig = px.area(df1,
                             title=' Cancellation_Policy',
                             x='cancellation_policy',
                             y='count',text='count',markers=True)

        fig.update_traces(textposition="top center")                    
        st.plotly_chart(fig,use_container_width=True)


        #Accommodates
        df1= df.query(query).groupby(["accommodates"]).size().reset_index(name="count")
        fig = px.bar(df1,
                             title='Accommodates',
                             x="accommodates",
                             y="count",
                             orientation='v',
                             color='count',
                             color_continuous_scale=px.colors.sequential.Peach)
        st.plotly_chart(fig,use_container_width=True)

if option=='Geo-visualisation':
 
        st.subheader(':violet[Geo-visualisation]')

        query = f'country in {country} & room_type in {room} & property_type in {prop}'
      

        country_df = df.query(query).groupby(['country'],as_index=False)['name'].count().rename(columns={'name' :'Properties'})
        fig = px.choropleth(country_df,
                                title='Properties in each Country',
                                locations='country',
                                locationmode='country names',
                                color='Properties',
                                color_continuous_scale=px.colors.sequential.Darkmint
                               )
        st.plotly_chart(fig,use_container_width=True)
  

        country_df = df.query(query).groupby('country',as_index=False)['price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='country',
                                       color= 'price', 
                                       hover_data=['price'],
                                       locationmode='country names',
                                       size='price',
                                       title= 'Average Price of properties in each Country',
                                       color_continuous_scale='Jet'
                            )
        st.plotly_chart(fig,use_container_width=True)