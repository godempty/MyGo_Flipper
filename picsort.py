import os
import json


def number_images(folder="./static/pics", output_json="words.json"):
    # Ensure the folder exists
    if not os.path.exists(folder):
        print(f"Folder '{folder}' not found.")
        return

    # Get all jpg files in the folder
    jpg_files = [f for f in os.listdir(folder) if f.lower().endswith(".jpg")]
    jpg_files.sort()
    # assign arbitrary numbers
    numbered_images = {i + 1: file[:-4] for i, file in enumerate(jpg_files)}

    # Save to JSON with UTF-8 encoding
    with open(output_json, "w", encoding="utf-8") as json_file:
        json.dump(numbered_images, json_file, indent=4, ensure_ascii=False)

    print(f"{len(jpg_files)} Numbered image mapping saved to '{output_json}'.")


if __name__ == "__main__":
    number_images()
