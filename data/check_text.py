import os
from docx import Document

# Укажите путь к вашему DOCX-файлу
file_path = r"C:/Users/1/Desktop/Lessons/Dipl/Diploma/data/raw/Reshenie Kollegii N141 o tranzitnoy deklaracii.docx" 

if not os.path.exists(file_path):
    print(f"❌ Файл не найден: {file_path}")
else:
    try:
        # Загружаем DOCX
        doc = Document(file_path)
        
        print(f"📄 Документ: {file_path}")
        print(f"Абзацев (параграфов): {len(doc.paragraphs)}")
        
        # Собираем текст из первых 5 абзацев для проверки
        extracted_text = ""
        for p in doc.paragraphs[:5]:
            if p.text.strip(): # пропускаем пустые строки
                extracted_text += p.text + "\n"
            
        if len(extracted_text.strip()) == 0:
            print("⚠️ Текст не извлекается! Возможно, документ пуст.")
        else:
            print("✅ Текст читается! Вот первые 300 символов:\n")
            print("-" * 40)
            print(extracted_text[:300])
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")