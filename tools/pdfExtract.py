#!/usr/bin/env python3
# coding: utf-8

"""

Verwendung:

 for i in ksk-?.pdf; do python pdfExtract.py $i;done


"""

import argparse
import os
from tika import parser
import sys 

class Client:
    def __init__(self):
        # Initialize the client, e.g., set up API keys, endpoints, etc.
        pass

    def generate(self, prompt, model, options):
        # Simulate a response from the language model
        # In a real implementation, this would involve making an API call
        return {
            'response': f"Simulated response for model {model} with prompt: {prompt}"
        }

# Funktion zum Extrahieren von Text aus einer PDF-Datei
def extract_text_from_pdf(pdf_path):
    try:
        parsed = parser.from_file(pdf_path)
        meta = parsed["metadata"]   
        print("meta: ", meta)
        #sys.exit()
        text = parsed["content"]
        return text.strip()
    except Exception as e:
        print(f"Fehler beim Lesen der PDF-Datei '{pdf_path}': {e}")
        exit(1)

# Funktion zum Entfernen leerer Zeilen aus einem Text
def remove_blank_lines(text):
    if text:
        non_blank_lines = [line for line in text.splitlines() if line.strip()]
        return "\n".join(non_blank_lines)
    else:
        return ""

# Funktion zum Zusammenfassen von Text mit dem angegebenen Modell und der Sprache
def summarize_text(client, model, summary_prompt):
    try:
        response = client.generate(
            prompt=summary_prompt, model=model, options={'temperature': 0}
        )
        return remove_blank_lines(response['response'])
    except Exception as e:
        print(f"Fehler bei der Zusammenfassung des Textes: {e}")
        exit(1)


# Funktion zum Extrahieren des Inhaltsverzeichnisses aus dem PDF-Text
def isTocLine(line):
    return line.strip() and line[0].isalpha() and line[1].isdigit() and line[2] == '.' and line[3].isdigit()
def isTocHdr(line):
    return line.strip() and line[0].isalpha() and line[1].isdigit() and line[2] != '.'


def extract_table_of_contents(text):
    try:
        # Suche nach dem Inhaltsverzeichnis
        textLines = text.splitlines()
        inToc = False
        toc_lines = []
        toc_items = []
        txt_lines = []
        for i, line in enumerate(textLines):
            #if line.lower().startswith("inhaltsverzeichnis"):
            if line.lower().startswith("handlungsfeld "):
                inToc = True
                continue
            elif not inToc or not line.strip():
                continue

            # Suche nach den Einträgen im Inhaltsverzeichnis
            if isTocLine(line):
                l = line.strip()
                item = l.split(" ")[0]
                print("append line: ", l,item)
                toc_lines.append(l)
                toc_items.append(item)
            elif len(toc_lines) == 0:
                print("skip in toc: ", line)
                continue
            elif isTocHdr(line):
                print("hdr ", line)
                continue
            else:
                l = line.replace("","").strip()
                print("text line: ", l)
                try:
                    page_number = int(l)
                    continue
                except ValueError:
                    pass
                txt_lines.append(l)
                continue

        print("toc_items: ", toc_items)
        return (toc_items,txt_lines)
    except Exception as e:
        print(f"Fehler beim Extrahieren des Inhaltsverzeichnisses: {e}")
        return None

# Kommandozeilenargumente für PDF-Pfad, Modell, Sprache, Temperatur, Kontextfenster und verbose
arg_parser = argparse.ArgumentParser(
    description="Interagiere mit einer PDF-Datei mittels eines lokalen Sprachmodells"
)
arg_parser.add_argument("pdf_path", type=str, help="Pfad zur PDF-Datei.")
arg_parser.add_argument("--model", type=str, default="llama3.2",
                    help="Das zu verwendende Sprachmodell (Standard: llama3.2)")
arg_parser.add_argument("--language", type=str, default="deutsch",
                    help="Die Sprache für Antworten und Zusammenfassung (Standard: deutsch)")
