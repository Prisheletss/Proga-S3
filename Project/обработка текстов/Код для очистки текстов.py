from pathlib import Path

for path in Path("./rvb_texts").glob("*.txt"):
    text = path.read_text(encoding="utf-8")
    parts = text.split("Close", 1)
    if len(parts) == 2:                    
        path.write_text(parts[1], encoding="utf-8")
    else:
        print(f"Пропущен (нет Close): {path.name}")
