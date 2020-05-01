import googlemaps
import pandas


def calculate_minutes(time: str) -> str:
    time_list = time.split(' ')

    return str(int(time_list[0]) * 60 + int(time_list[2]))


def gettingMeta(file_edges: str, file_nodes: str) -> None:
    dfRoads = pandas.read_csv(file_edges)
    gmaps_key = googlemaps.Client(key='AIzaSyDScIaDPfz6I13UTfHuZLmYRI5uoPDVs2c')

    dfCity = pandas.read_csv(file_nodes)

    dfRoads['cityFrom'] = None
    dfRoads['cityTo'] = None

    for city in range(len(dfRoads)):
        cityFrom, cityTo = dfRoads.iat[city, 0], dfRoads.iat[city, 1]
        dfRoads.iat[city, 2] = dfCity.iat[cityFrom - 1, 1]
        dfRoads.iat[city, 3] = dfCity.iat[cityTo - 1, 1]
    dfRoads.to_csv(file_edges, index=False)

    dfRoads['time'] = None

    for i in range(len(dfRoads)):
        cityFrom = dfRoads.iat[i, 2]
        cityTo = dfRoads.iat[i, 3]
        try:
            duration = gmaps_key.distance_matrix(cityFrom, cityTo)['rows'][0]['elements'][0]['duration']['text']
            dfRoads.iat[i, 4] = calculate_minutes(duration)
        except:
            duration = None

    dfRoads.to_csv(file_edges, index=False)



