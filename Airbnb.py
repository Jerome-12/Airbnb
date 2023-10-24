import pandas as pd
import pymongo
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

import os
from dotenv import load_dotenv

load_dotenv()


client=pymongo.MongoClient(os.getenv("MONGOKEY"))

db=client['sample_airbnb']
col=db['listingsAndReviews']

data = []
for i in col.find( {}, {'_id':1,'listing_url':1,'name':1,'property_type':1,'room_type':1,'bed_type':1,
                        'minimum_nights':1,'maximum_nights':1,'cancellation_policy':1,'accommodates':1,
                        'bedrooms':1,'beds':1,'number_of_reviews':1,'bathrooms':1,'price':1,
                        'cleaning_fee':1,'extra_people':1,'guests_included':1,'images.picture_url':1,
                        'review_scores.review_scores_rating':1} ):
    data.append(i)

#print(data)    

df_1 = pd.DataFrame(data)
df_1['images'] = df_1['images'].apply(lambda x: x['picture_url'])
df_1['review_scores'] = df_1['review_scores'].apply(lambda x: x.get('review_scores_rating',0))
#print(df_1.head())

# print(df_1.isnull().sum())

df_1['bedrooms'].fillna(0, inplace=True)
df_1['beds'].fillna(0, inplace=True)
df_1['bathrooms'].fillna(0, inplace=True)
df_1['cleaning_fee'].fillna('Not Specified', inplace=True)
#print(df_1.isnull().sum())

#print(df_1.head())

# print(df_1.dtypes)

df_1['minimum_nights'] = df_1['minimum_nights'].astype(int)
df_1['maximum_nights'] = df_1['maximum_nights'].astype(int)
df_1['bedrooms'] = df_1['bedrooms'].astype(int)
df_1['beds'] = df_1['beds'].astype(int)
df_1['bathrooms'] = df_1['bathrooms'].astype(str).astype(float)
df_1['price'] = df_1['price'].astype(str).astype(float).astype(int)
df_1['cleaning_fee'] = df_1['cleaning_fee'].apply(lambda x: int(float(str(x))) if x != 'Not Specified' else 'Not Specified')
df_1['extra_people'] = df_1['extra_people'].astype(str).astype(float).astype(int)
df_1['guests_included'] = df_1['guests_included'].astype(str).astype(int)

# print(df_1.dtypes)

# print(df_1.describe().T)

# print(df_1.head())

host = []
for i in col.find( {}, {'_id':1, 'host':1}):
    host.append(i)

df_host = pd.DataFrame(host)
host_keys = list(df_host.iloc[0,1].keys())
host_keys.remove('host_about')

for i in host_keys:
    if i == 'host_response_time':
        df_host['host_response_time'] = df_host['host'].apply(lambda x: x['host_response_time'] if 'host_response_time' in x else 'Not Specified')
    else:
        df_host[i] = df_host['host'].apply(lambda x: x[i] if i in x and x[i]!='' else 'Not Specified')

df_host.drop(columns=['host'], inplace=True)

# print(df_host.head())

df_host['host_is_superhost'] = df_host['host_is_superhost'].map({False:'No',True:'Yes'})
df_host['host_has_profile_pic'] = df_host['host_has_profile_pic'].map({False:'No',True:'Yes'})
df_host['host_identity_verified'] = df_host['host_identity_verified'].map({False:'No',True:'Yes'})

# print(df_host.head())

# print(df_host.isnull().sum())

# print(df_host.dtypes)

address = []
for i in col.find( {}, {'_id':1, 'address':1}):
    address.append(i)

df_address = pd.DataFrame(address)
address_keys = list(df_address.iloc[0,1].keys())

for i in address_keys:
    if i == 'location':
        df_address['location_type'] = df_address['address'].apply(lambda x: x['location']['type'])
        df_address['longitude'] = df_address['address'].apply(lambda x: x['location']['coordinates'][0])
        df_address['latitude'] = df_address['address'].apply(lambda x: x['location']['coordinates'][1])
        df_address['is_location_exact'] = df_address['address'].apply(lambda x: x['location']['is_location_exact'])
    else:
        df_address[i] = df_address['address'].apply(lambda x: x[i] if x[i]!='' else 'Not Specified')

df_address.drop(columns=['address'], inplace=True)

# print(df_address.head())

df_address['is_location_exact'] = df_address['is_location_exact'].map({False:'No',True:'Yes'})

# print(df_address.head())

# print(df_address.isnull().sum())

# print(df_address.dtypes)

availability = []
for i in col.find( {}, {'_id':1, 'availability':1}):
    availability.append(i)

df_availability = pd.DataFrame(availability)
availability_keys = list(df_availability.iloc[0,1].keys())

for i in availability_keys:
    df_availability['availability_30'] = df_availability['availability'].apply(lambda x: x['availability_30'])
    df_availability['availability_60'] = df_availability['availability'].apply(lambda x: x['availability_60'])
    df_availability['availability_90'] = df_availability['availability'].apply(lambda x: x['availability_90'])
    df_availability['availability_365'] = df_availability['availability'].apply(lambda x: x['availability_365'])

