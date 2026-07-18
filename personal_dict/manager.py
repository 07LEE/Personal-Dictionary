import os
import json
import logging
from kiwipiepy import Kiwi

class DictionaryManager:
    """
    Manages a single custom dictionary file to fix morphological analysis failures.
    """
    def __init__(self, kiwi_instance=None):
        self.kiwi = kiwi_instance or Kiwi()
        # Default path to the single custom dictionary (now in the same folder)
        self.dict_path = os.path.join(os.path.dirname(__file__), "custom_dict.txt")
        self.synonyms_path = os.path.join(os.path.dirname(__file__), "synonyms.json")
        self.synonyms = {}

    def load_dict(self):
        """Loads words from custom_dict.txt into the Kiwi dictionary."""
        if not os.path.exists(self.dict_path):
            return False
            
        count = 0
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                word = parts[0]
                tag = parts[1] if len(parts) > 1 else 'NNP'
                score = float(parts[2]) if len(parts) > 2 else 1.0
                
                try:
                    self.kiwi.add_user_word(word, tag, score)
                    count += 1
                except Exception as e:
                    logging.error(f"Failed to add word '{word}': {e}")
        
        print(f"LOGE: [DictionaryManager] Loaded {count} words from custom_dict.txt")
        self.load_synonyms()
        return True

    def load_synonyms(self):
        """Loads synonyms from synonyms.json into memory."""
        if not os.path.exists(self.synonyms_path):
            self.synonyms = {}
            return False
            
        try:
            with open(self.synonyms_path, 'r', encoding='utf-8') as f:
                self.synonyms = json.load(f)
            print(f"LOGE: [DictionaryManager] Loaded {len(self.synonyms)} synonyms from synonyms.json")
            return True
        except Exception as e:
            logging.error(f"Failed to load synonyms: {e}")
            self.synonyms = {}
            return False

    def preprocess_query(self, query):
        """Preprocesses the query by replacing registered synonyms."""
        if not query:
            return query
            
        normalized = query
        for k, v in self.synonyms.items():
            normalized = normalized.replace(k, v)
        return normalized

    def get_kiwi(self):
        return self.kiwi
