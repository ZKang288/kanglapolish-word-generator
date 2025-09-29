import streamlit as st
import random
from datetime import datetime

# === Phonetic rules ===
vowels = ['a', 'e', 'i', 'o', 'u', 'ou', 'ü']
complex_vowels = ['ae', 'ai','ao','ie','eo','iu','ei','oi','ui','uai']
consonants = ['b', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'th','z','y']
complex_consonants = ['zh', 'czh', 'ch','sh']
end_consonants = ['m','n','ng','k','t']

# === Kangpatsa translation ===
def kangpatsa(message):
    translation = {
        "b": 'ᥙ', 'p': 'ᥚ', 'd': 'ဒ', 'k': 'ᥐ', 'g': 'ᥠ', 'h': 'ᥑ',
        'ng': 'ᥒ', 't': 'ᥖ', 'th': 'ᥗ', 'f': 'ဖ', 'l': 'ᥘ', 'r': 'ລ',
        'm': 'ᥛ', 'n': 'ᥢ', 'z': 'ဈ', 'zh': 'ဈ', 'czh': 'ᥔ', 'c': 'ᥟ',
        'ch': 'ᥡ', 's': 'ᥞ', 'sh': 'ဆ', 'j': 'စ', 'y': 'ᥕ', 'a': 'ᥣ',
        'ai': 'ᥭ', 'ao': 'ᥝ', 'i': 'ᥤ', 'ü': 'ᥪ', 'ie': 'ᥬ', 'io': 'ᥬᥩ',
        'eo': 'ᥬᥩ', 'iu': 'ᥤᥝ', 'e': 'ᥫ', 'ei': 'ᥥ', 'ae': 'ᥦ', 'ou': 'ᥩ',
        'o': 'ᥨ', 'oi': 'ᥨᥭ', 'u': 'ᥧ', 'ui': 'ᥧᥤ', 'uai': 'ᥧᥭ', "'": "-"
    }
    result = ""
    i = 0
    while i < len(message):
        if i < len(message) - 2 and message[i:i+3] in translation:
            result += translation[message[i:i+3]]
            i += 3
        elif i < len(message) - 1 and message[i:i+2] in translation:
            result += translation[message[i:i+2]]
            i += 2
        else:
            result += translation.get(message[i], message[i])
            i += 1
    return result

# === Word generator ===
def generate_syllable():
    patterns = [
        lambda: random.choice(vowels) + random.choice(end_consonants),
        lambda: random.choice(consonants) + random.choice(vowels) + random.choice(end_consonants),
        lambda: random.choice(consonants) + random.choice(complex_vowels) + random.choice(end_consonants),
        lambda: random.choice(consonants) + random.choice(vowels),
        lambda: random.choice(consonants) + random.choice(complex_vowels),
        lambda: random.choice(complex_consonants) + random.choice(vowels) + random.choice(end_consonants),
        lambda: random.choice(complex_consonants) + random.choice(complex_vowels),
    ]
    return random.choice(patterns)()

def generate_word():
    syllable_count = random.randint(2, 4)
    word = ''.join(generate_syllable() for _ in range(syllable_count))
    return word.capitalize(), kangpatsa(word)

# === Streamlit UI ===
st.title("📝 Kanglapolish Word Generator")

num_words = st.number_input("How many words to generate?", min_value=1, max_value=50, value=5)
if st.button("Generate"):
    results = [generate_word() for _ in range(num_words)]
    for romanized, script in results:
        st.write(f"**{romanized}** → {script}")

    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"kanglapolish_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for romanized, script in results:
            f.write(f"{romanized} → {script}\n")

    with open(filename, "r", encoding="utf-8") as f:
        st.download_button("💾 Download Results", f.read(), file_name=filename)
