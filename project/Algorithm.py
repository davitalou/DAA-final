import networkx as nx
import itertools
# --- 1. BackTracking ---
def color_backtracking(G):
    color = {}
    nodes = list(G.nodes())

    def is_valid(node, c):
        for neighbor in G.neighbors(node):
            if neighbor in color and color[neighbor] == c:
                return False
        return True

    def backtrack(index, max_colors):
        if index == len(nodes):
            return True
        node = nodes[index]
        for c in range(1, max_colors + 1):
            if is_valid(node, c):
                color[node] = c
                if backtrack(index + 1, max_colors):
                    return True
                del color[node]
        return False

    n = len(nodes)
    for max_colors in range(1, n + 1):  # Thử từ 1 màu, tăng dần
        color.clear()
        if backtrack(0, max_colors):
            return color, max_colors

    return None, n  # Không tìm thấy (hầu như không xảy ra)


# --- 2. BruteForce ---
def is_valid_coloring(graph, coloring):
    """Kiểm tra coloring có hợp lệ không."""
    for u in graph.nodes():
        for v in graph.neighbors(u):
            if coloring[u] == coloring[v]:
                return False
    return True

def brute_force_coloring(graph):
    """Brute-force tô màu đồ thị."""
    nodes = list(graph.nodes())
    n = len(nodes)
    for num_colors in range(1, n + 1):
        for coloring_tuple in itertools.product(range(num_colors), repeat=n):
            coloring = {nodes[i]: coloring_tuple[i] for i in range(n)}
            if is_valid_coloring(graph, coloring):
                return coloring, num_colors
    return None, n



# --- 3. Welsh-Powell ---
def color_welsh_powell(G):
    nodes = sorted(G.nodes(), key=lambda x: G.degree[x], reverse=True)
    color = {}
    current_color = 1
    while len(color) < len(G.nodes()):
        for node in nodes:
            if node not in color:
                if all(color.get(nei) != current_color for nei in G.neighbors(node)):
                    color[node] = current_color
        current_color += 1
    return color


# --- 4. DSATUR ---
def color_dsatur(G):
    color = {}
    saturation = {node: 0 for node in G.nodes()}
    degrees = dict(G.degree())

    def sat_degree(n):
        return (saturation[n], degrees[n])

    while len(color) < len(G.nodes()):
        node = max((n for n in G.nodes() if n not in color), key=sat_degree)
        used_colors = {color[nei] for nei in G.neighbors(node) if nei in color}
        for c in range(1, len(G) + 1):
            if c not in used_colors:
                color[node] = c
                break
        for neighbor in G.neighbors(node):
            if neighbor not in color:
                saturation[neighbor] = len({color[n] for n in G.neighbors(neighbor) if n in color})
    return color