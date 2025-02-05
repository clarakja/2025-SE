import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import os
from collections import deque
import urllib.request

# 🔹 나눔고딕 폰트 다운로드 및 적용
font_path = "./NanumGothic.ttf"

if not os.path.exists(font_path):
    url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    urllib.request.urlretrieve(url, font_path)

# 🔹 기본 폰트 설정 (한글 깨짐 방지)
fontprop = fm.FontProperties(fname=font_path, size=12)
mpl.rc('font', family=fontprop.get_name())  # 한글 폰트 전역 설정

# 🔹 Streamlit 앱 제목
st.title("🔍 BFS 탐색 시각화 (인접 행렬)")

# 🔹 인접 행렬 방식으로 그래프 저장
nodes = ["A", "B", "C", "D", "E", "F"]
graph_matrix = [
    [0, 1, 1, 0, 0, 0],  # A (A-B, A-C)
    [1, 0, 0, 1, 1, 0],  # B (B-A, B-D, B-E)
    [1, 0, 0, 0, 0, 1],  # C (C-A, C-F)
    [0, 1, 0, 0, 0, 0],  # D (D-B)
    [0, 1, 0, 0, 0, 1],  # E (E-B, E-F)
    [0, 0, 1, 0, 1, 0]   # F (F-C, F-E)
]

# 🔹 초기 그래프 시각화 함수 (한글 폰트 적용)
def draw_graph(highlight_nodes=None, highlight_edges=None, title="현재 그래프 상태"):
    G = nx.Graph()
    
    # 노드 추가
    G.add_nodes_from(nodes)
    
    # 간선 추가 (인접 행렬 기반)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):  # 중복 방지
            if graph_matrix[i][j] == 1:
                G.add_edge(nodes[i], nodes[j])

    pos = st.session_state.graph_pos  # 🔹 저장된 레이아웃 사용 (고정됨)
    plt.figure(figsize=(6, 4))

    # 🔹 기본 그래프 노드 및 간선
    nx.draw(G, pos, with_labels=True, node_color="lightgray", edge_color="gray",
            node_size=1000, font_size=12, font_family=fontprop.get_name())

    # 🔹 탐색된 노드 강조 (빨간색)
    if highlight_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=highlight_nodes, node_color="red", node_size=1000)

    # 🔹 탐색된 간선 강조 (파란색)
    if highlight_edges:
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color="blue", width=2)

    plt.title(title, fontproperties=fontprop)
    st.pyplot(plt)
    plt.close()

# 🔹 Streamlit에서 시작 노드 선택 UI 제공
start_node = st.selectbox("시작 노드를 선택하세요:", nodes)

# 🔹 초기 레이아웃을 한 번만 생성하여 session_state에 저장
if "graph_pos" not in st.session_state:
    G = nx.Graph()
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):  
            if graph_matrix[i][j] == 1:
                G.add_edge(nodes[i], nodes[j])
    st.session_state.graph_pos = nx.spring_layout(G)  # 🔹 처음 만든 레이아웃 저장
    
# 🔹 BFS 상태를 유지하기 위한 session_state 초기화
if "bfs_queue" not in st.session_state or "visited" not in st.session_state:
    st.session_state.bfs_queue = deque([start_node])  # BFS 큐
    st.session_state.visited = []  # 방문한 노드 저장
    st.session_state.edges_traversed = []  # 방문한 간선 저장
    st.session_state.bfs_complete = False  # 탐색 완료 여부
    st.session_state.current_node = None  # 현재 탐색 중인 노드

# 🔹 BFS 탐색 단계별 진행
def bfs_step():
    if st.session_state.bfs_queue and not st.session_state.bfs_complete:
        node = st.session_state.bfs_queue.popleft()
        st.session_state.current_node = node  # 현재 방문 중인 노드 저장

        if node not in st.session_state.visited:
            st.session_state.visited.append(node)

            node_index = nodes.index(node)
            for i, connected in enumerate(graph_matrix[node_index]):
                if connected == 1 and nodes[i] not in st.session_state.visited:
                    st.session_state.edges_traversed.append((node, nodes[i]))
                    st.session_state.bfs_queue.append(nodes[i])

    # 🔹 BFS가 완료되었는지 체크
    if not st.session_state.bfs_queue:
        st.session_state.bfs_complete = True

# 🔹 BFS 진행 버튼 (단계별 실행)
if not st.session_state.bfs_complete:
    if st.button("Next (다음 단계)"):
        bfs_step()  # 🔹 버튼이 눌릴 때만 BFS의 한 단계 실행
        st.rerun()  # 🔹 UI 업데이트 강제 실행

# 🔹 최종 메시지 출력
if st.session_state.bfs_complete:
    st.success(f"🎉 BFS 탐색 완료! 탐색 순서: {' → '.join(st.session_state.visited)}")


# 🔹 현재 탐색 상태 그래프 시각화
draw_graph(highlight_nodes=st.session_state.visited, highlight_edges=st.session_state.edges_traversed,
           title=f"BFS 탐색 진행: {' → '.join(st.session_state.visited)}")
