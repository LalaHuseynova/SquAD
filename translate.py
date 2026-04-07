import json

from cache import (
    translate_text,
    context_cache,
    question_cache,
    answer_cache,
    title_cache,
    sentence_cache,
)

INPUT_FILE = "sentences_with_answers.json"
OUTPUT_FILE = "translated_only_az.json"


def normalize_text(text):
    # Mətn boşdursa, boş string qaytar
    if not text:
        return ""

    # Mətnin əvvəl-son boşluqlarını sil, kiçik hərfə çevir
    # və birdən çox boşluğu tək boşluğa endir
    return " ".join(text.strip().lower().split())


def choose_answer_translation(answer, answer_az, sentence_az):
    answer_norm = normalize_text(answer)  # Orijinal cavabı normalize et
    answer_az_norm = normalize_text(answer_az)   # Tərcümə olunmuş cavabı normalize et
    sentence_az_norm = normalize_text(sentence_az)     # Cavab olan cümlənin Azərbaycan dilinə tərcüməsini normalize et
    # 1-ci hal:
    # Əgər tərcümə olunmuş cavab tərcümə olunmuş cümlənin içində varsa,
    # deməli cavab düzgün tərcümə olunub, onu saxlayırıq
    if answer_az_norm and answer_az_norm in sentence_az_norm:
        return answer_az

    # 2-ci hal:
    # Əgər orijinal cavab hələ də tərcümə olunmuş cümlənin içində qalırsa,
    # bu adətən xüsusi ad, qəzet adı, şəxs adı və s. olur
    # belə halda tərcümə etmədən orijinal cavabı saxlayırıq
    if answer_norm and answer_norm in sentence_az_norm:
        return answer

    # if sentence_az:
    #     return sentence_az

    return answer_az


def process_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Yeni tərcümə olunmuş nəticələri burada saxlayacağıq
    translated_data = []

    for i, item in enumerate(data, start=1):
        print(f"Processing {i}/{len(data)} - {item.get('id', '')}")

        # Lazım olan sahələri JSON-dan götür
        title = item.get("title", "")
        context = item.get("context", "")
        question = item.get("question", "")
        answer = item.get("answer", "")
        answer_start = item.get("answer_start", -1)
        sentence_with_answer = item.get("sentence_with_answer", "")

        title_az = translate_text(title, title_cache)
        context_az = translate_text(context, context_cache)
        question_az = translate_text(question, question_cache)
        answer_az_raw = translate_text(answer, answer_cache)
        sentence_with_answer_az = translate_text(sentence_with_answer, sentence_cache)

        # Cavabın hansı versiyasını saxlayacağımıza qərar ver:
        # - tərcümə olunmuş variantı?
        # - yoxsa orijinalı?
        answer_az = choose_answer_translation(
            answer=answer,
            answer_az=answer_az_raw,
            sentence_az=sentence_with_answer_az,
        )

        translated_item = {
            "id": item.get("id", ""),
            "title": title,
            "title_az": title_az,
            "context": context,
            "context_az": context_az,
            "question": question,
            "question_az": question_az,
            "answer": answer,
            "answer_az": answer_az,
            "answer_start": answer_start,
            "sentence_with_answer": sentence_with_answer,
            "sentence_with_answer_az": sentence_with_answer_az,
        }

        # Hazır obyekti nəticə siyahısına əlavə et
        translated_data.append(translated_item)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(translated_data, f, indent=2, ensure_ascii=False)

    print(f"Done. Saved to {output_file}")


if __name__ == "__main__":
    process_file(INPUT_FILE, OUTPUT_FILE)