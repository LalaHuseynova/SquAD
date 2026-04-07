import json
# 1000 suali goturub simple sekilde yazir

INPUT_FILE = "train-v1.1.json"
OUTPUT_FILE = "train_50_simple.json"
LIMIT = 50

simplified_data = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    squad_data = json.load(f)

count = 0

for article in squad_data["data"]:
    title = article.get("title", "")
    
    for paragraph in article["paragraphs"]:
        context = paragraph["context"]
        
        for qa in paragraph["qas"]:
            # Cavab yoxdusa skip ele
            if "answers" not in qa or len(qa["answers"]) == 0:
                continue

            first_answer = qa["answers"][0]

            simplified_item = {
                "title": title,
                "context": context,
                "question": qa["question"],
                "answer": first_answer["text"],
                "answer_start": first_answer["answer_start"],
                "id": qa["id"]
            }

            simplified_data.append(simplified_item)
            count += 1

            if count >= LIMIT:
                break
        
        if count >= LIMIT:
            break
    
    if count >= LIMIT:
        break

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(simplified_data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(simplified_data)} simplified QA pairs to {OUTPUT_FILE}")