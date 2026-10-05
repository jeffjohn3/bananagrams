# Generates words.txt for the Bananagrams helper page.
# Requires: pip install wordfreq
from wordfreq import top_n_list, zipf_frequency

# --- Configuration ---
OUTPUT_FILE = 'words.txt'
TOP_N = 20000
MIN_ZIPF = 2.5

TILE_VALUES = {
    'A': 13, 'B': 3, 'C': 3, 'D': 6, 'E': 18, 'F': 3,
    'G': 4, 'H': 3, 'I': 12, 'J': 2, 'K': 2, 'L': 5,
    'M': 3, 'N': 8, 'O': 11, 'P': 3, 'Q': 2, 'R': 9,
    'S': 6, 'T': 9, 'U': 6, 'V': 3, 'W': 3, 'X': 2,
    'Y': 3, 'Z': 2
}

def generate_filtered_wordlist(output_file):
    print(f"Generating '{output_file}'... (this takes a moment)")
    valid_entries = []
    word_list = top_n_list('en', TOP_N)

    for word in word_list:
        if len(word) < 2 or not word.isalpha():
            continue
        if zipf_frequency(word, 'en') >= MIN_ZIPF:
            score = sum(TILE_VALUES.get(char.upper(), 0) for char in word)
            valid_entries.append((word.lower(), score))

    valid_entries.sort(key=lambda x: (len(x[0]), -x[1]))
    with open(output_file, mode='w', encoding='utf-8') as f:
        for word, _ in valid_entries:
            f.write(f"{word}\n")
    print(f"Wrote {len(valid_entries)} words to '{output_file}'")

if __name__ == "__main__":
    generate_filtered_wordlist(OUTPUT_FILE)
