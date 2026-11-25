import matplotlib.pyplot as plt

COLUMN_INDEX = None  # задаётся через input()
CHUNK = 1000

col = int(input("Номер столбца (1-based): ")) - 1
if col < 0:
    raise ValueError("номер столбца должен быть >= 1")

values = []
skipped = 0
with open("cost.txt", "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if col >= len(parts):
            skipped += 1
            continue
        try:
            values.append(float(parts[col]))
        except ValueError:
            skipped += 1

print(f"прочитано чисел: {len(values)}, пропущено строк: {skipped}")

mins, means, maxs = [], [], []
for i in range(0, len(values), CHUNK):
    chunk = values[i:i + CHUNK]
    mins.append(min(chunk))
    means.append(sum(chunk) / len(chunk))
    maxs.append(max(chunk))

x = list(range(1, len(mins) + 1))
plt.figure(figsize=(12, 6))
plt.scatter(x, mins, color="green", s=10, label="мин")
plt.scatter(x, means, color="blue", s=10, label="среднее")
plt.scatter(x, maxs, color="red", s=10, label="макс")
plt.xlabel("номер порции (по 1000 чисел)")
plt.ylabel("значение")
plt.title(f"столбец {col + 1}: мин/среднее/макс по порциям")
plt.legend()
plt.tight_layout()
plt.show()
