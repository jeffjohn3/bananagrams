# Generates words.txt for the Bananagrams helper page.
# Requires: pip install wordfreq
from urllib.request import urlopen
from wordfreq import top_n_list, zipf_frequency

# --- Configuration ---
OUTPUT_FILE = 'words.txt'
TOP_N = 20000
MIN_ZIPF = 2.5

# ENABLE is a public-domain word game dictionary. Requiring words to be in it
# drops proper nouns (names, places, brands) and abbreviations.
DICTIONARY_URL = 'https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt'

# Common modern words missing from ENABLE (published in 2000)
EXTRA_WORDS = {
    'app', 'apps', 'blog', 'blogs', 'email', 'emails', 'hashtag', 'internet',
    'offline', 'online', 'podcast', 'podcasts', 'selfie', 'smartphone',
    'smartphones', 'texting', 'website', 'websites', 'wifi'
}

def load_dictionary(url):
    with urlopen(url) as response:
        return {line.strip().lower() for line in response.read().decode('utf-8').splitlines()}

def generate_filtered_wordlist(output_file):
    print(f"Generating '{output_file}'... (this takes a moment)")
    dictionary = load_dictionary(DICTIONARY_URL) | EXTRA_WORDS
    valid_words = []
    word_list = top_n_list('en', TOP_N)

    for word in word_list:
        word = word.lower()
        if len(word) < 2 or word not in dictionary:
            continue
        if zipf_frequency(word, 'en') >= MIN_ZIPF:
            valid_words.append(word)

    valid_words.sort(key=lambda w: (len(w), w))
    with open(output_file, mode='w', encoding='utf-8') as f:
        for word in valid_words:
            f.write(f"{word}\n")
    print(f"Wrote {len(valid_words)} words to '{output_file}'")

if __name__ == "__main__":
    generate_filtered_wordlist(OUTPUT_FILE)
