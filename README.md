# 🍌 Bananagrams Helper

**Live site:** https://jeffjohn3.github.io/bananagrams/

Enter a root word to find common English words that are 1–3 letters longer and use all of its letters. Results are grouped by how many letters you add, sorted by tile score, and the added letters are highlighted. Tap any result to use it as the next root word.

It's a static page, so everything runs in the browser and no server is needed.

## Regenerating the word list

`words.txt` is built from the [wordfreq](https://pypi.org/project/wordfreq/) package. To exclude proper nouns and abbreviations, the list is filtered against the public-domain [ENABLE](https://github.com/dolph/dictionary) word game dictionary.

```
pip install wordfreq
python generate_words.py
```
