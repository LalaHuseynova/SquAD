import json

# İngilis və Azərbaycan faylları
FILE_EN = "train_50_simple.json"
FILE_AZ = "results/train_50_az2_cursor.json"

# Nəticə faylı
OUTPUT_FILE = "results/compare_answers.json"


# JSON faylı oxumaq üçün funksiya
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Məlumatları oxuyuruq
data_en = load_json(FILE_EN)
data_az = load_json(FILE_AZ)


# Azərbaycan faylını id-ə görə dictionary edirik ki, tez tapaq
az_by_id = {item["id"]: item for item in data_az}


# Müqayisə nəticələri burada saxlanacaq
compared_data = []


# İngilis fayldakı elementləri gəz
for item_en in data_en:
    qid = item_en["id"]

    # Əgər bu id Azərbaycan faylında da varsa
    if qid in az_by_id:
        item_az = az_by_id[qid]

        compared_data.append({
            "id": qid,
            "answer_en": item_en.get("answer", ""),
            "answer_az": item_az.get("answer", "")
        })


# Nəticəni JSON faylına yaz
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(compared_data, f, ensure_ascii=False, indent=2)


print(f"Saved {len(compared_data)} compared items to {OUTPUT_FILE}")