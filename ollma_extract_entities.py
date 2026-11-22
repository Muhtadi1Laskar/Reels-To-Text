# import json
# import ollama
# from utils import generate_file_path, parse_file_name


# def extract_recommendations(transcript):
#     response = ollama.chat(
#         model="qwen2.5:1.5b",
#         messages=[
#             {
#                 "role": "system",
#                 "content": """
#         You are a strict named-work extraction system.

#         Your task is to identify explicitly mentioned titles of:
#         - Books
#         - Comics and graphic novels
#         - Movies
#         - TV shows

#         IMPORTANT RULES:

#         1. Extract only actual named works.
#         2. A title must be a proper name identifying a specific work.
#         3. NEVER extract plot descriptions, summaries, character descriptions,
#         dialogue, ordinary sentences, or recommendations as titles.
#         4. NEVER convert a description into a title.
#         5. A sentence describing a story is NOT a title.
#         6. A character's name is NOT a title unless it is also explicitly
#         the name of a work.
#         7. If you cannot confidently identify a specific work title,
#         do not include it.
#         8. Do not invent missing information.
#         9. Do not infer titles from descriptions.
#         10. Prefer returning fewer correct results over many uncertain results.

#         Examples:

#         Input:
#         "I recommend Gideon Falls. It's about a priest arriving in
#         a rural town."

#         Correct:
#         Gideon Falls

#         Incorrect:
#         "A priest arriving in a rural town"

#         Input:
#         "Something Is Killing the Children is a fantastic comic.
#         Children are disappearing in the woods."

#         Correct:
#         Something Is Killing the Children

#         Incorrect:
#         "Children are disappearing in the woods"

#         Return valid JSON only.
#     """,
#             },
#             {
#                 "role": "user",
#                 "content": f"""
#     Extract explicitly named works from this transcript:

#     {transcript}

#     Return this JSON structure:

#     {{
#         "items": [
#             {{
#                 "title": "Exact title as mentioned",
#                 "creator": null,
#                 "recommendation": false
#             }}
#         ]
#     }}

#     Return an empty items array if no identifiable works are mentioned.
# """,
#             },
#         ],
#         format="json",
#         options={"temperature": 0, "num_predict": 2000, "num_ctx": 4096},
#     )

#     print(response.message.content)

#     content = response.message.content


#     # print("\n========== OLLAMA DIAGNOSTICS ==========")
#     # print("Request completed:", response.done)
#     # print("Done reason:", getattr(response, "done_reason", "Not available"))
#     # print("Prompt tokens:", getattr(response, "prompt_eval_count", "Not available"))
#     # print("Generated tokens:", getattr(response, "eval_count", "Not available"))

#     # print("\nRaw response:")
#     # print(repr(content))

#     # print("\nResponse length:", len(content))
#     # print("========================================\n")

#     try:
#         result = json.loads(content)
#         # return response.message.content
#         return result

#     except json.JSONDecodeError as error:
#         print("JSON parsing failed!")
#         print("Error:", error)
#         print("Problematic section:")
#         print(repr(content[max(0, error.pos - 100) : error.pos + 100]))

#         return None


# def read_files(path):
#     with open(path, "r", encoding="utf-8") as file:
#         content = file.read()

#         return content


# if __name__ == "__main__":
#     file_name, url = parse_file_name()
#     file_name = f"{file_name}.txt"

#     print("Running", file_name, url)

#     text_file_path = generate_file_path("output-text", file_name)

#     transcript = read_files(text_file_path)

#     results = extract_recommendations(transcript)

#     print(json.dumps(results, indent=4, ensure_ascii=False))


import json
from pathlib import Path

import ollama

from utils import generate_file_path, parse_file_name

# SYSTEM_PROMPT = """
# You are a strict named-work extraction system.

# Your task is to identify explicitly mentioned titles of:
# - Books
# - Comics and graphic novels
# - Movies
# - TV shows

# IMPORTANT RULES:

# 1. Extract only actual named works.
# 2. A title must be a proper name identifying a specific work.
# 3. NEVER extract plot descriptions, summaries, character descriptions, 
# dialogue, ordinary sentences, or recommendations as titles.
# 4. NEVER convert a description into a title.
# 5. A sentence describing a story is NOT a title.
# 6. A character's name is NOT a title unless it is also explicitly
# the name of a work.
# 7. If you cannot confidently identify a specific work title,
# do not include it.
# 8. Do not invent missing information.
# 9. Do not infer titles from descriptions.
# 10. Prefer returning fewer correct results over many uncertain results.

