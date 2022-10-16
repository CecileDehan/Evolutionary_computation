from xml.etree.ElementInclude import include
import numpy as np
import random
import copy
from utils import calculate_min_costs, calculate_all_distances


def random_solution(starting_node, data, distances):
    cost = 0
    chosen_nodes = []
    lst = list(range(200))
    lst.pop(starting_node)
    random.shuffle(lst)
    chosen_nodes.append(starting_node)
    i = 0
    for n in lst[:99]:
        start_node = chosen_nodes[i]
        cost += data[start_node]['cost']
        dist = distances[start_node, n]
        cost += dist
        chosen_nodes.append(n)
        i += 1
    last_node = chosen_nodes[-1]
    cost += data[last_node]['cost']
    dist = distances[last_node, chosen_nodes[0]]
    cost += dist
    return cost, chosen_nodes

def random_solution_iterate(data):
    """
    Start from each point and get min and max values and best set of nodes.
    """
    distances = calculate_all_distances(data)
    min_cost = np.inf
    max_cost = 0
    min_cost_nodes = []
    all_costs = []
    for i in range(len(data)):
        total_cost, chosen_nodes = random_solution(i, data, distances)
        all_costs.append(total_cost)
        if total_cost < min_cost:
            min_cost = total_cost
            min_cost_nodes = chosen_nodes
        if total_cost > max_cost:
            max_cost = total_cost
    avg_cost = round(sum(all_costs)/len(all_costs))
    return min_cost, max_cost, avg_cost, min_cost_nodes


def nearest_neighbor(starting_node, data, all_costs: np.ndarray, costs_included: bool):
    all_costs[..., starting_node] = np.inf
    path = [starting_node]
    if costs_included:
        cost = data[starting_node]['cost']
    else:
        cost = 0.
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
    all_costs = []
    all_distances = calculate_all_distances(data)
    all_costs_arr = np.array([data[i]['cost'] for i in data])
    if include_costs:
        all_distances_with_costs = all_distances + all_costs_arr
    else:
        all_distances_with_costs = all_distances
    for i in range(1):  #TODO
        total_cost, chosen_nodes = nearest_neighbor(i, data, copy.deepcopy(all_distances_with_costs), costs_included=include_costs)
        total_cost += all_distances[i, chosen_nodes[-1]]

        if not include_costs:
            total_cost += sum(data[i]["cost"] for i in chosen_nodes)

        all_costs.append(total_cost)
        if total_cost < min_cost:
            min_cost = total_cost
            min_cost_nodes = chosen_nodes
        if total_cost > max_cost:
            max_cost = total_cost
    avg_cost = round(sum(all_costs)/len(all_costs))
    return min_cost, max_cost, avg_cost, min_cost_nodes


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
    all_costs = []
    all_distances = calculate_all_distances(data)
    all_costs_arr = np.array([data[i]['cost'] for i in data])  # TODO add it
    if include_costs:
        all_distances_with_costs = all_distances + all_costs_arr
    else:
        all_distances_with_costs = all_distances
    min_costs = calculate_min_costs(all_distances_with_costs)
    for i in range(len(data)):#range(10):  # TODO should be len(data)
        dat = copy.deepcopy(data)
        first_node = i
        nearest_node = min_costs[i][0]
        cost, cycle = cycle_greedy(first_node=first_node, nearest_node=nearest_node, data=dat, all_distances_with_costs=all_distances_with_costs)
        all_costs.append(cost)
        if cost < min_cost:
            min_cost = cost
            min_cost_nodes = cycle
        if cost > max_cost:
            max_cost = cost
    avg_cost = round(sum(all_costs)/len(all_costs))
    return min_cost, max_cost, avg_cost, min_cost_nodes
