import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import os
from collections import deque
import urllib.request

font_path = "./NanumGothic.ttf"

if not os.path.exists(font_path):
    url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    urllib.request.urlretrieve(url, font_path)

fontprop = fm.FontProperties(fname=font_path, size=12)
mpl.rc('font', family=fontprop.get_name())  # 한글 폰트 전역 설정

nodes = ["A", "B", "C", "D", "E", "F"]
graph_matrix = [
    [0, 1, 1, 0, 0, 0],
    [1, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 1, 0]
]

def draw_graph(highlight_nodes=None, highlight_edges=None, title="현재 그래프 상태"):
    G = nx.Graph()
    G.add_nodes_from(nodes)

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if graph_matrix[i][j] == 1:
                G.add_edge(nodes[i], nodes[j])

    pos = st.session_state.graph_pos  
    plt.figure(figsize=(6, 4))

    nx.draw(G, pos, with_labels=True, node_color="lightgray", edge_color="gray",
            node_size=1000, font_size=12, font_family=fontprop.get_name())

    if highlight_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=highlight_nodes, node_color="red", node_size=1000)
    if highlight_edges:
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color="blue", width=2)

    plt.title(title, fontproperties=fontprop)
    st.pyplot(plt)
    plt.close()

def bfs_step():
    if st.session_state.bfs_queue and not st.session_state.bfs_complete:
        node = st.session_state.bfs_queue.popleft()
        st.session_state.current_node = node  

        if node not in st.session_state.visited:
            st.session_state.visited.append(node)

            node_index = nodes.index(node)
            for i, connected in enumerate(graph_matrix[node_index]):
                if connected == 1 and nodes[i] not in st.session_state.visited:
                    st.session_state.edges_traversed.append((node, nodes[i]))
                    st.session_state.bfs_queue.append(nodes[i])

    if not st.session_state.bfs_queue:
        st.session_state.bfs_complete = True

if not st.session_state.bfs_complete:
    if st.button("Next (다음 단계)"):
        bfs_step()  
        st.rerun()  
