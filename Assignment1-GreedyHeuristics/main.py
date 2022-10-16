from utils import plot_cycle
from utils import read_data, to_dict
from algorithms import random_solution_iterate, nearest_neighbor_iterate, cycle_greedy_iterate


if __name__ == "__main__":
    tspa, tspb = read_data()
    tspa_dic, tspb_dic = to_dict(tspa), to_dict(tspb)

    # random solution
    # min_cost, max_cost, avg_cost, random_points = random_solution_iterate(tspa_dic)
    # plot_cycle(random_points, tspa_dic)

    # nearest neighbor solution
    # min_cost, max_cost, avg_cost, nearest_points = nearest_neighbor_iterate(tspa_dic)
    # plot_cycle(nearest_points, tspa_dic)

    # cycle greedy solution
    min_cost, max_cost, avg_cost, nn_points = cycle_greedy_iterate(tspa_dic, include_costs=True)
    plot_cycle(nn_points, tspa_dic)
