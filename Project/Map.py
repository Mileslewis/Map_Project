import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import netCDF4 as nc

def data_for_civ(height,width,seasonal = True,elevation = False, api_key = None):
    m = Map(height,width,hex_grid = True)

    if elevation:
        m.elevation_request_fill(precision = 0, api_key = api_key)
        m.plot_map("real elevation")
        m.to_csv("Civ5_Input_Data/real_elevation_" + str(height) + "x" + str(width) + "_hex.csv")

    summer = [3,4,5,6,7,8]
    winter = [0,1,2,9,10,11]

    if seasonal:
        n = from_nc("Good_Sources/air_ltm_1981-2010_monthly_144x73.nc",var_name= "air",start_mid = True,start_top=True, times = summer)
        m.sample(n)
        m.round(2)
        m.plot_map("real summer temps")
        m.to_csv("Civ5_Input_Data/real_temp_summer_" + str(height) + "x" + str(width) + "_hex.csv")

        n = from_nc("Good_Sources/air_ltm_1981-2010_monthly_144x73.nc",var_name= "air",start_mid = True,start_top=True, times = winter)
        m.sample(n)
        m.round(2)
        m.plot_map("real winter temps")
        m.to_csv("Civ5_Input_Data/real_temp_winter_" + str(height) + "x" + str(width) + "_hex.csv")

    n = from_nc("Good_Sources/air_ltm_1981-2010_monthly_144x73.nc",var_name= "air",start_mid = True,start_top=True)
    m.sample(n)
    m.round(2)
    m.plot_map("real temps")
    m.to_csv("Civ5_Input_Data/real_temp_" + str(height) + "x" + str(width) + "_hex.csv")

    if seasonal:
        n = from_nc("Good_Sources/precip_ltm_1981-2010_monthly_144x72.nc",var_name= "precip",start_mid = True,times = summer)
        m.sample(n)
        m.round(2)
        m.plot_map("real summer rain")
        m.to_csv("Civ5_Input_Data/real_rainfall_summer_" + str(height) + "x" + str(width) + "_hex.csv")

        n = from_nc("Good_Sources/precip_ltm_1981-2010_monthly_144x72.nc",var_name= "precip",start_mid = True,times = winter)
        m.sample(n)
        m.round(2)
        m.plot_map("real winter rain")
        m.to_csv("Civ5_Input_Data/real_rainfall_winter_" + str(height) + "x" + str(width) + "_hex.csv")

    n = from_nc("Good_Sources/precip_ltm_1981-2010_monthly_144x72.nc",var_name= "precip",start_mid = True)
    m.sample(n)
    m.round(2)
    m.plot_map("real rain")
    m.to_csv("Civ5_Input_Data/real_rainfall_" + str(height) + "x" + str(width) + "_hex.csv")
    return

def maps_from_civ(folder = "",all = False, geo = False):
    m = from_civ_map(folder + "elevationMap.csv")
    m.plot_map("Civ elevation")
    if all:
        m = from_civ_map(folder + "summerMap.csv")
        m.plot_map("Civ summerTemp")
        m = from_civ_map(folder + "winterMap.csv")
        m.plot_map("Civ winterTemp")

    m = from_civ_map(folder + "temperatureMap.csv")
    m.plot_map("Civ Temp")
    if all:
        m = from_civ_map(folder + "rainfallSummerMap.csv")
        m.plot_map("Civ summerRain")
        m = from_civ_map(folder + "rainfallWinterMap.csv")
        m.plot_map("Civ winterRain")
        if geo:
            m = from_civ_map(folder + "rainfallGeostrophicMap.csv")
            m.plot_map("Civ geoRain")

    m = from_civ_map(folder + "rainfallMap.csv")
    m.plot_map("Civ Rain")
    return

def from_nc(filepath, var_name, times = None, info = False, start_top = False, start_mid = False):
    ds = nc.Dataset(filepath)
    if info:
        print(ds)
        print(ds.__dict__)
    ds = ds[var_name]
    if times is not None:
        ds = ds[times]
    time = len(ds)
    height = len(ds[0])
    width = len(ds[0][0])
    fill_value = ds[0].fill_value
    array = ds[0]
    for t in range (1,time):
        array += ds[t]
    array = array / time
    data = []
    if start_top:
        for row in array.data[::-1]:
            if start_mid:
                for point in row[int(width/2):]:
                    data.append(point)
                for point in row[:int(width/2)]:
                    data.append(point)
            else:
                for point in row:
                    data.append(point)
    else:
        for row in array.data:
            if start_mid:
                for point in row[int(width/2):]:
                    data.append(point)
                for point in row[:int(width/2)]:
                    data.append(point)
            else:
                for point in row:
                    data.append(point)
    return Map(height,width,data,hex_grid = False,fill_value = fill_value)
    

def from_civ_map(filepath,fill_value = -999999):
    content = open(filepath).read()
    i = content.find(',')
    width = int(content[:i])
    content = content[i+1:]
    i = content.find(',')
    height = int(content[:i])
    content = content[i+1:].split(',')
    data = []
    data = [float(c) for c in content]
    return Map(height, width, data, hex_grid = True, fill_value=fill_value)