df_availability.drop(columns=['availability'], inplace=True)

# print(df_availability.head())

# print(df_availability.isnull().sum())

# print(df_availability.dtypes)

def amenities_sort(x):
    a = x
    a.sort(reverse=False)
    return a

amenities = []
for i in col.find( {}, {'_id':1, 'amenities':1}):
    amenities.append(i)

df_amenities = pd.DataFrame(amenities)
df_amenities['amenities'] = df_amenities['amenities'].apply(lambda x: amenities_sort(x))

# print(df_amenities.head())

# print(df_amenities.isnull().sum())
# print(df_amenities.dtypes)

df = pd.merge(df_1, df_host, on='_id')
df = pd.merge(df, df_address, on='_id')
df = pd.merge(df, df_availability, on='_id')
df = pd.merge(df, df_amenities, on='_id')

# print(df.head())
# print(df.dtypes)

# print(df)

#df.to_csv('airbnb_excel.csv')

#Connect to sql

mydb= mysql.connector.connect(
    host='localhost',
    user='root',
    port='3306',
    password=os.getenv("MYSQLKEY"),
    database='Airbnb',
    auth_plugin = "mysql_native_password"

)

cursor=mydb.cursor()



engine = create_engine(os.getenv("MYSQLSRC"), echo=False)

# connect to sql

df.to_sql('airbnb_db',engine,if_exists='replace',index=False,
                     dtype={"_id" : sqlalchemy.types.VARCHAR(length=100),
                            "listing_url": sqlalchemy.types.TEXT,
                            "name" : sqlalchemy.types.VARCHAR(length=200),
                            "property_type" : sqlalchemy.types.VARCHAR(length=255),
                            "room_type" : sqlalchemy.types.VARCHAR(length=255),
                            "bed_type" : sqlalchemy.types.VARCHAR(length=255),
                            "minimum_nights" : sqlalchemy.types.Integer,
                            "maximum_nights" : sqlalchemy.types.Integer,
                            "cancellation_policy" : sqlalchemy.types.VARCHAR(length=255),
                            "accommodates" : sqlalchemy.types.Integer,
                            "bedrooms" : sqlalchemy.types.Integer,
                            "beds" : sqlalchemy.types.Integer,
                            "number_of_reviews" : sqlalchemy.types.Integer,
                            "bathrooms" : sqlalchemy.types.FLOAT,
                            "price" : sqlalchemy.types.Integer,
                            "extra_people" : sqlalchemy.types.Integer,
                            "guests_included" : sqlalchemy.types.Integer,
                            "images": sqlalchemy.types.TEXT,
                            "review_scores" : sqlalchemy.types.Integer,
                            "cleaning_fee" : sqlalchemy.types.VARCHAR(length=20),
                            "host_id" : sqlalchemy.types.VARCHAR(length=255),
                            "host_url": sqlalchemy.types.TEXT,
                            "host_name" : sqlalchemy.types.VARCHAR(length=255),
                            "host_location" : sqlalchemy.types.VARCHAR(length=255),
                            "host_thumbnail_url": sqlalchemy.types.TEXT,
                            "host_picture_url": sqlalchemy.types.TEXT,
                            "host_neighbourhood" : sqlalchemy.types.VARCHAR(length=255),
                            "host_is_superhost" : sqlalchemy.types.VARCHAR(length=50),
                            "host_has_profile_pic" : sqlalchemy.types.VARCHAR(length=50),
                            "host_identity_verified" : sqlalchemy.types.VARCHAR(length=50),
                            "host_listings_count" : sqlalchemy.types.Integer,
                            "host_total_listings_count" : sqlalchemy.types.Integer,
                            "host_verification": sqlalchemy.types.TEXT,
                            "street" : sqlalchemy.types.VARCHAR(length=255),
                            "suburb" : sqlalchemy.types.VARCHAR(length=255),
                            "government_area" : sqlalchemy.types.VARCHAR(length=255),
                            "market" : sqlalchemy.types.VARCHAR(length=255),
                            "country" : sqlalchemy.types.VARCHAR(length=255),
                            "country_code" : sqlalchemy.types.VARCHAR(length=255),
                            "location_type" : sqlalchemy.types.VARCHAR(length=255),
                            "longitude" : sqlalchemy.types.FLOAT,
                            "latitude" : sqlalchemy.types.FLOAT,
                            "is_location_exact" : sqlalchemy.types.VARCHAR(length=255),
                            "availability_30" : sqlalchemy.types.Integer,
                            "availability_60" : sqlalchemy.types.Integer,
                            "availability_90" : sqlalchemy.types.Integer,
                            "availability_365" : sqlalchemy.types.Integer,
                            'amenities': sqlalchemy.types.TEXT})

# Close the cursor and database connection

cursor.close()
mydb.close()