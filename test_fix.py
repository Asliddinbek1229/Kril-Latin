from transliterate import Transliterator

t = Transliterator()
test_words = [
    "ro'yobga", 
    "ro‘yobga", 
    "ro’yobga", 
    "ro`yobga",
    "o‘zbek",
    "O‘zbek",
    "g‘oz",
]

print("Testing Apostrophe variants:")
for word in test_words:
    cyrillic = t.to_cyrillic(word)
    print(f"{word} -> {cyrillic}")

expected = {
    "ro'yobga": "рўёбга",
    "ro‘yobga": "рўёбга",
    "ro’yobga": "рўёбга",
    "ro`yobga": "рўёбга",
    "o‘zbek": "ўзбек",
    "O‘zbek": "Ўзбек",
    "g‘oz": "ғоз"
}

all_passed = True
for word, exp in expected.items():
    res = t.to_cyrillic(word)
    if res != exp:
        print(f"FAILED: {word} -> {res} (Expected: {exp})")
        all_passed = False

if all_passed:
    print("\nALL TESTS PASSED!")
else:
    print("\nSOME TESTS FAILED.")
