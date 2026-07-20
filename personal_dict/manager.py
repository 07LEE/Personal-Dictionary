import json
import logging
from pathlib import Path
from kiwipiepy import Kiwi

logger = logging.getLogger(__name__)

class DictionaryManager:
    """
    Manages a single custom dictionary file to fix morphological analysis failures.
    """
    def __init__(self, kiwi_instance=None):
        self.kiwi = kiwi_instance or Kiwi()
        # Default path to the single custom dictionary (now in the same folder)
        base_dir = Path(__file__).resolve().parent
        self.dict_path = base_dir / "custom_dict.txt"
        self.synonyms_path = base_dir / "synonyms.json"
        self.synonyms = {}

    def load_dict(self):
        """Loads words from custom_dict.txt into the Kiwi dictionary."""
        if not self.dict_path.exists():
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
                    logger.error("Failed to add word '%s': %s", word, e)
        
        logger.info("Loaded %d words from custom_dict.txt", count)
        self.load_synonyms()
        return True

    def load_synonyms(self):
        """Loads synonyms from synonyms.json into memory."""
        if not self.synonyms_path.exists():
            self.synonyms = {}
            return False
            
        try:
            with open(self.synonyms_path, 'r', encoding='utf-8') as f:
                self.synonyms = json.load(f)
            logger.info("Loaded %d synonyms from synonyms.json", len(self.synonyms))
            return True
        except Exception as e:
            logger.error("Failed to load synonyms: %s", e)
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
