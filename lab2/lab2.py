import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import string

def task1():
    G = nx.petersen_graph()


    pos = {
        0: (0.68, 4.20),
        4: (2.07, 4.48),
        6: (1.45, 3.72),
        8: (2.38, 3.82),
        1: (0.48, 2.55),
        5: (1.55, 2.53),
        9: (2.07, 2.62),
        3: (2.67, 2.35),
        2: (1.35, 0.83),
        7: (2.15, 0.83),
    }
    pos1 = nx.spring_layout(G, seed=7)

    subax1 = plt.subplot(121)
    nx.draw(G, pos1, with_labels=True, font_weight='bold')

    subax2 = plt.subplot(122)
    nx.draw_shell(G, nlist=[range(5, 10), range(6)], with_labels=True, font_weight='bold')

def task2():
    p0= [[0, 1, 1, 1, 0, 1],
     [1, 0, 1, 1, 0, 1],
     [1, 1, 0, 1, 0, 1],
     [0, 1, 0, 0, 0, 0],
     [1, 1, 1, 1, 0, 1],
     [1, 1, 1, 1, 1, 1]]

    g = nx.DiGraph(np.matrix(p0))
    nx.draw(g, with_labels=True, node_size=300, arrows=True)
    plt.show()


    plt.show()

def task3():
    def read_adjacency_matrix():
        n = int(input("Введите количество вершин: "))

        if n > 26:
            raise ValueError("Слишком много вершин для автоматических подписей (максимум 26 — A-Z)")

        print(f"Введите матрицу смежности ({n}x{n}), каждая строка — числа через пробел:")
        matrix = []
        for i in range(n):
            row = list(map(int, input(f"Строка {i + 1}: ").split()))
            if len(row) != n:
                raise ValueError(f"Строка должна содержать {n} чисел")
            matrix.append(row)

        labels = list(string.ascii_uppercase[:n])

        return np.array(matrix), labels


    def draw_graph_from_adjacency(adj_matrix, labels, layout='spring', seed=42):
        G = nx.from_numpy_array(adj_matrix)

        mapping = {i: labels[i] for i in range(len(labels))}
        G = nx.relabel_nodes(G, mapping)

        if layout == 'spring':
            pos = nx.spring_layout(G, seed=seed)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'shell':
            pos = nx.shell_layout(G)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        else:
            raise ValueError("Неизвестный layout")

        nx.draw(
            G, pos,
            with_labels=True,
            node_color='violet',
            node_size=999,
            font_weight='bold',
            font_color='white',
            edge_color='gray'
        )

        plt.show()


    adj_matrix, labels = read_adjacency_matrix()
    draw_graph_from_adjacency(adj_matrix, labels, layout='spring', seed=1)


if __name__ == "__main__":
    task3()
