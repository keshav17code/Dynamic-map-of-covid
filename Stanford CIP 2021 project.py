import pandas as pd
import geopandas as gpd
import PIL
import io

#Reading in the csv data
data = pd.read_csv('D:/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

#Group the data by the country
data = data.groupby('Country/Region').sum()

# Drop Lat Lon columns
data = data.drop(columns = ['Lat','Long'])
 
#Create a transpose of the dataframe
data_trandposed = data.T
data_trandposed.plot(y = ['India', 'China', 'US', 'Japan' ], use_index = True, figsize  = (8,10), marker = '*')


# Read in the world map shapefile
world = gpd.read_file(r'C:\Users\Keshav\Desktop\Final project dynamic map\World_Map.shp')

world.replace('Viet Nam', 'Vietnam', inplace = True)
world.replace('Brunei Darusalam', 'Brunei', inplace = True)
world.replace('Democrartic Republic of the congo', 'Congo (Kinshasa)', inplace = True)
world.replace('Cape Verde', 'Cabo Verde', inplace = True)
world.replace('Congo', 'Congo (Brazzaville)', inplace = True)
world.replace('Czech Republic', 'Czechia', inplace = True)
world.replace('Swazilade', 'Eswatini', inplace = True)
world.replace('Iran (Islamic Republic of)', 'Iran', inplace = True)
world.replace('Korea,Republic of','Korea, South', inplace = True)
world.replace("Lao People's Democratic Republic", 'Laos', inplace = True)
world.replace('Libyan Arab Jamahiriya', 'Libya', inplace = True)
world.replace('Republic of Molodova', 'Moldova', inplace = True)
world.replace('The former Yugoslav Republic of Macedonia', 'North Macedonia', inplace = True)
world.replace('Syrian Arab Republic', 'Syria', inplace = True)
world.replace('Taiwan', 'Taiwan*', inplace = True)
world.replace('United Republic of Tanzania', 'Tanzania', inplace = True)
world.replace('United States', 'US', inplace = True)
world.replace('Palestine', 'Vietnam', inplace = True)

#Merging the 'data' with 'world'geopandas geodataframe
merge = world.join(data, on = 'NAME', how = 'right')

image_frames = []
for dates in merge.columns.to_list()[2:494]:

    #Plot
    ax = merge.plot(column = dates,
                    cmap = 'OrRd',
                    figsize = (14,14),
                    legend = True,
                    scheme = 'user_defined',
                    classification_kwds = {'bins':[10,20,50,100,500,1000,5000,10000,500000]},
                    edgecolor = 'black',
                    linewidth = 0.4)
    
    #Add a title to the map
    ax.set_title('Total Confirmed Coronavirus cases:'+ dates,fontdict = 
                 {'fontsize':17},pad = 12.5)    
    
    # Removing the axis
    ax.set_axis_off()
    
    # Move the legend
    ax.get_legend().set_bbox_to_anchor((0.18, 0.6))
    
    img = ax.get_figure()
    
    f = io.BytesIO()
    img.savefig(f,format = 'png', bbox_inches = 'tight')
    f.seek(0)
    image_frames.append(PIL.Image.open(f))
    

#Create a GIF animation
image_frames[0].save('Dynamic Covid-19 cases till second wave map.gif',format = 'GIF',
                     append_images = image_frames[1:],
                     save_all = True, duration = 300,
                     loop = 2)
f.close()