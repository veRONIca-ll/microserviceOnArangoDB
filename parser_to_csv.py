from get_info import getting_meta


def change_to_space(names: list) -> list:
    without_comas = []
    for name in names:
        name = ' '.join(name.split(','))
        without_comas.append(name)

    return without_comas


# with open('ent.subelj_euroroad_euroroad.city.name') as file:
#     cities = change_to_space(list(file.read().split('\n')))
#     cities.remove('')
#
#
# with open('city.csv', 'w') as nodes_file:
#     nodes_file.write('_key,name\n')
#     for i in range(len(cities)):
#         nodes_file.write(str(i + 1) + ',' + cities[i] + '\n')

with open('out.subelj_euroroad_euroroad') as file:
    data = file.read().split('\n')

with open('way.csv', 'w') as edge_file:
    edge_file.write('_to,_from\n')
    for way in data:
        edge_file.write(','.join(way.split(' ')) + '\n')

getting_meta('way.csv', 'city.csv')