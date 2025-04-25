import time
import matplotlib.pyplot as plt
import networkx as nx
import random
import Algorithm

# Danh sách mở rộng đã đề cập
sizes = [
    (100, 600), (200, 1200), (300, 1800), (400, 2800), (500, 3500),
    (600, 5000), (700, 6200), (800, 7500), (900, 9000), (1000, 10500),
    (1200, 13000), (1500, 17000), (1800, 21000), (2000, 25000),
    (2300, 29000), (2600, 34000), (3000, 42000), (3500, 51000),
    (4000, 62000), (4500, 73000), (5000, 85000), (5500, 97000),
]

#     (6000, 110000), (6500, 123000), (7000, 137000)

num_trials = 20

# Tạo các dict để lưu thời gian và số màu trung bình
algorithms = ["Greedy", "Welsh-Powell", "DSATUR"]
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

        # --- Greedy ---
        start = time.time()
        result = Algorithm.color_greedy(G)
        elapsed = (time.time() - start) * 1000
        trial_times["Greedy"].append(elapsed)
        trial_colors["Greedy"].append(len(set(result.values())))

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
    ax1.plot(x_labels, time_results[algo], marker='o', label=f"{algo} (Thời gian)", linestyle='-', color=f"C{algorithms.index(algo)}")
ax1.set_xlabel("Số đỉnh")
ax1.set_ylabel("Thời gian trung bình (ms)", color="black")
ax1.tick_params(axis='y', labelcolor="black")

# Tạo trục phụ (y2) cho số màu
ax2 = ax1.twinx()
for algo in algorithms:
    ax2.plot(x_labels, color_counts[algo], marker='s', label=f"{algo} (Số màu)", linestyle='--', color=f"C{algorithms.index(algo)}")
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
