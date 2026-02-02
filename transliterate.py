class Transliterator:
    def __init__(self):
        # Cyrillic to Latin mapping
        self.cyr_to_lat_map = {
            "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
            "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
            "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
            "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "ъ": "'", "ь": "",
            "э": "e", "ю": "yu", "я": "ya", "ў": "o'", "қ": "q", "ғ": "g'", "ҳ": "h",
            "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Е": "E", "Ё": "Yo",
            "Ж": "J", "З": "Z", "И": "I", "Й": "Y", "К": "K", "Л": "L", "М": "M",
            "Н": "N", "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T", "У": "U",
            "Ф": "F", "Х": "X", "Ц": "Ts", "Ч": "Ch", "Ш": "Sh", "Ъ": "'", "Ь": "",
            "Э": "E", "Ю": "Yu", "Я": "Ya", "Ў": "O'", "Қ": "Q", "Ғ": "G'", "Ҳ": "H"
        }

        # Latin to Cyrillic mapping
        # Order matters! Compound letters first.
        self.lat_to_cyr_map = [
            ("yo'q", "йўқ"), ("Yo'q", "Йўқ"), 
            ("o'", "ў"), ("g'", "ғ"), ("sh", "ш"), ("ch", "ч"), ("ng", "нг"),
            ("O'", "Ў"), ("G'", "Ғ"), ("Sh", "Ш"), ("Ch", "Ч"), ("Ng", "Нг"), 
            # Handle different apostrophes for o' and g'
            ("o‘", "ў"), ("g‘", "ғ"), ("O‘", "Ў"), ("G‘", "Ғ"),
            ("o’", "ў"), ("g’", "ғ"), ("O’", "Ў"), ("G’", "Ғ"),
            ("o`", "ў"), ("g`", "ғ"), ("O`", "Ў"), ("G`", "Ғ"),
            ("SH", "Ш"), ("CH", "Ч"), ("NG", "НГ"),
            ("yo", "ё"), ("yu", "ю"), ("ya", "я"), ("ye", "е"),
            ("Yo", "Ё"), ("Yu", "Ю"), ("Ya", "Я"), ("Ye", "Е"),
            ("YO", "Ё"), ("YU", "Ю"), ("YA", "Я"), ("YE", "Е"),
            ("ts", "ц"), ("Ts", "Ц"), ("TS", "Ц"),
            # Single characters
            ("a", "а"), ("b", "б"), ("d", "д"), ("e", "э"), ("f", "ф"),
            ("g", "г"), ("h", "ҳ"), ("i", "и"), ("j", "ж"), ("k", "к"),
            ("l", "л"), ("m", "м"), ("n", "н"), ("o", "о"), ("p", "п"),
            ("q", "қ"), ("r", "р"), ("s", "с"), ("t", "т"), ("u", "у"),
            ("v", "в",), ("x", "х"), ("y", "й"), ("z", "з"), 
            ("'", "ъ"), ("‘", "ъ"), ("’", "ъ"), ("`", "ъ"), # Handle all apostrophes as ъ
            ("A", "А"), ("B", "Б"), ("D", "Д"), ("E", "Э"), ("F", "Ф"),
            ("G", "Г"), ("H", "Ҳ"), ("I", "И"), ("J", "Ж"), ("K", "К"),
            ("L", "Л"), ("M", "М"), ("N", "Н"), ("O", "О"), ("P", "П"),
            ("Q", "Қ"), ("R", "Р"), ("S", "С"), ("T", "Т"), ("U", "У"),
            ("V", "В"), ("X", "Х"), ("Y", "Й"), ("Z", "З")
        ]

    def to_latin(self, text):
        result = ""
        i = 0
        while i < len(text):
            # Special handling for 'Е', 'е'
            # If start of word or after vowel -> 'Ye'/'ye'
            # If after consonant -> 'E'/'e'
            char = text[i]
            if char in ['Е', 'е']:
                is_start_or_vowel = (i == 0) or (text[i-1] in "аоуиэюяёеўАОУИЭЮЯЁЕЎ \n\t\r.,!?:;()")
                if is_start_or_vowel:
                    if char == 'Е': result += 'Ye'
                    else: result += 'ye'
                else:
                    if char == 'Е': result += 'E'
                    else: result += 'e'
                i += 1
                continue
            
            # Special handling for 'Ц', 'ц'
            # Start of word? -> 'S' (usually), but modern loanwords keep Ts. We'll stick to strict transliteration 'Ts' for now as requested by user logic "Kril-Lotin".
            # Standard Uzbek mapping often converts initial Ц to S (e.g. Tsirk -> Sirk), but technical converter should probably be reversible or strict. 
            # Let's simple use the dict mapping which is 'ts'.
            
            if char in self.cyr_to_lat_map:
                result += self.cyr_to_lat_map[char]
            else:
                result += char
            i += 1
        return result

    def to_cyrillic(self, text):
        # We need to handle compound sounds first.
        # Since we are iterating, simply replacing strings might be dangerous if order is wrong.
        # But for 'replace' method, it does global replacement. 
        # Better approach: Iterate and look ahead. OR use replace with carefully sorted list.
        # The list self.lat_to_cyr_map is sorted by length (descending) effectively if we put compounds first.
        
        # However, simple .replace() cascades can be wrong (e.g. replacing 's' then 'h' separately instead of 'sh').
        # So we must iterate through the priorities.
        
        # Special logic for 'E'/'e' (E -> Э at start, E -> Е inside).
        # This is context dependent, so simple replace won't work perfectly for 'E'.
        # Let's do a token-based or character-walking approach.
        
        # Actually, standard 'replace' for 'sh', 'ch' etc is fine. 
        # The problem is 'E'. 
        # In Latin Uzbek: 'E' at start is 'Э', 'E' inside is 'Е'. 
        # BUT 'Ye' is always 'Е'.
        
        w_text = text
        
        # First handle standard compounds
        compounds = [
            ("yo'q", "йўқ"), ("Yo'q", "Йўқ"), 
            ("o'", "ў"), ("g'", "ғ"), ("sh", "ш"), ("ch", "ч"),
            ("O'", "Ў"), ("G'", "Ғ"), ("Sh", "Ш"), ("Ch", "Ч"),
            # New variants
            ("o‘", "ў"), ("g‘", "ғ"), ("O‘", "Ў"), ("G‘", "Ғ"),
            ("o’", "ў"), ("g’", "ғ"), ("O’", "Ў"), ("G’", "Ғ"),
            ("o`", "ў"), ("g`", "ғ"), ("O`", "Ў"), ("G`", "Ғ"),
            ("SH", "Ш"), ("CH", "Ч"),
            ("yo", "ё"), ("yu", "ю"), ("ya", "я"), ("ye", "е"),
            ("Yo", "Ё"), ("Yu", "Ю"), ("Ya", "Я"), ("Ye", "Е"),
            ("YO", "Ё"), ("YU", "Ю"), ("YA", "Я"), ("YE", "Е"),
            ("ts", "ц"), ("Ts", "Ц"), ("TS", "Ц")
        ]
        
        # We use a placeholder approach to prevent double replacement? 
        # No, 'sh' to 'ш' is safe. 'ш' won't be matched by other latin tokens.
        
        for lat, cyr in compounds:
            w_text = w_text.replace(lat, cyr)
            
        # Now single chars. 
        # 'e' is special. 
        # We need to distinguish 'e' -> 'э' (start of word) vs 'e' -> 'е' (elsewhere).
        # Since we already replaced 'ye' -> 'е', valid 'e's remaining are likely 'э' or 'е'.
        # Rule: 'e' at beginning of word -> 'э'. 'e' after vowel -> 'э' (poema -> поэма)? No, poema -> поэма (cyrillic). 
        # Actually in Uzbek latin: 'e' is used for 'э'. 'ye' is used for 'е'.
        # e.g. 'ekran' -> 'экран'. 'bel' -> 'бел'.
        # So 'e' -> 'э' if start of word, else 'e' -> 'е'.
        
        # Let's use a regex or per-character rebuild for 'e'.
        
        result_chars = []
        length = len(w_text)
        i = 0
        while i < length:
            char = w_text[i]
            
            if char == 'e' or char == 'E':
                # Check if start of word
                is_start = (i == 0) or (w_text[i-1] in " \n\t\r.,!?:;()\"'-")
                if is_start:
                    result_chars.append('Э' if char == 'E' else 'э')
                else:
                    result_chars.append('Е' if char == 'E' else 'е')
            elif char == "'":
                # modifier only if not consumed by o' or g' (which are already handled)
                # single ' is ъ
                result_chars.append('ъ')
            else:
                # Basic mapping
                found = False
                for lat, cyr in [
                    ("a", "а"), ("b", "б"), ("d", "д"), ("f", "ф"),
                    ("g", "г"), ("h", "ҳ"), ("i", "и"), ("j", "ж"), ("k", "к"),
                    ("l", "л"), ("m", "м"), ("n", "н"), ("o", "о"), ("p", "п"),
                    ("q", "қ"), ("r", "р"), ("s", "с"), ("t", "т"), ("u", "у"),
                    ("v", "в"), ("x", "х"), ("y", "й"), ("z", "з"),
                    ("A", "А"), ("B", "Б"), ("D", "Д"), ("F", "Ф"),
                    ("G", "Г"), ("H", "Ҳ"), ("I", "И"), ("J", "Ж"), ("K", "К"),
                    ("L", "Л"), ("M", "М"), ("N", "Н"), ("O", "О"), ("P", "П"),
                    ("Q", "Қ"), ("R", "Р"), ("S", "С"), ("T", "Т"), ("U", "У"),
                    ("V", "В"), ("X", "Х"), ("Y", "Й"), ("Z", "З")
                ]:
                    if char == lat:
                        result_chars.append(cyr)
                        found = True
                        break
                if not found:
                    result_chars.append(char)
            i += 1
            
        return "".join(result_chars)

if __name__ == "__main__":
    t = Transliterator()
    print(t.to_latin("Ассалому алайкум"))
    print(t.to_cyrillic("Assalomu alaykum"))
    print(t.to_latin("Ўзбекистон"))
    print(t.to_cyrillic("O'zbekiston"))
