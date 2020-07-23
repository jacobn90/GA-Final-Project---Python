#!/usr/bin/env python
# coding: utf-8

# ## WALK - Sidewalks

# In[74]:


# new dataframe snyc
snyc = pd.read_csv("SIDEWALK.csv")


# In[75]:


snyc.head(10)


# In[76]:


# connvert data to float by getting rid of commas and periods
snyc['SHAPE_Leng'] = snyc['SHAPE_Leng'].apply(lambda x: x.replace(',', ''))
snyc['SHAPE_Leng'] = snyc['SHAPE_Leng'].apply(lambda x: float(x))


# In[77]:


snyc['SHAPE_Area'] = snyc['SHAPE_Area'].apply(lambda x: x.replace(',', ''))
snyc['SHAPE_Area'] = snyc['SHAPE_Area'].apply(lambda x: float(x))


# In[78]:


snyc['SHAPE_Leng'].head(5)


# In[98]:


# creating new value to define width or "comfort" of street
snyc['Comfort_dim'] = snyc['SHAPE_Area'] / snyc['SHAPE_Leng']


# In[99]:


snyc['Comfort_dim'].head(5)


# In[100]:


snyc['Comfort_dim'].max()


# In[101]:


snyc['Comfort_dim'].min()


# In[103]:


snyc['Comfort_dim'].mean()


# In[104]:


snyc['Comfort_dim'] = snyc['Comfort_dim'].astype("int")


# In[105]:


snyc['Comfort_Rating'] = (snyc['Comfort_dim']/8)*100


# In[108]:


snyc['Comfort_Rating'].max()


# In[114]:


snyc[snyc['Comfort_Rating'] == 0].head(10)


# In[113]:


snyc[snyc['Comfort_Rating'] == 0].info()


# In[127]:


snyc.head(20)


# ## Sidewalk shapes with Comfort Rating

# In[152]:


import geopandas as gpd
shapefile = 'geo_export_edb47a91-5dd7-4bee-bca0-2d1078658f7f.shp'
#Read shapefile using Geopandas
Sidewalks_geo = gpd.read_file(shapefile)
#Rename columns


# In[153]:


Sidewalk_map = Sidewalks_geo['geometry']


# In[156]:


import geopandas

gdf = geopandas.read_file('geo_export_edb47a91-5dd7-4bee-bca0-2d1078658f7f.shp')


# In[157]:


gdf


# In[148]:


Sidewalk_map['Comfort_Rating'] = snyc['Comfort_Rating']


# In[149]:


Sidewalk_map.head(5)


# In[189]:


gdf_color_good = snyc[snyc['Comfort_Rating'] >= 75]
gdf_color_medium = snyc[(snyc['Comfort_Rating'] >= 75) & (snyc['Comfort_Rating'] <= 50)]
gdf_color_bad = snyc[snyc['Comfort_Rating'] <= 50]
#['#C62828', '#C62828', '#283593', '#FF9800', '#283593']


# In[187]:


gdf_color_good.info(5)


# In[185]:


gdf_color_good['color'] = '#C62828'
gdf.plot(color=gdf['color'], figsize=(100,100)) 


# In[191]:


gdf_color_bad['color'] = '#fc4503'
gdf.plot(color=gdf['color'], figsize=(100,100))


# In[188]:


gdf_color_bad.info(5)


# In[190]:


gdf_color_medium['color'] = '283593'
gdf.plot(color=gdf['color'], figsize=(100,100))


# In[ ]:





# In[131]:


Sidewalk_map.plot(figsize=(100,100))


# In[136]:


import fiona
from shapely.geometry import shape
import numpy as np


# In[137]:


path = 'geo_export_edb47a91-5dd7-4bee-bca0-2d1078658f7f.shp' #your points
points = fiona.open(path)
Sidewalk_Shapes = [ shape(feat["geometry"]) for feat in points ]


# In[143]:


Sidewalk_Shapes[5]


# In[ ]:





# ## SHADE - Brooklyn Trees

# In[2]:


import pandas as pd
# Brooklyn Tree data from NYC open data
BK_Trees_NYC = pd.read_csv("Brooklyn_Trees.csv")


# In[3]:


