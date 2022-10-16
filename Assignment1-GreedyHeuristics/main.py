from utils import plot_cycle
from utils import read_data, to_dict
from algorithms import random_solution_iterate, nearest_neighbor_iterate, cycle_greedy_iterate
from time import perf_counter as ctime


if __name__ == "__main__":
    tspa, tspb = read_data()
    tspa_dic, tspb_dic = to_dict(tspa), to_dict(tspb)

    # random solution
    # min_cost, max_cost, avg_cost, random_points = random_solution_iterate(tspa_dic)
    # print("min_cost", min_cost)
    # print("max_cost", max_cost)
    # print("avg_cost", avg_cost)
    # print("The path:", random_points)
    # plot_cycle(random_points, tspa_dic, "rp.png")
    

    # nearest neighbor solution
    # min_cost, max_cost, avg_cost, nearest_points = nearest_neighbor_iterate(tspa_dic, include_costs=True)
    # print("min_cost", min_cost)
    # print("max_cost", max_cost)
    # print("avg_cost", avg_cost)
    # print("The path:", nearest_points)
    # plot_cycle(nearest_points, tspa_dic, "nn.png")
    

    # cycle greedy solution
    stime = ctime()
    min_cost, max_cost, avg_cost, cg_points = cycle_greedy_iterate(tspa_dic, include_costs=True)
    etime = ctime()
    print(f"Time taken: {etime - stime}s")
    print("min_cost", min_cost)
    print("max_cost", max_cost)
    print("avg_cost", avg_cost)
    print("The path:", cg_points)
    plot_cycle(cg_points, tspa_dic, "cg.png")
