import time
import matplotlib.pyplot as plt
import networkx as nx
import random
import Algorithm
import numpy as np

# Danh sách mở rộng đã đề cập
sizes = [
    (4, 3),(5, 4), (6, 5), (7, 6),(8, 7),(9, 8),(10, 10),(11, 12),(12, 14),(13, 15),
    (14, 17),(15, 20),(16, 22),(17, 25),(18, 28),(19, 30),(20, 33),(21, 36)
]


nodes, edges = zip(*sizes)

num_trials = 20

# Tạo các dict để lưu thời gian và số màu trung bình
algorithms = ["BruteForce", "backtracking"]
time_results = {algo: [] for algo in algorithms}
color_counts = {algo: [] for algo in algorithms}

def generate_random_graph(num_nodes, num_edges):
    G = nx.Graph()
    edges = set()
    while len(edges) < num_edges:
        u = random.randint(1, num_nodes)
        v = random.randint(1, num_nodes)
        if u != v:
            edge = (min(u, v), max(u, v))
            edges.add(edge)
    G.add_edges_from(edges)
    return G

for n, m in sizes:
    print(f"Xử lý ({n} đỉnh, {m} cạnh)...")

    trial_times = {algo: [] for algo in algorithms}
    trial_colors = {algo: [] for algo in algorithms}

    for _ in range(num_trials):
        G = generate_random_graph(n, m)

        # --- BruteForce ---
        if n <= 12:
            start = time.time()
            result, num_color = Algorithm.brute_force_coloring(G)
            elapsed = (time.time() - start) * 1000
            trial_times["BruteForce"].append(elapsed)
            trial_colors["BruteForce"].append(len(set(result.values())))
        else:
            trial_times["BruteForce"].append(None)
            trial_colors["BruteForce"].append(None)

        # --- backtracking ---
        start = time.time()
        result, num_colors = Algorithm.color_backtracking(G)
        elapsed = (time.time() - start) * 1000
        trial_times["backtracking"].append(elapsed)
        trial_colors["backtracking"].append(len(set(result.values())))

    # Trung bình sau 20 lần
    for algo in algorithms:
        times = [t for t in trial_times[algo] if t is not None]
        colors = [c for c in trial_colors[algo] if c is not None]
        time_results[algo].append(sum(times) / len(times) if times else None)
        color_counts[algo].append(sum(colors) / len(colors) if colors else None)


print(f"BruteForce - Số màu sử dụng: {color_counts["BruteForce"]}, thời gian: {time_results["BruteForce"]}ms")
print(f"backtracking - Số màu sử dụng: {color_counts["backtracking"]}, thời gian: {time_results["backtracking"]}ms")
