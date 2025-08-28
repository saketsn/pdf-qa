import os
from symspellpy.symspellpy import SymSpell

DICT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "frequency_dictionary_en_82_765.txt")

_symspell = None

def load_symspell(max_edit_distance=2, prefix_length=7):
    global _symspell
    if _symspell is None:
        _symspell = SymSpell(max_dictionary_edit_distance=max_edit_distance, prefix_length=prefix_length)
        if os.path.exists(DICT_PATH):
            _symspell.load_dictionary(DICT_PATH, term_index=0, count_index=1)
    return _symspell

def spell_correct(text: str) -> str:
    s = load_symspell()
    if s is None:
        return text
    suggestions = s.lookup_compound(text, max_edit_distance=2)
    if suggestions:
        return suggestions[0].term
    return text
