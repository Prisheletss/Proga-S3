from pathlib import Path

target_dir = Path(r"C:\Users\Agent\PycharmProjects\LabaProga1\.venv\rvb_texts")

keywords = ["toc"] # - вводим элемент, который должен быть в названии файла, который следует удалить

files_to_delete = [
    file for file in target_dir.glob("*.txt")
    if any(combo.lower() in file.stem.lower() for combo in keywords)
]

if not files_to_delete:
    print("Подходящие текстовые файлы не найдены.")
else:
    print(f"Найдено файлов: {len(files_to_delete)}")
    for file in files_to_delete:
        print(f" - {file.name}")

    confirm = input("\nВы уверены, что хотите БЕЗВОЗВРАТНО удалить эти файлы? (y/n): ")
    if confirm.lower() == "y":
        deleted_count = 0
        for file in files_to_delete:
            try:
                file.unlink()
                print(f"Удалён: {file.name}")
                deleted_count += 1
            except OSError as e:
                print(f"Ошибка при удалении {file.name}: {e}")
        print(f"\nГотово! Успешно удалено файлов: {deleted_count}")
    else:
        print("Удаление отменено.")
