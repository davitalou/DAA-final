import time
import matplotlib.pyplot as plt
import networkx as nx
import random
import Algorithm
import numpy as np

#Mật độ thấp ~0.2
sizes = [
    (100, 990), (200, 3980), (300, 8970), (400, 15960), (500, 24950),
#     (600, 35990), (700, 48230), (800, 61700), (900, 76410), (1000, 92410),
#     (1200, 132360), (1500, 224950)
]
#Mật độ thấp ~0.6
# sizes = [
#     # (100, 1980), (200, 7960), (300, 17940), (400, 31920), (500, 49900),
#     # (600, 71980), (700, 96510),
#     #   (800, 123400), (900, 152820), (1000, 184820),
#     # (1200, 264720), (1500, 449900)
# ]

#     (6000, 110000), (6500, 123000), (7000, 137000)

nodes, edges = zip(*sizes)

# Nội suy (interpolation) để có khoảng 150 phần tử
num_points = 70
new_nodes = np.linspace(min(nodes), max(nodes), num=num_points, dtype=int)
new_edges = np.interp(new_nodes, nodes, edges).astype(int)

# Tạo lại danh sách sizes mới
sizes = list(zip(new_nodes, new_edges))

num_trials = 20

# Tạo các dict để lưu thời gian và số màu trung bình
algorithms = ["Welsh-Powell", "DSATUR"]
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

        # --- Welsh-Powell ---
        start = time.time()
        result = Algorithm.color_welsh_powell(G)
        elapsed = (time.time() - start) * 1000
        trial_times["Welsh-Powell"].append(elapsed)
        trial_colors["Welsh-Powell"].append(len(set(result.values())))

        # --- DSATUR ---
        start = time.time()
        result = Algorithm.color_dsatur(G)
        elapsed = (time.time() - start) * 1000
        trial_times["DSATUR"].append(elapsed)
        trial_colors["DSATUR"].append(len(set(result.values())))

    # Lấy trung bình sau 20 lần
    for algo in algorithms:
        time_results[algo].append(sum(trial_times[algo]) / num_trials)
        color_counts[algo].append(sum(trial_colors[algo]) / num_trials)

# --- Vẽ biểu đồ gộp số màu và thời gian ---
x_labels = [n for (n, _) in sizes]
fig, ax1 = plt.subplots(figsize=(12, 5))

# Biểu đồ thời gian (y1)
for algo in algorithms:
    ax1.plot(x_labels, time_results[algo], label=f"{algo} (Thời gian)", linestyle='-', color=f"C{algorithms.index(algo)}")
ax1.set_xlabel("Số đỉnh")
ax1.set_ylabel("Thời gian trung bình (ms)", color="black")
ax1.tick_params(axis='y', labelcolor="black")

# Tạo trục phụ (y2) cho số màu
ax2 = ax1.twinx()
for algo in algorithms:
    ax2.plot(x_labels, color_counts[algo], label=f"{algo} (Số màu)", linestyle='--', color=f"C{algorithms.index(algo)}")
ax2.set_ylabel("Số màu trung bình", color="black")
ax2.tick_params(axis='y', labelcolor="black")

# Thiết lập tiêu đề và hiển thị
plt.title("Biểu đồ Thời gian và Số Màu trung bình của các thuật toán tô màu")
fig.tight_layout()

# Thêm legend
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

plt.grid(True)
plt.show()