# Examples:

# Input:
# "I recommend Gideon Falls. It's about a priest arriving in a rural town."

# Correct:
# {"items": ["Gideon Falls"]}

# Incorrect:
# {"items": ["A priest arriving in a rural town"]}

# Input:
# "Something Is Killing the Children is a fantastic comic.
# Children are disappearing in the woods."

# Correct:
# {"items": ["Something Is Killing the Children"]}

# Incorrect:
# {"items": ["Children are disappearing in the woods"]}

# Return valid JSON only.
# """

SYSTEM_PROMPT = """
You are a strict named-work extraction system.

Your task is to identify explicitly mentioned titles of:
- Books
- Comics and graphic novels
- Movies
- TV shows

IMPORTANT RULES:

1. Extract only actual named works.
2. A title must be a proper name identifying a specific work.
3. NEVER extract plot descriptions, summaries, character descriptions,
dialogue, ordinary sentences, or recommendations as titles.
4. NEVER convert a description into a title.
5. A sentence describing a story is NOT a title.
6. A character's name is NOT a title unless it is also explicitly
the name of a work.
7. If you cannot confidently identify a specific work title,
do not include it.
8. Do not invent missing information.
9. Do not infer titles from descriptions.
10. Prefer returning fewer correct results over many uncertain results.

Examples:

Input:
"I recommend Gideon Falls. It's about a priest arriving in
a rural town."

Correct:
Gideon Falls

Incorrect:
"A priest arriving in a rural town"

Input:
"Something Is Killing the Children is a fantastic comic.
Children are disappearing in the woods."

Correct:
Something Is Killing the Children

Incorrect:
"Children are disappearing in the woods"

Return valid JSON only.
"""


FORMAT_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {"type": "string"},
        }
    },
    "required": ["items"],
}


def extract_recommendations(transcript):
    response = ollama.chat(
        model="qwen2.5:1.5b",  # upgrade to qwen2.5:7b or qwen3:4b if quality is poor
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Extract explicitly named works from this transcript:\n\n"
                    f"{transcript}\n\n"
                    'Return {"items": ["Exact title as mentioned", ...]}.\n'
                    "Use the exact title as mentioned in the transcript.\n"
                    "Return an empty items array if no identifiable works are mentioned."
                ),
            },
        ],
        format=FORMAT_SCHEMA,
        options={
            "temperature": 0,
            "num_ctx": 4096,
            "num_predict": 256,
            "repeat_penalty": 1.2,
            "repeat_last_n": 128,
        },
    )

    content = response.message.content

    # Truncated output is the failure mode you hit before — detect it explicitly
    if response.done_reason == "length":
        print("Output truncated!")
        print("Prompt tokens:", response.prompt_eval_count)
        print("Generated tokens:", response.eval_count)
        print("Increase num_predict/num_ctx or chunk the transcript.")
        return None

    try:
        data = json.loads(content)
    except json.JSONDecodeError as error:
        print("JSON parsing failed!")
        print("Error:", error)
        print("Problematic section:")
        print(repr(content[max(0, error.pos - 100) : error.pos + 100]))
        return None

    # Dedupe while preserving order (insurance against small-model repetition loops)
    titles = list(
        dict.fromkeys(
            t.strip()
            for t in data.get("items", [])
            if isinstance(t, str) and t.strip()
        )
    )

    # Rebuild your original object shape in Python — costs zero model tokens
    return {
        "items": [
            {"title": title, "creator": None, "recommendation": False}
            for title in titles
        ]
    }


def read_files(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    file_name, url = parse_file_name()
    file_name_with_extension = f"{file_name}.txt"


    text_file_path = generate_file_path("output-text", file_name_with_extension)
    transcript = read_files(text_file_path)

    results = extract_recommendations(transcript)

    if results is not None:
        output_dir = Path("output-results")
        output_dir.mkdir(exist_ok=True)

        output_path = output_dir / f"{file_name}.json"

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)

    print(json.dumps(results, indent=4, ensure_ascii=False))