from Map import Map

API_KEY = ""
m = Map(h = 40, w = 60, hex_grid = True)
m.elevation_request_fill(precision = 0, api_key = API_KEY)

m.plot_map("real elevation")