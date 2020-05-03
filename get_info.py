import googlemaps
import pandas


def calculate_minutes(time: str) -> str:
    time_list = time.split(' ')
    return str(int(time_list[0]) * 60 + int(time_list[2]))


def only_km(distance: str) -> str:
    distance_list = distance.split(' ')
    if distance_list[0].find(',') != -1:
        return distance_list[0].replace(',', '')
    return distance_list[0]


def getting_meta(fileEdges: str, fileNodes: str) -> None:
    dfRoads = pandas.read_csv(fileEdges)
    gmaps_key = googlemaps.Client(key='api-key')

    dfCity = pandas.read_csv(fileNodes)

    dfRoads['cityFrom'] = None
    dfRoads['cityTo'] = None

    for city in range(len(dfRoads)):
        cityFrom, cityTo = dfRoads.iat[city, 0], dfRoads.iat[city, 1]
        dfRoads.iat[city, 2] = dfCity.iat[cityFrom - 1, 1]
        dfRoads.iat[city, 3] = dfCity.iat[cityTo - 1, 1]
    dfRoads.to_csv(fileEdges, index=False)

    dfRoads['distance'] = None
    dfRoads['time'] = None

    for i in range(len(dfRoads)):
        cityFrom = dfRoads.iat[i, 2]
        cityTo = dfRoads.iat[i, 3]
        try:
            distance = gmaps_key.distance_matrix(cityFrom, cityTo)['rows'][0]['elements'][0]['distance']['text']
            duration = gmaps_key.distance_matrix(cityFrom, cityTo)['rows'][0]['elements'][0]['duration']['text']
            dfRoads.iat[i, 4] = only_km(distance)
            dfRoads.iat[i, 5] = calculate_minutes(duration)
        except:
            distance = None
            duration = None

    dfRoads.to_csv(fileEdges, index=False)

