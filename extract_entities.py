import json

from gliner import GLiNER
from utils import generate_file_path, parse_file_name

MODEL_NAME = "gliner-community/gliner_small-v2.5"

print("Loading Model...")

model = GLiNER.from_pretrained(MODEL_NAME)

def extract_entities(transcript):
    labels = ["movie title", "book title", "author name", "film director"]
    entities = model.predict_entities(transcript, labels, threshold=0.4)

    results = {"movies": [], "books": [], "authors": [], "directors": []}

    mapping = {
        "movie title": "movies",
        "book title": "books",
        "author name": "authors",
        "film directors": "directors",
    }

    for entity in entities:
        category = mapping.get(entity["label"])

        if category:
            results[category].append(
                {"title": entity["text"], "confidence": entity["score"]}
            )

    return results


def read_files(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

        return content


if __name__ == "__main__":

    file_name, _ = parse_file_name()
    file_name = f"{file_name}.txt"

    text_file_path = generate_file_path("output-text", file_name)

    transcript = read_files(text_file_path)
    results = extract_entities(transcript)

    filtered_result = []
    seen_names = set()

    for book in results.get("books"):
        name = book.get("title")
        confidence = book.get("confidence")

        if name:
            if name.lower() not in seen_names and confidence > 0.4:
                seen_names.add(name.lower())
                filtered_result.append({"name": name, "confidence": confidence})

    print(json.dumps(filtered_result, indent=4))

