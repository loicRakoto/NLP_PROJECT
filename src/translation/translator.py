# Traduit chaque segment

# Use a pipeline as a high-level helper
#from transformers import pipeline

#pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

# Load model directly
#from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
#model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-fr")

#code mandeha
#from transformers import pipeline

#pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

#result = pipe("Hello, how are you?")
#print(result[0]['translation_text'])  # => "Bonjour, comment ça va ?"
#nouveaux code complete


# --- Paramètres ---


import json
import os
from transformers import pipeline

# Fichiers
INPUT_FILE = "segments.json"
OUTPUT_FILE = "translated_segments.json"

# Initialiser le pipeline de traduction
try:
    translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
except Exception as e:
    print("❌ Erreur lors de l'initialisation du modèle :", str(e))
    exit(1)

# Lire le fichier d'entrée
if not os.path.exists(INPUT_FILE):
    print(f"❌ Fichier introuvable : {INPUT_FILE}")
    exit(1)

try:
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        sentences = data.get("sentences", [])
        if not isinstance(sentences, list):
            raise ValueError("Le champ 'sentences' doit être une liste.")
except Exception as e:
    print("❌ Erreur à la lecture du fichier :", str(e))
    exit(1)

# Traduction
translated_sentences = []
for i, sentence in enumerate(sentences):
    if not isinstance(sentence, str):
        print(f"⚠️ Phrase ignorée (non texte) à l'index {i}")
        translated_sentences.append("")
        continue
    try:
        result = translator(sentence)
        translated_sentences.append(result[0]['translation_text'])
    except Exception as e:
        print(f"⚠️ Erreur de traduction à l'index {i} : {str(e)}")
        translated_sentences.append("")

# Écriture du résultat
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"translations": translated_sentences}, f, ensure_ascii=False, indent=4)
    print(f"✅ Traduction terminée. Fichier : {OUTPUT_FILE}")
except Exception as e:
    print("❌ Erreur à l’écriture du fichier :", str(e))
