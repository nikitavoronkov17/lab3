
"""
Лабораторная работа № 2. Вариант 5.
n = 1000, 2000, 3000, 4000, 5000, 6000; тип S (упорядоченные);
диапазон [0; 100 000]; повторов k = 3. Доп. задание М5.
Сравнение сортировки пузырьком (с флагом), сортировки вставками
и шейкерной сортировки (двунаправленный пузырёк).
"""
from sorts_common import generate_data, measure


def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def shaker_sort(arr):
    """М5: шейкерная сортировка (двунаправленный пузырёк)."""
    a = arr.copy()
    left, right = 0, len(a) - 1
    while left < right:
        swapped = False
        for j in range(left, right):           # прямой проход
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        right -= 1
        for j in range(right, left, -1):       # обратный проход
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                swapped = True
        left += 1
        if not swapped:
            break
    return a


# --- версии со счётчиком сравнений и обменов (для М5) ---

def bubble_sort_counted(arr):
    a = arr.copy()
    comparisons = swaps = 0
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return a, comparisons, swaps


def shaker_sort_counted(arr):
    a = arr.copy()
    comparisons = swaps = 0
    left, right = 0, len(a) - 1
    while left < right:
        swapped = False
        for j in range(left, right):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        right -= 1
        for j in range(right, left, -1):
            comparisons += 1
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                swaps += 1
                swapped = True
        left += 1
        if not swapped:
            break
    return a, comparisons, swaps


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    SIZES = [1000, 2000, 3000, 4000, 5000, 6000]
    REPEATS = 3
    algorithms = {
        "Пузырьком": bubble_sort,
        "Вставками": insertion_sort,
        "Шейкерная (М5)": shaker_sort,
    }
    results = {name: [] for name in algorithms}

    print(f"{'n':>6}" + "".join(f"{name:>22}" for name in algorithms))
    for n in SIZES:
        data = generate_data(n, kind="sorted", lo=0, hi=100_000)
        row = f"{n:>6}"
        for name, func in algorithms.items():
            t = measure(func, data, REPEATS)
            results[name].append(t)
            row += f"{t:>22.6f}"
        print(row)

    for name, times in results.items():
        plt.plot(SIZES, times, marker="o", label=name)
    plt.xlabel("Размер массива n")
    plt.ylabel("Время, с")
    plt.title("Зависимость времени сортировки от n (вариант 5, тип S)")
    plt.grid(True)
    plt.legend()
    plt.savefig("lr2_plot.png", dpi=150)
    plt.show()
```