import numpy as np
import sympy as sp

# ========================================
# ВВОД ГРАФА: МАТРИЦА СМЕЖНОСТИ
# ========================================
# Порядок вершин: A, B, C, D
vertices = ['A', 'B', 'C', 'D']

A = np.array([
    [0, 1, 0, 1],   # A: связан с B, D
    [1, 0, 1, 1],   # B: связан с A, C, D
    [0, 1, 0, 1],   # C: связан с B, D
    [1, 1, 1, 0]    # D: связан с A, B, C
])

print("=" * 50)
print("МАТРИЦА СМЕЖНОСТИ")
print("=" * 50)
print("   ", "  ".join(vertices))
for i, row in enumerate(A):
    print(vertices[i], row)


# ========================================
# ПУНКТ 1: МАТРИЦА ИНЦИДЕНТНОСТИ
# ========================================
print("\n" + "=" * 50)
print("ПУНКТ 1: МАТРИЦА ИНЦИДЕНТНОСТИ")
print("=" * 50)

# Определяем рёбра графа (обозначение e1, e2, ...)
edges = []
n = len(vertices)
for i in range(n):
    for j in range(i + 1, n):
        if A[i][j] == 1:
            edges.append((i, j))

edge_labels = [f"e{k+1}({vertices[i]}{vertices[j]})"
               for k, (i, j) in enumerate(edges)]

print("Рёбра графа:", edge_labels)

# Строим матрицу инцидентности
incidence_matrix = np.zeros((n, len(edges)), dtype=int)
for k, (i, j) in enumerate(edges):
    incidence_matrix[i][k] = 1
    incidence_matrix[j][k] = 1

print("\nМатрица инцидентности I (строки - вершины, столбцы - рёбра):")
print("     ", "  ".join([f"e{k+1}" for k in range(len(edges))]))
for i, row in enumerate(incidence_matrix):
    print(vertices[i], " ", row)


# ========================================
# ПУНКТ 2: МАТРИЦА КИРХГОФА (ЛАПЛАСА)
# ========================================
print("\n" + "=" * 50)
print("ПУНКТ 2: МАТРИЦА КИРХГОФА (ЛАПЛАСА)")
print("=" * 50)

# Матрица степеней D (диагональная)
degrees = A.sum(axis=1)
D = np.diag(degrees)

print("Степени вершин:")
for i, v in enumerate(vertices):
    print(f"  deg({v}) = {degrees[i]}")

print("\nМатрица степеней D:")
print(D)

# Матрица Кирхгофа (Лапласиан) L = D - A
L = D - A

print("\nМатрица Кирхгофа (Лапласа) L = D - A:")
print(L)

# Проверка: сумма элементов в каждой строке = 0
print("\nПроверка (сумма по строкам должна быть 0):")
print(L.sum(axis=1))


# ========================================
# ПУНКТ 3: СПЕКТР ГРАФА
# ========================================
print("\n" + "=" * 50)
print("ПУНКТ 3: СПЕКТР ГРАФА")
print("=" * 50)

# --- Символьный вывод характеристического уравнения ---
lam = sp.symbols('lambda')
A_sym = sp.Matrix(A.tolist())
I_sym = sp.eye(n)

char_matrix = A_sym - lam * I_sym
print("\nМатрица (A - λI):")
sp.pprint(char_matrix)

char_poly = char_matrix.det()
char_poly_expanded = sp.expand(char_poly)
print("\nХарактеристическое уравнение det(A - λI) = 0:")
print(f"{char_poly_expanded} = 0")

# Приводим к стандартному виду (переставляем знак, если нужно)
char_poly_final = sp.simplify(char_poly_expanded)
print(f"\nУпрощённое уравнение: {sp.factor(char_poly_final)} = 0")

# --- Находим корни уравнения (собственные значения) ---
eigenvalues_symbolic = sp.solve(sp.Eq(char_poly_expanded, 0), lam)

print("\nСобственные значения (точные, символьные):")
for i, val in enumerate(eigenvalues_symbolic, 1):
    print(f"  λ{i} = {val} ≈ {complex(val).real:.4f}" if val.is_real
          else f"  λ{i} = {val}")

# --- Численный расчёт через numpy (для сравнения) ---
eigenvalues_numeric = np.linalg.eigvals(A)
eigenvalues_numeric_sorted = sorted(eigenvalues_numeric, reverse=True)

print("\nСобственные значения (численно, через numpy):")
for i, val in enumerate(eigenvalues_numeric_sorted, 1):
    print(f"  λ{i} = {val:.4f}")

# --- Спектр графа (итоговый набор) ---
print("\n" + "-" * 50)
print("СПЕКТР ГРАФА:")
print("-" * 50)
spectrum_str = ", ".join([f"{v:.4f}" for v in eigenvalues_numeric_sorted])
print(f"Spec(G) = {{{spectrum_str}}}")

# --- Проверки корректности ---
print("\n" + "-" * 50)
print("ПРОВЕРКИ:")
print("-" * 50)

trace_A = np.trace(A)
sum_eigenvalues = sum(eigenvalues_numeric).real
print(f"След матрицы A = {trace_A}")
print(f"Сумма собственных значений = {sum_eigenvalues:.4f}")
print(f"Проверка 1 (должны совпадать): {'✓ OK' if abs(trace_A - sum_eigenvalues) < 1e-6 else '✗ ОШИБКА'}")

num_edges = len(edges)
sum_squares = sum([abs(v)**2 for v in eigenvalues_numeric]).real
print(f"\n2 × число рёбер = {2 * num_edges}")
print(f"Сумма квадратов собственных значений = {sum_squares:.4f}")
print(f"Проверка 2 (должны совпадать): {'✓ OK' if abs(2*num_edges - sum_squares) < 1e-6 else '✗ ОШИБКА'}")