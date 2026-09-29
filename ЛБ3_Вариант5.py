"""
Лабораторная работа № 3. Вариант 5.
Быстрая сортировка (опорный — медиана трёх, разбиение Хоара) и
нисходящая сортировка слиянием. Доп. задание Г5 — устойчивость.
"""
import math
from sorts_common import generate_data, measure
from lr2 import bubble_sort, insertion_sort


# ---------- Медиана трёх (для М3) ----------
def median3(x, y, z):
    """Возвращает медиану трёх значений."""
    if x <= y:
        if y <= z:
            return y
        return z if x <= z else x
    else:
        if x <= z:
            return x
        return z if y <= z else y


# ---------- Быстрая сортировка (М3 + Хоар) ----------
def quick_sort(arr, key=lambda v: v):
    """Быстрая сортировка с медианой трёх и разбиением Хоара."""
    a = arr.copy()
    _quick_sort(a, 0, len(a) - 1, key)
    return a


def _quick_sort(a, lo, hi, key):
    while lo < hi:
        p = _partition(a, lo, hi, key)
        # рекурсия в меньшую часть — глубина стека O(log n)
        if p - lo < hi - p:
            _quick_sort(a, lo, p, key)
            lo = p + 1
        else:
            _quick_sort(a, p + 1, hi, key)
            hi = p


def _partition(a, lo, hi, key):
    """Разбиение Хоара, опорный элемент — медиана трёх."""
    mid = (lo + hi) // 2
    pivot = median3(key(a[lo]), key(a[mid]), key(a[hi]))
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while key(a[i]) < pivot:
            i += 1
        j -= 1
        while key(a[j]) > pivot:
            j -= 1
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]


# ---------- Сортировка слиянием (нисходящая) ----------
def merge_sort(arr, key=lambda v: v):
    """Нисходящая сортировка слиянием (устойчивая)."""
    if len(arr) <= 1:
        return arr.copy()
    mid = len(arr) // 2
    return _merge(merge_sort(arr[:mid], key), merge_sort(arr[mid:], key), key)


def _merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):     # <= обеспечивает устойчивость
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------- Версии со счётчиком сравнений ----------
def quick_sort_counted(arr):
    """Быстрая сортировка со счётчиком сравнений. Возвращает (список, число)."""
    a = arr.copy()
    cnt = [0]

    def part(lo, hi):
        mid = (lo + hi) // 2
        pivot = median3(a[lo], a[mid], a[hi])
        i, j = lo - 1, hi + 1
        while True:
            i += 1
            while a[i] < pivot:
                cnt[0] += 1
                i += 1
            cnt[0] += 1
            j -= 1
            while a[j] > pivot:
                cnt[0] += 1
                j -= 1
            cnt[0] += 1
            if i >= j:
                return j
            a[i], a[j] = a[j], a[i]

    def qs(lo, hi):
        while lo < hi:
            p = part(lo, hi)
            if p - lo < hi - p:
                qs(lo, p)
                lo = p + 1
            else:
                qs(p + 1, hi)
                hi = p

    qs(0, len(a) - 1)
    return a, cnt[0]


def merge_sort_counted(arr):
    """Сортировка слиянием со счётчиком сравнений. Возвращает (список, число)."""
    cnt = [0]

    def ms(x):
        if len(x) <= 1:
            return x.copy()
        mid = len(x) // 2
        left, right = ms(x[:mid]), ms(x[mid:])
        res = []
        i = j = 0
        while i < len(left) and j < len(right):
            cnt[0] += 1
            if left[i] <= right[j]:
                res.append(left[i]); i += 1
            else:
                res.append(right[j]); j += 1
        res.extend(left[i:]); res.extend(right[j:])
        return res

    return ms(arr), cnt[0]


