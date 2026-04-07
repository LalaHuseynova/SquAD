import json

INPUT_FILE = "translated_only_az.json"
OUTPUT_FILE = "translated_with_answer_start_az.json"


def normalize_text(text):
    # Mətn boşdursa, boş string qaytar
    if not text:
        return ""

    # Kiçik hərfə çevir, sətir sonlarını və artıq boşluqları sil
    text = text.lower().strip()
    text = " ".join(text.split())

    # Dırnaq işarələrini eyniləşdir
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")

    return text


def find_answer_start_az(context_az, answer_az, sentence_az):
    # Kontekst və cavab yoxdursa, tapmaq mümkün deyil
    if not context_az or not answer_az:
        return -1

    # Əvvəl orijinal mətndə exact search et
    idx = context_az.find(answer_az)
    if idx != -1:
        return idx

    # Normalize olunmuş formada axtar
    context_norm = normalize_text(context_az)
    answer_norm = normalize_text(answer_az)
    sentence_norm = normalize_text(sentence_az)

    # 1. Cavabı bütün kontekstdə axtar
    idx_norm = context_norm.find(answer_norm)
    if idx_norm != -1:
        return idx_norm

    # 2. Əgər cümlə varsa, əvvəl cümləni kontekstdə tap, “Əgər mən cavab olan cümləni context-də tapsam, onda cavabı həmin cümlənin içindən çıxararam
    if sentence_norm:
        sentence_idx = context_norm.find(sentence_norm)

        if sentence_idx != -1:
            # Sonra cavabı cümlənin içində axtar
            local_idx = sentence_norm.find(answer_norm)

            if local_idx != -1:
                return sentence_idx + local_idx

            # Cavab tapılmasa, heç olmasa cümlənin başlanğıcını qaytar
            return sentence_idx

    return -1


def process_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_data = []

    # counters
    total = 0
    failed = 0

    for i, item in enumerate(data, start=1):
        print(f"Processing {i}/{len(data)} - {item.get('id', '')}")

        context_az = item.get("context_az", "")
        answer_az = item.get("answer_az", "")
        sentence_az = item.get("sentence_with_answer_az", "")

        answer_start_az = find_answer_start_az(context_az, answer_az, sentence_az)

        # count
        total += 1
        if answer_start_az == -1:
            failed += 1

        item["answer_start_az"] = answer_start_az
        updated_data.append(item)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=2, ensure_ascii=False)

    print(f"Done. Saved to {output_file}")

    print("\n===== RESULTS =====")
    print(f"Total: {total}")
    print(f"Failed (-1): {failed}")
    print(f"Success: {total - failed}")
    print(f"Accuracy: {(total - failed) / total * 100:.2f}%")


if __name__ == "__main__":
    process_file(INPUT_FILE, OUTPUT_FILE)