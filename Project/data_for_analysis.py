from Map import Map, from_civ_map, from_csv, from_nc
import numpy as np
import pandas as pd

def data_for_analysis(height,width,filepath = "",elevation = False):

    e = Map(height,width)
    if elevation:
        e.elevation_request_fill(precision = 0)
        e.plot_map("real elevation")

    summer = [3,4,5,6,7,8]
    winter = [0,1,2,9,10,11]

    t = Map(height,width)
    n = from_nc("Good_Sources/air_ltm_1981-2010_monthly_144x73.nc",var_name= "air",start_mid = True,start_top=True, times = summer)
    t.sample(n)
    t.plot_map("real summer temps")

    r = Map(height,width)
    n = from_nc("Good_Sources/precip_ltm_1981-2010_monthly_144x72.nc",var_name= "precip",start_mid = True,times = summer)
    r.sample(n)
    r.plot_map("real summer rain")

    locations = t.get_locations()
    df = pd.DataFrame({"lat":locations[0],"long":locations[1],"elevation":e.data,"temp":t.data,"rain":r.data})
    df.to_csv(filepath + "summer.csv")

    n = from_nc("Good_Sources/air_ltm_1981-2010_monthly_144x73.nc",var_name= "air",start_mid = True,start_top=True, times = winter)
    t.sample(n)
    t.plot_map("real winter temps")

    n = from_nc("Good_Sources/precip_ltm_1981-2010_monthly_144x72.nc",var_name= "precip",start_mid = True,times = winter)
    r.sample(n)
    r.plot_map("real winter rain")

    df = pd.DataFrame({"lat":locations[0],"long":locations[1],"elevation":e.data,"temp":t.data,"rain":r.data})
    df.to_csv(filepath + "winter.csv")

    n = from_nc("Good_Sources/air_ltm_1981-2010_monthly_144x73.nc",var_name= "air",start_mid = True,start_top=True)
    t.sample(n)
    t.plot_map("real temps")

    n = from_nc("Good_Sources/precip_ltm_1981-2010_monthly_144x72.nc",var_name= "precip",start_mid = True)
    r.sample(n)
    r.plot_map("real rain")

    df = pd.DataFrame({"lat":locations[0],"long":locations[1],"elevation":e.data,"temp":t.data,"rain":r.data})
    df.to_csv(filepath + "year.csv")

    return

data_for_analysis(72,144,"Spare/")