# ---------- Вспомогательная функция для экспериментов ----------
def run_experiment(algorithms, sizes, kind="random", repeats=3, lo=0, hi=100_000):
    """Печатает таблицу время/размер и возвращает словарь результатов."""
    results = {name: [] for name in algorithms}
    print(f"{'n':>8}" + "".join(f"{name:>14}" for name in algorithms))
    for n in sizes:
        data = generate_data(n, kind=kind, lo=lo, hi=hi)
        row = f"{n:>8}"
        for name, func in algorithms.items():
            t = measure(func, data, repeats)
            results[name].append(t)
            row += f"{t:>14.6f}"
        print(row)
    return results


# ---------- Запуск ----------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # --- Эксперимент 1: 4 алгоритма на размерах из ЛР № 2 ---
    small = [1000, 2000, 3000, 4000, 5000, 6000]
    algs1 = {"Пузырьком": bubble_sort, "Вставками": insertion_sort,
             "Быстрая": quick_sort, "Слиянием": merge_sort}

    print("=== Эксперимент 1а: упорядоченные (S) ===")
    res1a = run_experiment(algs1, small, "sorted", 3, 0, 100_000)

    print("\n=== Эксперимент 1б: случайные (R) ===")
    res1b = run_experiment(algs1, small, "random", 3, 0, 100_000)

    # --- Эксперимент 2: большие размеры варианта 5 ---
    large = [30_000, 60_000, 90_000, 120_000]
    print("\n=== Эксперимент 2 ===")
    res2 = run_experiment({"Быстрая": quick_sort, "Слиянием": merge_sort,
                           "sorted()": sorted}, large, "random", 3, 0, 100_000)

    # --- Эксперимент 3: структура данных, n = 50 000 ---
    print("\n=== Эксперимент 3, n = 50 000 ===")
    for label, kind, lo, hi in [("R", "random", 0, 100_000),
                                ("S", "sorted", 0, 100_000),
                                ("V", "reversed", 0, 100_000),
                                ("N", "nearly_sorted", 0, 100_000),
                                ("D", "random", 0, 10)]:
        data = generate_data(50_000, kind=kind, lo=lo, hi=hi)
        print(f"{label:>3}: быстрая {measure(quick_sort, data, 3):.4f} с, "
              f"слиянием {measure(merge_sort, data, 3):.4f} с")

    # --- Число сравнений ---
    print("\n=== Число сравнений (случайные данные) ===")
    print(f"{'n':>8}{'быстрая':>12}{'слиянием':>12}{'n*log2(n)':>12}"
          f"{'q/nlogn':>10}{'m/nlogn':>10}")
    for n in large:
        data = generate_data(n, "random", 0, 100_000)
        _, cq = quick_sort_counted(data)
        _, cm = merge_sort_counted(data)
        nl = n * math.log2(n)
        print(f"{n:>8}{cq:>12}{cm:>12}{nl:>12.0f}{cq / nl:>10.2f}{cm / nl:>10.2f}")

    # --- Г5: устойчивость ---
    print("\n=== Г5: устойчивость на записях (регион, выручка) ===")
    records = [("Москва", 100), ("СПб", 50), ("Москва", 50),
               ("Казань", 100), ("СПб", 100), ("Казань", 50)]
    print("Исходные:               ", records)
    print("Слиянием (устойчивая):  ", merge_sort(records, key=lambda r: r[1]))
    print("Быстрая (неустойчивая): ", quick_sort(records, key=lambda r: r[1]))

    # --- Графики ---
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for name, t in res1b.items():
        axes[0].plot(small, t, marker="o", label=name)
    axes[0].set_yscale("log")
    axes[0].set_title("Эксперимент 1б, лог. шкала (случайные)")

    for name, t in res2.items():
        axes[1].plot(large, t, marker="o", label=name)
    axes[1].set_title("Эксперимент 2")

    for ax in axes:
        ax.set_xlabel("Размер массива n")
        ax.set_ylabel("Время, с")
        ax.grid(True)
        ax.legend()
    plt.tight_layout()
    plt.savefig("lr3_plot.png", dpi=150)
    plt.show()