arg_parser.add_argument("--temperature", type=float, default=0.8,
                    help="Die Temperatur für Modellantworten (Standard: 0.8)")
arg_parser.add_argument("--context_window", type=int, default=120000,
                    help="Maximale Anzahl von Zeichen aus dem PDF-Inhalt (Standard: 120000)")
arg_parser.add_argument("--summary_prompt", type=str, default=None,
                    help="Der Prompt, der für die Zusammenfassung verwendet wird.")
arg_parser.add_argument("--system_prompt", type=str, default=None,
                    help="Der System-Prompt für die Unterhaltung (Standardwert wird verwendet, falls nicht angegeben).")
arg_parser.add_argument("-v", "--verbose", action="store_true",
                    help="Aktiviere ausführliche Ausgabe für Debugging")
args = arg_parser.parse_args()

pdf_name = os.path.basename(args.pdf_path)

# Text aus der PDF extrahieren
pdf_text = extract_text_from_pdf(args.pdf_path)

toc, text = extract_table_of_contents(pdf_text)

# Inhaltsverzeichnis dem Benutzer anzeigen
if toc:
    print(f"Inhaltsverzeichnis:\n{toc}\n")
else:
    print("Kein Inhaltsverzeichnis gefunden oder Fehler beim Extrahieren.")

if text:
    print(f"Text:\n{'\n'.join(text)}\n")

def writeSegment(seg,id):
    print("write segment: ", id)
    with open(os.sep.join(["ksk_extracted",f"{id}_extracted.txt"]), "w") as f:
        f.write("\n".join(seg))

m = None
segment = []
for t in text:
    if t.lower().startswith("maßnahme ") and t.split(" ")[1] in toc:
        id = t.split(" ")[1] 
        if id != m:
            print("found: ", id)
            if m != None:
                # write
                writeSegment(segment,m)
            segment = []
            m = id 
    segment.append(t)    
# last
writeSegment(segment,m)

sys.exit()



# Inhalt kürzen, falls er das Kontextfenster überschreitet
if len(pdf_text) > args.context_window:
    pdf_text = pdf_text[:args.context_window]
    print("Der Inhalt der PDF-Datei wurde gekürzt, um in das Kontextfenster "
          "des Modells zu passen.")
elif args.verbose:
    print(f"Der gesamte Text passt in das Kontextfenster ({len(pdf_text)} Zeichen).")

# Ollama-Client initialisieren
if False:
    try:
        client = ollama.Client()
    except Exception as e:
        print(f"Fehler beim Initialisieren des Ollama-Clients: {e}")
        exit(1)
else:
    client = Client()

# Zusammenfassungsprompt vorbereiten
if args.summary_prompt:
    try:
        summary_prompt = args.summary_prompt.format(language=args.language, text=pdf_text)
    except KeyError as e:
        print(f"Fehler: Platzhalter {e} in summary_prompt nicht gefunden.")
        exit(1)
else:
    summary_prompt = (
        f"Summarize the following text in {args.language}. "
        f"Two paragraphs will be enough:\n\n{pdf_text}\n\nSummary:"
    )

# PDF-Text zusammenfassen
if args.verbose:
    print("Fasse den Text zusammen...")
pdf_summary = summarize_text(client, args.model, summary_prompt)

# Zusammenfassung dem Benutzer anzeigen
print(f"{pdf_summary}\n")

# System-Prompt vorbereiten
if args.system_prompt:
    try:
        conversation_history = args.system_prompt.format(text=pdf_text)
    except KeyError as e:
        print(f"Fehler: Platzhalter {e} in system_prompt nicht gefunden.")
        exit(1)
else:
    conversation_history = (
        f"You are a helpful assistant and inform the user about the following document:\n\n"
        f"{pdf_text}\n\nNow take the user's question."
    )
if args.verbose:
    print("Konversationsverlauf initialisiert.")


