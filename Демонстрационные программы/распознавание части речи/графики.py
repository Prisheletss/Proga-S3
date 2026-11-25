import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def plot_column_from_tsv(file_path, col_index):
    """
    Читает TSV файл построчно, извлекает один столбец и строит точечный график.
    """
    if not os.path.exists(file_path):
        print(f"Ошибка: файл {file_path} не найден.")
        return

    print(f"Чтение столбца {col_index} из файла {file_path}...")
    
    # Используем pandas для построчного чтения. 
    # usecols позволяет не парсить остальные 188 столбцов, экономя память.
    # names=[0] задаем имя столбцу, чтобы к нему можно было обратиться.
    try:
        data_iter = pd.read_csv(
            file_path, 
            sep='\t', 
            header=None, 
            usecols=[col_index], 
            names=['value'],
            dtype={'value': 'float64'}, # сразу приводим к числу
            chunksize=100000 # читаем пачками по 100к строк
        )
        
        # Собираем данные из чанков в один список
        values = []
        for chunk in data_iter:
            # Пропускаем пустые строки или нечисловые значения
            values.extend(chunk['value'].dropna().tolist())
            
    except IndexError:
        print(f"Ошибка: в файле нет столбца с индексом {col_index}.")
        print(f"Напоминание: индексация в коде начинается с 0. Столбец 74 в вашем примере — это индекс 73.")
        return
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return

    if not values:
        print("В выбранном столбце не найдено валидных числовых данных.")
        return

    print(f"Прочитано {len(values)} строк. Построение графика...")

    # Подготовка координат X (индексы строк) и Y (значения из файла)
    x_coords = list(range(len(values)))
    y_coords = values

    # Настройка и построение графика
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # s=10 — размер точек, можно уменьшить до 1-2 для очень больших массивов
    ax.scatter(x_coords, y_coords, s=10, alpha=0.7, c='royalblue', edgecolors='none')
    
    ax.set_title(f'Точечная диаграмма столбца {col_index}', fontsize=16)
    ax.set_xlabel('Номер строки (индекс)', fontsize=12)
    ax.set_ylabel('Значение', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Автоматическое ограничение осей по данным, чтобы не было пустых полей
    ax.set_xlim(min(x_coords), max(x_coords))
    ax.set_ylim(min(y_coords), max(y_coords))

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Имя файла можно передать аргументом или прописать жестко
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = 'cost.txt'#'evolution.txt'
        
    # Запрос номера столбца у пользователя
    try:
        # Напоминаем пользователю, что индексация с 0
        col_input = input(f"Введите номер столбца (начиная с нуля): ")
        column_index = int(col_input)
        
        if column_index < 0:
            print("Номер столбца не может быть отрицательным.")
            sys.exit(1)
            
    except ValueError:
        print("Ошибка: введено не число.")
        sys.exit(1)

    plot_column_from_tsv(file_name, column_index)
