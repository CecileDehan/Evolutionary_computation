from utils import plot_cycle
from utils import read_data, to_dict
from algorithms import nearest_neighbor_iterate, cycle_greedy_iterate


if __name__ == "__main__":
    tspa, tspb = read_data()
    tspa_dic, tspb_dic = to_dict(tspa), to_dict(tspb)
    min_cost, max_cost, nn_points = cycle_greedy_iterate(tspa_dic, include_costs=True)
    plot_cycle(nn_points, tspa_dic)
