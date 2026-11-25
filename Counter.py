import re
import csv
from pathlib import Path
from collections import Counter, defaultdict

FOLDER_PATH = Path(r"C:\Users\Agent\PycharmProjects\LabaProga1\.venv\rvb_texts")
OUTPUT_CSV = Path("word_transitions.csv")

# Так как у текста остались некоторые технические детали, нужно его подчистить посредством ниже описанного кода
def clean_and_tokenize(text: str):
    text = re.sub(r'([а-яА-ЯёЁ]+)\n+([аеёиоуыэюяАЕЁИОУЫЭЮЯ])\n+([а-яА-ЯёЁ]+)', r'\1\2\3', text)
  
    text = re.sub(r'\n(?:Воспроизводится по изданию:|[^\n]+//[^\n]+|[^\n]+(?:Советский писатель|Гос\. изд-во|ГИХЛ|Библиотека поэта).*)$', '', text, flags=re.DOTALL)

    text = re.sub(r'^.*?Поиск по РВБ\s+Найти\s+Авторы\s+', '', text, flags=re.DOTALL)

    text = re.sub(r'\n+\s*\d{1,4}\s*\n+(?=[а-яё])', ' ', text)

    text = re.sub(r'(?m)^\s*(?:\d{1,4}|[IVXLCDM]+)\s*$', '', text)
  
    text = re.sub(r'(?m)^\s*\d{1,3}\s+(?=[А-ЯЁа-яё])', '', text)

    text = re.sub(r'(?m)^\s*(?:\d{1,2}\s+[а-я]+\s+)?\d{4}(?:-е)?\s*(?:год[а-я]*|г\.?)?\s*$', '', text, flags=re.IGNORECASE)
  
    lines = text.splitlines()
    cleaned_lines = []
    header_zone = True  

    for line in lines:
        s = line.strip()
        if not s:
            continue

        if header_zone:
            if (
                re.match(r'^(?:[А-ЯЁ]\.\s*){1,2}[А-ЯЁ][а-яё]+', s) or  # И. А. Крылов, А. С. Пушкин
                re.match(r'^(?:Т\.|Том|Книга|Часть|Собр\.|Полн\.|Стихотворения|Переводы|Басни|Раннее|История Петра)', s) or
                re.match(r'^\d+\.\s+[А-ЯЁ]', s) or  # "301. На родине"
                'перевод с ' in s.lower() or
                s.isupper()  
            ):
                continue
            else:
                header_zone = False

        # Пропускаем заголовки 
        if s.isupper() and len(s) > 1:
            continue
        if s in ("Священник", "Стихотворец"):
            continue

        cleaned_lines.append(s)

    # Начинаем сам подсчёт
    tokens = []
    for seg in cleaned_lines:
        # Оставляем только слова (игнорируя знаки препинания, числа, латинские пометки)
        words = re.findall(r'[а-яА-ЯёЁ]+(?:-[а-яА-ЯёЁ]+)*', seg.lower())
        if words:
            tokens.extend(words)
            tokens.append("<КОНЕЦ_АБЗАЦА/СТРОКИ>")

    return tokens

transitions = defaultdict(Counter)
word_totals = Counter()
files_processed = 0

print("Начинаю анализ файлов...")

for file_path in FOLDER_PATH.glob("*.txt"):
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"Ошибка чтения {file_path.name}: {e}")
        continue

    tokens = clean_and_tokenize(content)
    files_processed += 1

    for i in range(len(tokens) - 1):
        current_word = tokens[i]
        next_word = tokens[i + 1]

        if current_word == "<КОНЕЦ_АБЗАЦА/СТРОКИ>":
            continue

        word_totals[current_word] += 1
        transitions[current_word][next_word] += 1

print(f"Обработано файлов: {files_processed}")
print(f"Найдено уникальных слов: {len(word_totals)}")

with open(OUTPUT_CSV, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['Слово', 'Всего_встретилось', 'Следующее_слово', 'Сколько_раз_после', 'Вероятность_%'])

    for word, total_count in word_totals.most_common():
        for next_w, count in transitions[word].most_common():
            prob = round((count / total_count) * 100, 2)
            writer.writerow([word, total_count, next_w, count, prob])

print(f"Готово! Таблица сохранена в {OUTPUT_CSV.resolve()}")
