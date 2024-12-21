import os
import sys
import re
import nltk
from ragInstrumentation import measure_execution_time

DEBUG = False

class PreProcessor():
    def __init__(self,lang="german"):
        nltk.download('punkt_tab')
        #nltk.download('words')
        if lang not in ["german","english"]:
            raise ValueError("Invalid language")
        self.lang = lang

    @measure_execution_time
    def clean(self, text):
        # Remove special characters
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces, tabs, and newlines with a single space
        text = re.sub(r'\.{2,}', '.', text)  # Replace multiple periods with a single period
        text = text.strip()  # Remove leading and trailing whitespace
        # tokenize the text into sentences
        sents_raw = nltk.sent_tokenize(text,language=self.lang)
        sents = []
        wordcount = 0
        for s in sents_raw:
            words = nltk.wordpunct_tokenize(s)
            wordcount += len(words)
            sents.append(" ".join(words).strip())
        # merge the sentences back into a single text            
        # return merged text, wordcount, sentences
        return "".join(sents), wordcount, sents


    @measure_execution_time
    def chunk(self, text, size=200):
        """
        Split the text into smaller chunks of a fixed size with an overlap.
        
        Args:
            text (str): The text to split.
            chunk_size (int): The size of each chunk (in tokens, not characters).
        Returns:
            list: A list of text chunks.
        """
        if DEBUG: print(f"Chunking text: {text}")
        ctext , wc, sents = self.clean(text)
        if wc <= size:
            return [ctext]
        else:
            chunks = []
            idx = 0
            chunk = ""
            while idx < len(sents):
                if DEBUG: print(f"idx: {idx}, chunk: {chunk}")
                chunk = f"{chunk}.{sents[idx]}".strip()
                if len(chunk.split()) >= size:
                    if DEBUG: print(f"Chunk: {chunk},{idx}")
                    chunks.append(chunk)
                    chunk =  ""
                    # no idx incremtent here. overlapping chunks
                else:
                    idx += 1
            return chunks


