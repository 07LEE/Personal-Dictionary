# Personal-Dictionary

Personal-Dictionary is a custom dictionary management package for the Kiwi morphological analyzer. It provides a simple interface to manage user-defined words, ensuring the integrity of technical terms and domain-specific jargon for NLP projects.

## Features

- **Single File Management:** Centralized management of custom words via `custom_dict.txt`.
- **Kiwi Integration:** Seamless integration with the Kiwi (`kiwipiepy`) morphological analyzer.
- **Easy Integration:** Designed to be easily integrated into larger search or NLP pipelines.

## Tech Stack

- **Language:** Python 3.8+
- **Core Engine:** `kiwipiepy` (Kiwi) - LGPLv3

## Installation

To integrate this dictionary with other projects, install it in editable mode:

```bash
git clone https://github.com/username/Personal-Dictionary.git
cd Personal-Dictionary
pip install -e .
```

## Usage

### 1. Dictionary Format

Edit `personal_dict/custom_dict.txt` with the following format:

```text
# Word [Tag] [Score]
# Default Tag: NNP (Proper Noun)
COLMAP NNP 1.0
3DGS NNP 1.0
Gaussian-Splatting NNG 1.0
```

### 2. Integration Example

```python
from personal_dict import DictionaryManager

# Initialize manager
dict_manager = DictionaryManager()

# Load custom dictionary
dict_manager.load_dict()

# Get the configured Kiwi instance
kiwi = dict_manager.get_kiwi()
tokens = kiwi.tokenize("3DGS and COLMAP algorithm analysis")
print([t.form for t in tokens])
```

## Directory Structure

- `personal_dict/`: Core package source code.
  - `custom_dict.txt`: The primary custom dictionary file.
  - `manager.py`: Dictionary loading logic.
- `setup.py`: Package installation and dependency management.
