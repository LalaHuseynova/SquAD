import json
import re

INPUT_FILE = "train_50_simple.json"
OUTPUT_FILE = "sentences_with_answers.json"


def extract_sentence(context, answer):
    sentences = re.split(r'(?<=[.!?])\s+', context)

    for sentence in sentences:
        if answer in sentence:
            return sentence.strip()

    return None


def process_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for item in data:
        context = item.get("context", "")
        answer = item.get("answer", "")
        answer_start = item.get("answer_start", -1)

        sentence = extract_sentence(context, answer)

        # keep everything + add new field
        new_item = {
            "id": item.get("id"),
            "title": item.get("title"),
            "context": context,
            "question": item.get("question"),
            "answer": answer,
            "answer_start": answer_start,
            "sentence_with_answer": sentence
        }

        results.append(new_item)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    process_file(INPUT_FILE, OUTPUT_FILE)