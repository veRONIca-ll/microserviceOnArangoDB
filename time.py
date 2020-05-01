import googlemaps
import pandas


def gettingMeta(fileEdges: str, fileNodes: str) -> None:
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

    dfRoads['time'] = None

    for i in range(len(dfRoads)):
        cityFrom = dfRoads.iat[i, 2]
        cityTo = dfRoads.iat[i, 3]
        try:
            duration = gmaps_key.distance_matrix(cityFrom, cityTo)['rows'][0]['elements'][0]['duration']['text']
            dfRoads.iat[i, 5] = duration
        except:
            duration = None

    dfRoads.to_csv(fileEdges, index=False)