def from_csv(filepath, hex_grid = False, dimensions = True,fill_value = -999999, h = None, w = None):
    content = open(filepath).read()
    if dimensions == True:
        i = content.find('width')
        if i != -1:
            j = content[i:].find(",") + i
            width = int(content[i:j].lstrip("width: "))
        else:
            width = w

        i = content.find('height')
        if i != -1:
            j = content[i:].find(",") + i
            height = int(content[i:j].lstrip("height: "))
        else:
            height = h

        i = content.find('fillval')
        if i != -1:
            j = content[i:].find(",") + i
            f = float(content[i:j].lstrip("fillval: "))
        else:
            f = fill_value
        i = content.find("\n")
        content = content[i+1:]
    else:
        width = w
        height = h
        f = fill_value

    content = content.split(',')
    data = [float(c) for c in content]
    return Map(height,width,data,hex_grid, fill_value=f)
    

class Map:
    def __init__(self,h,w, data = None, hex_grid = False, fill_value = -999999):
        self.h = h
        self.w = w
        self.hex_grid = hex_grid
        self.fill_value = fill_value

        if data is None:
            self.data = np.ndarray(h*w)
            self.data.fill(0)
        else:
            self.data = np.array(data[:h*w])

        
        
    def width(self):
        return self.w
    def height(self):
        return self.h
    def length(self):
        return self.w * self.h

    def round(self, d = 0):
        self.data = self.data.round(d)

    def change_fill(self, f):
        for i,d in enumerate(self.data):
            if d == self.fill_value:
                self.data[i] = f
        self.fill_value = f
    
    def reverse(self):
        self.data = np.flip(self.data)

    def sample(self,sample_map):
        if not isinstance(sample_map,Map):
            print("need map to sample")
            return
        locations  = self.get_locations()
        lat_step, long_step = 180/sample_map.h, 360/sample_map.w
        for k,loc in enumerate(locations[0]):
            j = ((locations[0][k] + 90) % 180)/lat_step
            if sample_map.hex_grid:
                i = ((locations[1][k] + 180 - 0.5 * long_step) % 360)/long_step
            else:
                i = ((locations[1][k] + 180) % 360)/long_step
            self.data[k] = sample_map.data[int(i) + int(j) * int(sample_map.w)]
        self.fill_value = sample_map.fill_value

    def get_locations(self, decimal = 5):
        lats,longs = [],[]
        lat_step, long_step = 180/self.h, 360/self.w
        column = [-90 + (y + 0.5)*lat_step for y in range(self.h)]
        row = [-180 + x * long_step for x in range(self.w)]
        for j, lat in enumerate(column):
            for long in row:
                if j % 2 == 0 and self.hex_grid == True:
                    longs.append(round(long,decimal))
                else:
                    longs.append(round(long + 0.5 * long_step,decimal))
                lats.append(lat)
        return np.array([lats,longs])

    def locations_strings(self, max = 500):
        locations = self.get_locations()
        num_loc = len(locations[0])
        loc_strings = []
        n = 0
        loc_str = ""
        for i in range(num_loc):
            loc_str += str(locations[0][i])
            loc_str += ","
            loc_str += str(locations[1][i])
            n += 1
            if n >= max or i == num_loc - 1 :
                loc_strings.append(loc_str)
                loc_str = ""
                n = 0
            else:
                loc_str += "|"
        if len(loc_strings) > 200:
            print("over 200 requests")
            return "0|0"
        else:
            return loc_strings

    def elevation_request_fill(self,api_key = None,max = 500, precision = 3):

        if api_key is None:
            print("need api key")
            return

        payload={}
        headers = {}
        elevations = []

        loc_strings = self.locations_strings(max = max)
        for loc_str in loc_strings:
            url = "https://maps.googleapis.com/maps/api/elevation/json?locations=" + loc_str + "&key=" + api_key
        #print(url)

            response = requests.request("GET", url, headers=headers, data=payload)
            r = response.json()

            for item in r.get("results"):
                elevations.append(round(item.get("elevation"),precision))
        
        self.data = np.array(elevations[:self.h * self.w])


    def to_csv(self, filepath, mode = "w", dimensions = True):
        content = ""
        if dimensions == True:
            content += "width: " + str(self.w) + ", " + "height: " + str(self.h) + ", " + "fillval: " + str(self.fill_value)+ "," + "\n"
        for data in self.data:
            content += str(data) + ","
        f = open(filepath, mode)
        f.write(content[:-1])
        f.close()
    
    def plot_map(self, title = None,cmap = "viridis",type = None):
        locations = self.get_locations()
        na_vals = self.data == self.fill_value
 
        vals = self.data != self.fill_value
        if self.hex_grid == True:
            marker = "h"
        else:
            marker = "s"
        plt.scatter(locations[1][na_vals], locations[0][na_vals], s = 300000 / (self.h * self.w), marker = marker, c = "black")
        plt.scatter(locations[1][vals], locations[0][vals], s = 300000 / (self.h * self.w), marker = marker, c = self.data[vals],cmap = cmap)
        plt.colorbar(label = type)
        plt.xlabel("Longitude")
        plt.xticks([-180,-120,-60,0,60,120,180])
        plt.ylabel("Latitude")
        plt.yticks([-90,-60,-30,0,30,60,90])
        plt.title(title)
        plt.axis(xmin = -180,xmax = 180,ymin = -90,ymax = 90)
        #plt.axhline(c= "black",linestyle = "--",label = "equator")
        #plt.legend()

        plt.gcf().set_size_inches(12.8, 5.9)
        plt.tight_layout()

        plt.show()
