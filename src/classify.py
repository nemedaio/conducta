import os
import glob
import json
import re
from datetime import datetime
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Config
TRANSCRIPT_DIR = "obsidian_vault/transcripts"
CLASSIFIED_DIR = "obsidian_vault/classified"
METADATA_FILE = "data/metadata.json"

# High-level Psychological Ontology
ONTOLOGY = {
    "Conductismo": ["conducta", "refuerzo", "castigo", "skinner", "pavlov", "condicionamiento", "estímulo", "respuesta"],
    "Psicología Cognitiva": ["memoria", "atención", "pensamiento", "mente", "procesamiento", "cognitivo"],
    "Psicoanálisis": ["inconsciente", "freud", "pulsión", "ego", "superyó", "psicoanálisis", "sueño"],
    "Psicología de la Salud / Clínica": ["trastorno", "síntoma", "terapia", "clínica", "salud mental", "ansiedad", "depresión"],
    "Neuropsicología": ["cerebro", "neuronas", "neurotransmisores", "neuro", "córtex", "lóbulo"],
    "Psicología del Desarrollo": ["niñez", "desarrollo", "infancia", "aprendizaje", "etapas", "piaget"],
    "Epistemología y Ciencia": ["ciencia", "método scientifico", "epistemología", "investigación", "teoría"]
}

def clean_transcript(text):
    """Remove timestamp headers for NLP processing."""
    return re.sub(r'\[\d+\.\d+s\] ', '', text)

def get_summary(text, count=3, language="spanish"):
    """Generate a simple extractive summary."""
    try:
        parser = PlaintextParser.from_string(text, Tokenizer(language))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, count)
        return " ".join([str(sentence) for sentence in summary])
    except:
        return text[:300] + "..."

def classify_text(text):
    """Identify topics based on the ontology."""
    text_lower = text.lower()
    found_topics = []
    for topic, keywords in ONTOLOGY.items():
        if any(kw in text_lower for kw in keywords):
            found_topics.append(topic)
    return found_topics if found_topics else ["General"]

def run_classification():
    os.makedirs(CLASSIFIED_DIR, exist_ok=True)
    
    # Load metadata if exists
    metadata = {}
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            metadata = json.load(f)

    files = glob.glob(os.path.join(TRANSCRIPT_DIR, "*.md"))
    print(f"Processing {len(files)} files for classification...")

    # Index by topic for the ontology view
    ontology_index = {topic: [] for topic in ONTOLOGY.keys()}
    ontology_index["General"] = []

    for file_path in files:
        vid_id = os.path.basename(file_path).replace(".md", "")
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        cleaned_text = clean_transcript(raw_content)
        topics = classify_text(cleaned_text)
        summary = get_summary(cleaned_text)
        
        vid_meta = metadata.get(vid_id, {})
        title = vid_meta.get("title", f"Video {vid_id}")
        date_str = vid_meta.get("upload_date", "Unknown Date")
        if date_str != "Unknown Date" and len(date_str) == 8:
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

        # Create Obsidian frontmatter
        md_classification = f"""---
id: {vid_id}
title: "{title}"
date: {date_str}
topics: {json.dumps(topics, ensure_ascii=False)}
---
# Summary
{summary}

# Original Transcript
[[{vid_id}]]
"""
        
        # Save to obsidian_vault/classified
        out_path = os.path.join(CLASSIFIED_DIR, f"Classified_{vid_id}.md")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(md_classification)
            
        for t in topics:
            ontology_index[t].append({
                "id": vid_id,
                "title": title,
                "date": date_str
            })

    # Create ONTOLOGY.md overall view
    ontology_md = "# Psychology Ontology - Channel Overview\n\n"
    for topic, videos in ontology_index.items():
        if videos:
            ontology_md += f"## {topic}\n"
            # Sort by date
            videos.sort(key=lambda x: x['date'], reverse=True)
            for v in videos:
                ontology_md += f"- [[Classified_{v['id']}]] | {v['date']} | {v['title']}\n"
            ontology_md += "\n"

    with open(os.path.join("obsidian_vault", "ONTOLOGY.md"), 'w', encoding='utf-8') as f:
        f.write(ontology_md)

    print("Classification and Ontology creation complete!")

if __name__ == "__main__":
    run_classification()
