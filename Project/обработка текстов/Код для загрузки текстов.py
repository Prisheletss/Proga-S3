import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import os
import re

# --- Настройки ---
BASE_URL = "http://www.rvb.ru"
START_URLS = [
    "http://www.rvb.ru/pushkin/",
    "http://www.rvb.ru/18vek/",
    "http://www.rvb.ru/19vek/",
]
OUTPUT_DIR = "rvb_texts"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
DELAY = 1.5  # секунды между запросами

# --- Вспомогательные функции ---

def get_html(url):
    """Скачивает HTML страницы с обработкой ошибок."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            # Принудительно ставим кодировку windows-1251, если сервер не указал её
            if resp.encoding is None or resp.encoding.lower() == 'iso-8859-1':
                resp.encoding = 'windows-1251'
            return resp.text
    except requests.RequestException as e:
        print(f"  [Ошибка] {url} -> {e}")
    return None

def extract_text(html):
    """Извлекает чистый текст из HTML-страницы."""
    soup = BeautifulSoup(html, "html.parser")
    # Удаляем скрипты и стили
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # Чистим множественные пустые строки
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def is_text_page(url):
    """Проверяет, похожа ли ссылка на страницу с текстом."""
    # Отсекаем навигационные, служебные и медиа-файлы
    skip_patterns = [
        r'\.(jpg|jpeg|png|gif|pdf|zip|rar|doc|docx)$',
        r'/soft/',
        r'/about/',
        r'/meta/',
        r'/search',
        r'/index\.htm$',
        r'/toc\.htm$',  # оглавления
        r'/links\.htm$',
        r'/default\.asp$',
    ]
    url_lower = url.lower()
    for pattern in skip_patterns:
        if re.search(pattern, url_lower):
            return False
    # Считаем текстом всё, что находится в /text/ или оканчивается на .htm
    if '/text/' in url_lower or url_lower.endswith('.htm') or url_lower.endswith('.html'):
        return True
    return False

def sanitize_filename(url):
    """Создаёт безопасное имя файла из URL."""
    parsed = urlparse(url)
    name = parsed.path.strip('/').replace('/', '_')
    name = re.sub(r'[\\/*?:"<>|]', "_", name)
    if not name.endswith('.txt'):
        name += '.txt'
    return name

# --- Основная логика ---

def crawl(start_urls):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    visited = set()
    queue = list(start_urls)
    downloaded_count = 0

    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        print(f"[{downloaded_count}] Обрабатываю: {url}")
        html = get_html(url)
        if not html:
            continue

        # Если это похоже на страницу с текстом — сохраняем
        if is_text_page(url):
            text = extract_text(html)
            if len(text) > 500:  # отсекаем пустышки
                filename = sanitize_filename(url)
                filepath = os.path.join(OUTPUT_DIR, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(text)
                downloaded_count += 1
                print(f"  ✓ Сохранено ({len(text)} симв.): {filename}")
            else:
                print(f"  - Пропущено (мало текста)")

        # Ищем ссылки для дальнейшего обхода
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            # Преобразуем относительные ссылки в абсолютные
            full_url = urljoin(url, href)
            # Ограничиваемся только доменом rvb.ru
            if full_url.startswith(BASE_URL) and full_url not in visited:
                queue.append(full_url)

        time.sleep(DELAY)

    print(f"\nГотово. Скачано файлов: {downloaded_count}")

if __name__ == "__main__":
    crawl(START_URLS)
