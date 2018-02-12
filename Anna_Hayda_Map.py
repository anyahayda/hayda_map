import folium
from geopy.geocoders import ArcGIS


def read_file(path):
    """
    (str) -> (list)
    Open file and create a list of lists
    """
    with open(path, encoding='utf-8', errors='ignore') as loc_file:
        loc_file = loc_file.readlines()
        lst = [line.strip().split('\t') for line in loc_file]
        return lst


def years_loc(lines_list, year):
    """
    (list, int) -> (list)
    The function takes the list of lists and return the list of their
    locations
    """
    year = '(' + str(year) + ')'
    lst2 = []
    for i in lines_list:
        if year in i[0]:
            lst2.append(i[-1])
    return lst2



def coordinates(lst_loc):
    """
    (list)->list)
    The function takes the list of locations and return the list of their
    coordinates
    """
    lst = []
    geo = ArcGIS()
    for i in lst_loc:
        try:
            loc = geo.geocode(i)
            loc1 = [loc.latitude, loc.longitude]
            lst.append(loc1)
        except:
            pass
    return lst


def map():
    """
    (None) -> map
    Create a HTML map
    """
    return folium.Map()


def point():
    """
    (int) -> (None)
    The function put points into the map and make the map coloured
    according to countries' population
    """
    map1 = map()
    lst = coordinates(years_loc(read_file("locations.txt"), 1895))
    films = folium.FeatureGroup(name='Films')
    for i in lst:
        films.add_child(folium.Marker(location=i,
                                      icon=folium.Icon()))

    population = folium.FeatureGroup(name="Population")
    population.add_child(folium.GeoJson(data=open('world.json', 'r',
                                                  encoding='utf-8-sig').read(),
                                        style_function=lambda x: {
                                            'fillColor': 'green'
                                            if x['properties'][
                                                   'POP2005'] < 10000000
                                            else 'red' if 10000000 <=
                                                          x['properties'][
                                                              'POP2005'] < 20000000
                                            else 'black'}))
    map1.add_child(population)
    map1.add_child(films)
    map1.add_child(folium.LayerControl())
    map1.save("map_lab.html")


point()
