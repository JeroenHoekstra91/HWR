# coding=utf-8
import re

char_map = {
    "Alef": 0,
    "Ayin": 1,
    "Bet": 2,
    "Dalet": 3,
    "Gimel": 4,
    "He": 5,
    "Het": 6,
    "Kaf": 7,
    "Kaf-final": 8,
    "Lamed": 9,
    "Mem": 10,
    "Mem-medial": 11,
    "Noise": 12,
    "Nun-final": 13,
    "Nun-medial": 14,
    "Pe": 15,
    "Pe-final": 16,
    "Qof": 17,
    "Resh": 18,
    "Samekh": 19,
    "Shin": 20,
    "Taw": 21,
    "Tet": 22,
    "Tsadi-final": 23,
    "Tsadi-medial": 24,
    "Waw": 25,
    "Yod": 26,
    "Zayin": 27,
}

hebrew_map = {
    "Alef": "א",
    "Ayin": "ע",
    "Bet": "ב",
    "Dalet": "ד",
    "Gimel": "ג",
    "He": "ה",
    "Het": "ח",
    "Kaf": "כ",
    "Kaf-final": "ך",
    "Lamed": "ל",
    "Mem": "ם",
    "Mem-medial": "מ",
    "Nun-final": "ן",
    "Nun-medial": "נ",
    "Pe": "פ",
    "Pe-final": "ף",
    "Qof": "ק",
    "Resh": "ר",
    "Samekh": "ס",
    "Shin": "ש",
    "Taw": "ת",
    "Tet": "ט",
    "Tsadi-final": "צ",
    "Tsadi-medial": "צ",
    "Waw": "ו",
    "Yod": "י",
    "Zayin": "ז",
    "": " ",
}

flat_map = {
    "Alef": "a",
    "Ayin": "b",
    "Bet": "c",
    "Dalet": "d",
    "Gimel": "e",
    "He": "f",
    "Het": "g",
    "Kaf": "h",
    "Kaf-final": "i",
    "Lamed": "j",
    "Mem": "k",
    "Mem-medial": "l",
    "Nun-final": "m",
    "Nun-medial": "n",
    "Pe": "o",
    "Pe-final": "p",
    "Qof": "q",
    "Resh": "r",
    "Samekh": "s",
    "Shin": "t",
    "Taw": "u",
    "Tet": "v",
    "Tsadi-final": "w",
    "Tsadi-medial": "x",
    "Waw": "y",
    "Yod": "z",
    "Zayin": "0",
    "": "1"
}

def to_hebrew(word):
    hebrew = ""
    for character in word.split(" "):
        hebrew += hebrew_map[character]
    return hebrew

def to_flat(word):
    flat = ""
    for character in word.split(" "):
        flat += flat_map[character]
    return flat

def hebrew_to_phonetic(word):
    phonetics = ""
    for character in re.findall(r"\xd7.", word):
        phonetics += hebrew_map.keys()[
            hebrew_map.values().index(character)
        ] + " "
    return phonetics.strip()