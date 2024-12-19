import os
import sys
import re
import nltk

debug = False

class PreProcessor():
    def __init__(self,lang="german"):
        nltk.download('punkt_tab')
        #nltk.download('words')
        if lang not in ["german","english"]:
            raise ValueError("Invalid language")
        self.lang = lang

    def clean(self, text):
        sents_raw = nltk.sent_tokenize(text,language=self.lang)
        sents = []
        wordcount = 0
        for s in sents_raw:
            words = nltk.wordpunct_tokenize(s)
            wordcount += len(words)
            sents.append(" ".join(words).strip())
            
        text_cleaned = ".".join(sents)
        return text_cleaned


    def chunk(self, text, size=200, overlap=30):
        """
        Split the text into smaller chunks of a fixed size with an overlap.
        
        Args:
            text (str): The text to split.
            chunk_size (int): The size of each chunk (in tokens, not characters).
            overlap (int): The number of tokens to overlap between chunks.
        
        Returns:
            list: A list of text chunks.
        """
        overlap = size // 2 if overlap >= size else overlap
        words = text.split()  # Split text into words
        chunks = []
        for i in range(0, len(words), size - overlap):
            chunk = ' '.join(words[i:i + size])
            chunks.append(chunk)
        return chunks


