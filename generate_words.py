# Generates words.txt for the Bananagrams helper page.
# Requires: pip install wordfreq
import io
import tarfile
from urllib.error import URLError
from urllib.request import urlopen
from wordfreq import iter_wordlist, zipf_frequency

# --- Configuration ---
OUTPUT_FILE = 'words.txt'
MIN_ZIPF = 2.0

# ENABLE is a public-domain word game dictionary. Requiring words to be in it
# drops abbreviations and other words that aren't valid in word games.
DICTIONARY_URL = 'https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt'

# SCOWL ranks spellchecker words by how common they are (10 = most common,
# 60 = large dictionary, 95 = everything) and keeps proper nouns in separate
# lists. Requiring words to be in it drops names and obscure words.
SCOWL_URL = 'https://downloads.sourceforge.net/project/wordlist/SCOWL/2020.12.07/scowl-2020.12.07.tar.gz'
SCOWL_MAX_SIZE = 60
SCOWL_LISTS = {'english', 'american', 'british', 'variant_1'}

# Common words missing from ENABLE (published in 2000) or SCOWL
EXTRA_WORDS = {
    'app', 'apps', 'blog', 'blogs', 'cafe', 'cafes', 'donut', 'donuts',
    'email', 'emails', 'hashtag', 'internet', 'lockdown', 'offline', 'online',
    'podcast', 'podcasts', 'selfie', 'smartphone', 'smartphones', 'texting',
    'website', 'websites', 'wifi'
}

# Slurs, plus names and obscure words that get past the filters
EXCLUDE_WORDS = {
    'chink', 'chinks', 'coon', 'coons', 'dyke', 'dykes', 'fag', 'faggot',
    'faggots', 'fags', 'gook', 'gooks', 'gyp', 'homo', 'homos', 'nigger',
    'niggers', 'retard', 'retards', 'wop', 'wops',
    'alb', 'charlie', 'ecu', 'ens', 'hie', 'nae', 'nus'
}

def download(url, attempts=3):
    # SourceForge redirects to a random mirror, so retrying usually gets a working one
    for attempt in range(attempts):
        try:
            with urlopen(url) as response:
                return response.read()
        except URLError:
            if attempt == attempts - 1:
                raise

def load_enable(url):
    return {line.strip().lower() for line in download(url).decode('utf-8').splitlines()}

def load_scowl(url):
    words = set()
    with tarfile.open(fileobj=io.BytesIO(download(url)), mode='r:gz') as tar:
        for member in tar.getmembers():
            # e.g. scowl-2020.12.07/final/american-words.50
            folder, _, name = member.name.rpartition('/')
            kind, _, size = name.partition('-words.')
            if folder.endswith('/final') and kind in SCOWL_LISTS and size.isdigit() and int(size) <= SCOWL_MAX_SIZE:
                for line in tar.extractfile(member).read().decode('latin-1').splitlines():
                    # Proper nouns and abbreviations are capitalized
                    if line.isascii() and line.isalpha() and line.islower():
                        words.add(line)
    return words

def generate_filtered_wordlist(output_file):
    print(f"Generating '{output_file}'... (this takes a moment)")
    dictionary = (load_enable(DICTIONARY_URL) & load_scowl(SCOWL_URL)) | EXTRA_WORDS
    valid_words = []

    # Words come in order of decreasing frequency
    for word in iter_wordlist('en'):
        if zipf_frequency(word, 'en') < MIN_ZIPF:
            break
        word = word.lower()
        if len(word) < 2 or word not in dictionary or word in EXCLUDE_WORDS:
            continue
        valid_words.append(word)

    valid_words = sorted(set(valid_words), key=lambda w: (len(w), w))
    with open(output_file, mode='w', encoding='utf-8') as f:
        for word in valid_words:
            f.write(f"{word}\n")
    print(f"Wrote {len(valid_words)} words to '{output_file}'")

if __name__ == "__main__":
    generate_filtered_wordlist(OUTPUT_FILE)
