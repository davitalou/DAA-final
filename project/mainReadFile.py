import networkx as nx
import Algorithm
import time
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import random

def read_col_file(filepath):
    print(f"Đang đọc tệp: {filepath}")
    G = nx.Graph()
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('e'):
                parts = line.strip().split()
                u = int(parts[1])
                v = int(parts[2])
                G.add_edge(u, v)
    return G

def select_file_via_gui():
    """Hiển thị hộp thoại chọn tệp và trả về đường dẫn tệp đã chọn."""
    Tk().withdraw()  # Ẩn cửa sổ chính của Tkinter
    file_path = askopenfilename(title="Chọn tệp đầu vào", 
                                filetypes=[("Text Files", "*.col"), ("All Files", "*.*")])
    return file_path

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


G = read_col_file(select_file_via_gui())
# G = generate_random_graph(700, 90000)
# print(f"Số đỉnh: {G.number_of_nodes()}")
# print(f"Số cạnh: {G.number_of_edges()}")

# Welsh-Powell
start = time.time()*1000
wp_result = Algorithm.color_welsh_powell(G)
end1 = time.time()*1000
print(f"Welsh-Powell - Số màu sử dụng: {len(set(wp_result.values()))}, thời gian: {end1 - start}ms")
# DSATUR
dsatur_result = Algorithm.color_dsatur(G)
end2 = time.time()*1000
print(f"DSATUR - Số màu sử dụng: {len(set(dsatur_result.values()))}, thời gian: {end2 - end1}ms")
