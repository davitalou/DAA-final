import networkx as nx

def color_backtracking(G, max_colors):
    color = {}
    nodes = list(G.nodes())

    def is_valid(node, c):
        for neighbor in G.neighbors(node):
            if neighbor in color and color[neighbor] == c:
                return False
        return True

    def backtrack(index):
        if index == len(nodes):
            return True
        node = nodes[index]
        for c in range(1, max_colors + 1):
            if is_valid(node, c):
                color[node] = c
                if backtrack(index + 1):
                    return True
                del color[node]
        return False

    if backtrack(0):
        return color
    else:
        return None


# --- 3. Greedy coloring (mặc định theo thứ tự node) ---
def color_greedy(graph):
    color = {}
    
    for node in graph:
        # Lấy màu của các đỉnh kề
        neighbor_colors = {color[neighbor] for neighbor in graph[node] if neighbor in color}
        
        # Tìm màu nhỏ nhất chưa được dùng
        for c in range(1, len(graph) + 1):
            if c not in neighbor_colors:
                color[node] = c
                break
                
    return color


# --- 4. Welsh-Powell ---
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


# --- 5. DSATUR ---
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