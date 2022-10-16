from utils import calculate_cost
from utils import plot_cycle
from utils import read_data, to_dict
from algorithms import random_solution_iterate, nearest_neighbor_iterate, cycle_greedy_iterate
from time import perf_counter as ctime


if __name__ == "__main__":
    tspa, tspb = read_data()
    tspa_dic, tspb_dic = to_dict(tspa), to_dict(tspb)

    data_dic = tspa_dic

    # random solution
    print("random solution...")
    min_cost, max_cost, avg_cost, random_points = random_solution_iterate(data_dic)
    print("min_cost", min_cost)
    print("max_cost", max_cost)
    print("avg_cost", avg_cost)
    print("The path:", random_points)
    plot_cycle(random_points, data_dic, "rp.png")
    print(f"sanity check, the min cost again: {calculate_cost(random_points, data_dic)}")
    

    # nearest neighbor solution
    print("nearest neighbor...")
    min_cost, max_cost, avg_cost, nearest_points = nearest_neighbor_iterate(data_dic, include_costs=True)
    print("min_cost", min_cost)
    print("max_cost", max_cost)
    print("avg_cost", avg_cost)
    print("The path:", nearest_points)
    plot_cycle(nearest_points, data_dic, "nn.png")
    print(f"sanity check, the min cost again: {calculate_cost(nearest_points, data_dic)}")
    

    # cycle greedy solution
    print("cycle greedy...")
    stime = ctime()
    min_cost, max_cost, avg_cost, cg_points = cycle_greedy_iterate(data_dic, include_costs=True)
    etime = ctime()
    print(f"Time taken: {etime - stime}s")
    print("min_cost", min_cost)
    print("max_cost", max_cost)
    print("avg_cost", avg_cost)
    print("The path:", cg_points)
    plot_cycle(cg_points, data_dic, "cg.png")
    print(f"sanity check, the min cost again: {calculate_cost(cg_points, data_dic)}")
