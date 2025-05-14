import Algorithm
import time
import matplotlib.pyplot as plt
import networkx as nx
import random
import matplotlib.ticker as ticker

def generate_random_graph(n, density=0.5):
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < density:
                G.add_edge(i, j)
    return G

num_trials = 20
sizes = list(range(4, 25))  # Backtracking: từ 4 đến 24 đỉnh

backtracking_times = []
brute_force_times = []

for n in sizes:
    total_back_time = 0
    total_brute_time = 0

    for _ in range(num_trials):
        G = generate_random_graph(n, density=0.5)

        # Backtracking
        start = time.time()
        result_back, num_colors_back = Algorithm.color_backtracking(G)
        end = time.time()
        total_back_time += (end - start)

        # Brute-force (chỉ chạy khi n <= 11)
        if n <= 11:
            start = time.time()
            brute_result, num_colors_brute = Algorithm.brute_force_coloring(G)
            end = time.time()
            total_brute_time += (end - start)

    avg_back_time = (total_back_time / num_trials) * 1000  # ms
    backtracking_times.append(avg_back_time)

    if n <= 11:
        avg_brute_time = (total_brute_time / num_trials) * 1000  # ms
        brute_force_times.append(avg_brute_time)
    else:
        brute_force_times.append(None)  # để khi vẽ đồ thị thì bỏ qua

# Vẽ biểu đồ
plt.figure(figsize=(10, 5))
plt.plot(sizes, backtracking_times, label='Backtracking')

# Vẽ brute-force chỉ ở phần có dữ liệu
sizes_brute = sizes[:8]  # từ 4 đến 11 (8 phần tử)
plt.plot(sizes_brute, brute_force_times[:8], label='Brute-force', linestyle='--')

plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.xlabel('Số đỉnh')
plt.ylabel('Thời gian trung bình (ms)')
plt.title('So sánh thời gian Backtracking và Brute-force')
plt.legend()
plt.grid(True)
plt.show()
