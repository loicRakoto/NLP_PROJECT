import json
import os
from transformers import pipeline
from langdetect import detect

# Configuration des fichiers
INPUT_FILE = os.path.join("data", "segments.json")
OUTPUT_FILE = os.path.join("data", "translated_segments.json")

def detect_language(text):
    """Détecte la langue du texte"""
    try:
        detected = detect(text)
        return detected if detected in ['fr', 'en'] else 'en'
    except:
        # Fallback simple si la détection échoue
        french_indicators = ['le', 'la', 'les', 'de', 'du', 'et', 'est', 'dans', 'pour', 'avec']
        words = text.lower().split()[:5]
        if any(word in french_indicators for word in words):
            return 'fr'
        return 'en'


def load_translator(direction):
    """Charge le modèle de traduction"""
    models = {
        "fr-en": "Helsinki-NLP/opus-mt-fr-en",
        "en-fr": "Helsinki-NLP/opus-mt-en-fr"
    }
    try:
        return pipeline("translation", model=models[direction])
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle {direction}: {e}")
        return None


def translate_text(text, translator):
    """Traduit un texte"""
    try:
        result = translator(text)
        return result[0]['translation_text']
    except Exception as e:
        print(f"⚠️ Erreur de traduction: {e}")
        return text  # Retourne le texte original en cas d'erreur


def main():
    print("🚀 Traducteur automatique français ⇄ anglais")
    print("=" * 50)

    # Vérifier l'existence du fichier d'entrée
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Fichier introuvable: {INPUT_FILE}")
        return

    # Lire le fichier d'entrée
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            sentences = data.get("sentences", [])
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return

    if not sentences:
        print("⚠️ Aucune phrase trouvée")
        return

    print(f"📝 {len(sentences)} phrases à traduire...")

    # Variables pour les traducteurs (chargement à la demande)
    fr_to_en = None
    en_to_fr = None
    translations = []

    # Traduire chaque phrase
    for i, sentence in enumerate(sentences):
        if not isinstance(sentence, str) or not sentence.strip():
            translations.append("")
            continue

        # Détecter la langue
        lang = detect_language(sentence)

        # Charger le bon traducteur si nécessaire
        if lang == 'fr':
            if fr_to_en is None:
                print("🔄 Chargement modèle français → anglais...")
                fr_to_en = load_translator("fr-en")
            translator = fr_to_en
            direction = "🇫🇷→🇬🇧"
        else:
            if en_to_fr is None:
                print("🔄 Chargement modèle anglais → français...")
                en_to_fr = load_translator("en-fr")
            translator = en_to_fr
            direction = "🇬🇧→🇫🇷"

        if translator is None:
            translations.append("")
            continue

        # Traduire
        translation = translate_text(sentence, translator)
        translations.append(translation)

        # Afficher progression
        if i < 3 or (i + 1) % 10 == 0:
            print(f"{direction} [{i + 1:3d}] {sentence[:30]}... → {translation[:30]}...")

    # Sauvegarder le résultat
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump({"translations": translations}, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Traduction terminée!")
        print(f"📁 Résultat: {OUTPUT_FILE}")
        print(f"📊 {len([t for t in translations if t])} traductions réussies")
    except Exception as e:
        print(f"❌ Erreur écriture: {e}")


if __name__ == "__main__":
    main()