BK_Trees_NYC.head(5)


# In[4]:


# tree species (common name) in Brooklyn
BK_Trees_NYC['spc_common'].head(10)


# In[ ]:


BK_Trees_NYC['spc_common']


# In[ ]:





# In[6]:


# 5 Most common tree species (common name) in Brooklyn
BK_Trees_NYC['spc_common'].value_counts()


# In[ ]:


#DV


# In[8]:


# List of NTA (Neighborhood Tabulation Areas) in Brooklyn i.e. Brooklyn neighborhoods
BK_Trees_NYC['nta_name'].value_counts()


# In[9]:


# DV


# ## Bedford Trees

# In[10]:


# isolating trees based on nta for neighborhood where i live
BK_Trees_NYC[BK_Trees_NYC['nta_name'] == 'Bedford']


# In[12]:


BT = BK_Trees_NYC['nta_name'] == 'Bedford' 


# In[13]:


Bedford_Trees = BK_Trees_NYC[BT]


# In[14]:


Bedford_Trees.head(5)


# In[16]:


Bedford_Trees.info()


# In[17]:


import gmaps
import gmaps.datasets
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
import fiona

geometry = [Point(xy) for xy in zip(Bedford_Trees.latitude, Bedford_Trees.longitude)]
crs = {'init': 'epsg:2263'} #http://www.spatialreference.org/ref/epsg/2263/
Trees_geo = GeoDataFrame(Bedford_Trees, crs=crs, geometry=geometry)


# In[20]:


new_york_coordinates = (40.689700, -73.947591)
figure_layout = {
    'width': '900px',
    'height': '900px',
    'border': '1px solid black',
    'padding': '1px'
}

gmaps.configure(api_key='AIzaSyCmXsdUPhYEiQYDFv3NQXBI-o4Jah-Ldvs')

Trees_geo = Trees_geo[['latitude', 'longitude']]

SW_layer = gmaps.symbol_layer(
    Trees_geo, fill_color='green', stroke_color='green', scale=2
)


# In[21]:


Sidewalk_map = gmaps.figure(center=new_york_coordinates, zoom_level=14, layout=figure_layout)
Sidewalk_map.add_layer(SW_layer)
Sidewalk_map


# ## Tree Density - Bedford, Brooklyn

# In[81]:


import pandas as pd


# In[82]:


B_Boundaries = pd.read_csv('nynta.csv')


# In[83]:


B_Boundaries.head(5)


# In[84]:


BSF = B_Boundaries['NTAName'] == 'Bedford'


# In[85]:


B_Boundaries['Shape_Area'] = B_Boundaries['Shape_Area'].apply(lambda x: x.replace(',', ''))
B_Boundaries['Shape_Area'] = B_Boundaries['Shape_Area'].apply(lambda x: float(x))


# In[86]:


B_Boundaries.head(5)


# In[89]:


B_Boundaries[B_Boundaries['NTAName'] == 'Bedford']['Shape_Area']


# In[208]:


ST = BK_Trees_NYC['nta_name'] == 'Stuyvesant Heights' 
Stuyvesant_Trees = BK_Trees_NYC[ST]

BF_TD = (len(Bedford_Trees))/(B_Boundaries[B_Boundaries['NTAName'] == 'Bedford']['Shape_Area'])
SH_TD = (len(Stuyvesant_Trees))/(B_Boundaries[B_Boundaries['NTAName'] == 'Stuyvesant Heights']['Shape_Area'])


# In[210]:


BF_TD


# In[211]:


SH_TD


# In[199]:


len(Bedford_Trees)


# In[200]:


B_Boundaries['NTAName'] == 'Stuyvesant Heights'


# In[203]:


ST = BK_Trees_NYC['nta_name'] == 'Stuyvesant Heights' 
Stuyvesant_Trees = BK_Trees_NYC[ST]


# In[204]:


BF_Area = B_Boundaries[B_Boundaries['NTAName'] == 'BedFord']['Shape_Area']
BF_Trees = len(Bedford_Trees)

SH_Area = B_Boundaries[B_Boundaries['NTAName'] == 'Stuyvesant Heights']['Shape_Area']
SH_Trees = len(Stuyvesant_Trees)


# In[ ]:




