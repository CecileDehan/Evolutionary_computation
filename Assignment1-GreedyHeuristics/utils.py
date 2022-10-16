import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_data():
    colnames = ['x', 'y', 'cost']
    TSPA = pd.read_csv('data/TSPA.csv', header=None, sep=';', names=colnames)
    TSPB = pd.read_csv('data/TSPB.csv', header=None, sep=';', names=colnames)
    return TSPA, TSPB


def to_dict(data):
    return data.to_dict('index')


def calculate_distances(node, data):
    """
    Calculate Euclidean distances from a given node to all available nodes.
    """
    distances = {}
    starting_cords = np.array([node['x'], node['y']])
    for key in data.keys():
        ending_cords = np.array([data[key]['x'], data[key]['y']])
        dist = round(np.linalg.norm(starting_cords - ending_cords))
        distances[key] = dist
    return distances


def calculate_single_distance(starting_node, ending_node):
    """
    Calculate Euclidean distances between two nodes.
    """
    starting_cords = np.array([starting_node['x'], starting_node['y']])
    ending_cords = np.array([ending_node['x'], ending_node['y']])
    dist = round(np.linalg.norm(starting_cords - ending_cords))
    return dist


def calculate_all_distances(data_dic):
    all_distances = np.empty((200,200))
    for i in range(200):
        for j in range(i + 1, 200):
            dist = calculate_single_distance(data_dic[i], data_dic[j])
            all_distances[i][j] = dist
            all_distances[j][i] = dist
    for i in range(200):
        all_distances[i][i] = np.inf
    return all_distances


def calculate_min_costs(all_costs):
    min_costs = dict()
    for i in range(all_costs.shape[0]):
        min_id = all_costs[i].argmin()
        min_costs[i] = (min_id, all_costs[i, min_id])
    return min_costs


def calculate_cost(cycle, data: dict):
    if type(cycle[0]) == int:
        cycle = [data[i] for i in cycle]
    allcost = 0.
    allcost += sum([calculate_single_distance(cycle[i], cycle[(i+1) % len(cycle)]) for i in range(len(cycle))])
    allcost += sum([i['cost'] for i in cycle])
    return allcost


def plot_cycle(points, data_dic):
    plt.rcParams["figure.figsize"] = (20,20)
    chosen_points_x = [data_dic[k]['x'] for k in points]
    chosen_points_x.append(chosen_points_x[0])
    chosen_points_y = [data_dic[k]['y'] for k in points]
    chosen_points_y.append(chosen_points_y[0])
    costs = [data_dic[k]['cost']/25 for k in points]
    costs.append(costs[0])
    plt.plot(chosen_points_x, chosen_points_y)
    plt.scatter(chosen_points_x, chosen_points_y, s=costs)
    plt.show()
