import numpy as np
import pandas as pd
import random
import copy
import matplotlib.pyplot as plt
from utils import calculate_single_distance, calculate_min_costs, calculate_all_distances, calculate_cost, calculate_distances


def random_solution(starting_node, data, total_cost, chosen_nodes):
    """
    Next node is chosen randomly.
    """
    chosen_nodes.append(starting_node)
    while len(data) > 101:
        start_node = data.pop(starting_node)
        random_node = random.choice(list(data.keys()))
        end_node = data[random_node]
        dist = calculate_single_distance(start_node, end_node)
        total_cost.append(start_node['cost'])
        total_cost.append(dist)
        random_solution(random_node, data, total_cost, chosen_nodes)
    return sum(total_cost), chosen_nodes


def random_solution_iterate(data):
    """
    Start from each point and get min and max values and best set of nodes.
    """
    min_cost = np.inf
    max_cost = 0
    min_cost_nodes = []
    for i in range(len(data)):
        total_cost, chosen_nodes = random_solution(i, copy.deepcopy(data), total_cost = [], chosen_nodes = [])
        if total_cost < min_cost:
            min_cost = total_cost
            min_cost_nodes = chosen_nodes
        if total_cost > max_cost:
            max_cost = total_cost
    print(min_cost)
    print(max_cost)
    print(len(min_cost_nodes))
    print(min_cost_nodes)
    return min_cost_nodes


def nearest_neighbor(starting_node, data, all_costs: np.ndarray):
    all_costs[..., starting_node] = np.inf
    path = [starting_node]
    cost = data[starting_node]['cost']
    curr_id = starting_node
    
    for _ in range(99):
        min_index = all_costs[curr_id].argmin()
        min_value = all_costs[curr_id, min_index]
        all_costs[..., min_index] = np.inf
        cost += min_value
        path.append(min_index)
        curr_id = min_index
    return cost, path
    

def nearest_neighbor_iterate(data, include_costs=True):
    """
    Start from each point and get min and max values and best set of nodes.
    """
    min_cost = np.inf
    max_cost = 0
    min_cost_nodes = []
    all_distances = calculate_all_distances(data)
    all_costs_arr = np.array([data[i]['cost'] for i in data])  # TODO add it
    if include_costs:
        all_distances_with_costs = all_distances + all_costs_arr
    else:
        all_distances_with_costs = all_distances
    # min_costs = calculate_min_costs(all_distances_with_costs)
    # sorted_indices = all_distances_with_costs.argsort(axis=1)
    # sorted_indices = [i: list(sorted_indices[i]) for i in range(sorted_indices.shape[0])]
    for i in range(len(data)):
        total_cost, chosen_nodes = nearest_neighbor(i, copy.deepcopy(data), copy.deepcopy(all_distances_with_costs)) 
        total_cost += all_distances[i, chosen_nodes[-1]]
        if total_cost < min_cost:
            min_cost = total_cost
            min_cost_nodes = chosen_nodes
        if total_cost > max_cost:
            max_cost = total_cost
    print(min_cost)
    print(max_cost)
    print(min_cost_nodes)
    return min_cost, max_cost, min_cost_nodes


def cycle_greedy_old(first_node, nearest_node, data, all_distances):
    """
    Version that checks all points and all edges.
    """
    # cos nie dziala! zwraca 101 wyników zamiast 100, i koszty sie nie zgadzaja, ale wyglad obrazka ten sam
    # TODO remove whole function in future release
    total_cost = [all_distances[first_node, nearest_node] * 2]
    total_cost_dist = total_cost.copy()
    total_cost_cost = []
    chosen_nodes = [first_node, nearest_node]
    while len(data) > 101:
        mini = np.inf
        for n in range(len(chosen_nodes)-1):
            i = chosen_nodes[n]
            j = chosen_nodes[n+1]
            for new_node in list(data.keys()):
                i_next_dist = all_distances[i, new_node]
                j_next_dist = all_distances[new_node, j]
                insertion_dist = i_next_dist + j_next_dist - all_distances[i, j]
                if insertion_dist < mini:
                    mini = insertion_dist
                    indx = new_node
                    pos = n+1
        chosen_nodes.insert(pos, indx)
        total_cost.append(mini)
        total_cost.append(data.pop(indx)['cost'])
        total_cost_cost.append(total_cost[-1])
        total_cost_dist.append(mini)
    return sum(total_cost), chosen_nodes


def cycle_greedy(first_node, nearest_node, data, all_distances_with_costs):
    cost = 0
    cost += data[first_node]['cost']
    cost += data[nearest_node]['cost']
    cost += 2 * all_distances_with_costs[first_node, nearest_node]
    cycle = [first_node, nearest_node]
    chosen_nodes = {first_node, nearest_node}
    for _ in range(100-2):
        min_insertion_dist = np.inf
        min_insert_id = None
        min_new_node = None
        node_candidates = set(range(200)) - chosen_nodes
        for edge_id, edge in enumerate(zip(cycle[:-1], cycle[1:])):
            i, j = edge
            for new_node in node_candidates:
                edge0dist = all_distances_with_costs[i, new_node]
                edge1dist = all_distances_with_costs[j, new_node]
                insertion_dist = edge0dist + edge1dist - all_distances_with_costs[i, j]
                if insertion_dist < min_insertion_dist:
                    min_insertion_dist = insertion_dist
                    min_insert_id = edge_id + 1
                    min_new_node = new_node
        chosen_nodes.add(min_new_node)
        cycle.insert(min_insert_id, min_new_node)
        cost += min_insertion_dist
        cost += data[min_new_node]['cost']
    return cost, cycle


def cycle_greedy_iterate(data, include_costs=True):
    """
    Start from each point and get min and max values and best set of nodes.
    """
    min_cost = np.inf
    max_cost = 0
    min_cost_nodes = []
    all_distances = calculate_all_distances(data)
    all_costs_arr = np.array([data[i]['cost'] for i in data])  # TODO add it
    if include_costs:
        all_distances_with_costs = all_distances + all_costs_arr
    else:
        all_distances_with_costs = all_distances
    min_costs = calculate_min_costs(all_distances_with_costs)
    for i in range(10):  # TODO should be len(data)
        dat = copy.deepcopy(data)
        first_node = i
        nearest_node = min_costs[i][0]
        cost, cycle = cycle_greedy(first_node=first_node, nearest_node=nearest_node, data=dat, all_distances_with_costs=all_distances_with_costs)
        if cost < min_cost:
            min_cost = cost
            min_cost_nodes = cycle
        if cost > max_cost:
            max_cost = cost
    print(min_cost)
    print(max_cost)
    print(min_cost_nodes)
    return min_cost, max_cost, min_cost_nodes