import csv
import os
from datetime import datetime, timedelta

# Эта строка заставит скрипт всегда создавать файл рядом с самим собой
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(BASE_DIR, "corpus_registry.csv")
STALE_DAYS = 90  # если документ не проверялся 90 дней — напомнить

FIELDS = [
    "doc_id", "doc_type", "title", "date", "status",
    "last_checked", "replaced_by", "source", "file_path",
    "pages", "has_ocr", "airport_specific", "chunking_strategy",
    "chunk_count", "notes"
]

def init_registry():
    """Создаёт пустой реестр, если его нет."""
    if not os.path.exists(REGISTRY_PATH):
        # Создаем папку, только если путь содержит директорию
        folder = os.path.dirname(REGISTRY_PATH)
        if folder:
            os.makedirs(folder, exist_ok=True)
            
        with open(REGISTRY_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
        print(f"Создан новый реестр: {REGISTRY_PATH}")

def load_registry():
    with open(REGISTRY_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_registry(rows):
    with open(REGISTRY_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def check_stale(rows):
    """Показывает документы, которые давно не проверялись."""
    today = datetime.today().date()
    stale = []
    for row in rows:
        if row["status"] != "действующий":
            continue
        last = row.get("last_checked", "").strip()
        if not last:
            stale.append((row["doc_id"], "нет даты проверки"))
            continue
        try:
            last_date = datetime.strptime(last, "%Y-%m-%d").date()
        except ValueError:
            stale.append((row["doc_id"], f"некорректная дата: {last}"))
            continue
        if (today - last_date).days > STALE_DAYS:
            stale.append((row["doc_id"], f"не проверялся {(today - last_date).days} дней"))

    if stale:
        print("\n⚠️  Документы, требующие проверки актуальности:")
        for doc_id, reason in stale:
            print(f"  - {doc_id}: {reason}")
    else:
        print("\n✅ Все действующие документы проверены недавно.")

def mark_outdated(doc_id, replaced_by):
    """Помечает документ как утративший силу и указывает замену."""
    rows = load_registry()
    found = False
    for row in rows:
        if row["doc_id"] == doc_id:
            row["status"] = "утратил силу"
            row["replaced_by"] = replaced_by
            row["last_checked"] = datetime.today().strftime("%Y-%m-%d")
            found = True
            break
    if found:
        save_registry(rows)
        print(f"✅ {doc_id} помечен как 'утратил силу', замена: {replaced_by}")
    else:
        print(f"❌ Документ {doc_id} не найден в реестре.")

if __name__ == "__main__":
    init_registry()
    rows = load_registry()
    print(f"Всего документов в реестре: {len(rows)}")
    check_stale(rows)

    # Пример: пометить устаревший документ (раскомментируйте, если нужно)
    # mark_outdated("tk_eaeu_2022", "tk_eaeu_2024")