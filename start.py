import json
from difflib import SequenceMatcher

INPUT_FILE = "translated_only_az.json"
OUTPUT_FILE = "translated_with_answer_start_az.json"


def normalize_text(text):
    if not text:
        return ""

    text = text.lower().strip()
    text = " ".join(text.split())
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    return text


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def approximate_char_match(context, candidate, threshold=0.82):
    if not context or not candidate:
        return -1

    best_idx = -1
    best_score = 0.0
    n = len(candidate)

    min_len = max(1, n - 5)
    max_len = min(len(context), n + 5)

    for window_size in range(min_len, max_len + 1):
        for i in range(len(context) - window_size + 1):
            chunk = context[i:i + window_size]
            score = similarity(chunk.lower(), candidate.lower())

            if score > best_score:
                best_score = score
                best_idx = i

    if best_score >= threshold:
        return best_idx

    return -1


def generate_candidates(answer, answer_az):
    candidates = []

    for x in [answer_az, answer]:
        if x and x not in candidates:
            candidates.append(x)

    return candidates


def find_answer_start_az(context_az, answer, answer_az):
    if not context_az:
        return -1

    candidates = generate_candidates(answer, answer_az)

    # 1. exact search
    for candidate in candidates:
        idx = context_az.find(candidate)
        if idx != -1:
            return idx

    # 2. normalized search
    context_norm = normalize_text(context_az)

    for candidate in candidates:
        candidate_norm = normalize_text(candidate)
        idx = context_norm.find(candidate_norm)
        if idx != -1:
            return idx

    # 3. char-by-char approximate search
    for candidate in candidates:
        idx = approximate_char_match(context_az, candidate, threshold=0.82)
        if idx != -1:
            return idx

    return -1


def process_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_data = []
    total = 0
    failed = 0

    for i, item in enumerate(data, start=1):
        print(f"Processing {i}/{len(data)} - {item.get('id', '')}")

        context_az = item.get("context_az", "")
        answer = item.get("answer", "")
        answer_az = item.get("answer_az", "")

        answer_start_az = find_answer_start_az(context_az, answer, answer_az)

        item["answer_start_az"] = answer_start_az
        updated_data.append(item)

        total += 1
        if answer_start_az == -1:
            failed += 1

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=2, ensure_ascii=False)

    print(f"Done. Saved to {output_file}")
    print(f"Total: {total}")
    print(f"Failed: {failed}")
    print(f"Success: {total - failed}")
    print(f"Accuracy: {(total - failed) / total * 100:.2f}%")


if __name__ == "__main__":
    process_file(INPUT_FILE, OUTPUT_FILE)