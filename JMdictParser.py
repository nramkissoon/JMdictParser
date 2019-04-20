
""" This is a script for parsing the JMdict_e data that can be found at http://www.edrdg.org/jmdict/edict_doc.html.

This script parses through entries looking for words made entirely of kanji and builds a Python dictionary containing
readings, definitions, and JLPT levels for those words. The Python dictionary is then exported to a json file to be
used for other projects. JLPT data is obtained from the KANJIDIC project at
 http://www.edrdg.org/wiki/index.php/KANJIDIC_Project."""

import json
import re


def read_jmdict():
    """ Creates a line generator from the JMdict_e file"""

    try:
        f = open('JMdict_e', 'r')
        for line in f:
            yield line
    except FileNotFoundError:
        print("JMdict_e not found in directory")
        raise FileNotFoundError


def yield_entries():
    """ Groups together lines that belong to the same entry and creates a generator for entries"""

    entry = ""
    new_entry = False
    for line in read_jmdict():
        if line == "<entry>\n":
            new_entry = True
        if new_entry:
            entry += line
        if line == "</entry>\n":
            new_entry = False
            yield entry
            entry = ""


def kanji_check(character):
    """ Determines if the character parameter is a kanji character based on UTF-8 code"""

    if (ord(character) >= ord('\u4e00')) and (ord(character) <= ord('\u9faf')):
        return True
    else:
        return False


def trim_entries_for_kanjiwords():
    """ Parses for entries that are composed of only kanji and are of length > 1"""

    for entry in yield_entries():
        entry_name = re.search('<keb>(.*?)</keb>', entry)
        if not entry_name:
            pass
        else:
            entry_name = entry_name.group(1)
            kanji_word = True
            for char in entry_name:
                if not kanji_check(char):
                    kanji_word = False
            if kanji_word and len(entry_name) > 1:
                yield entry


def trim_data():
    """ Trims extraneous data and yields dictionaries for each entry"""

    for entry in trim_entries_for_kanjiwords():
        trimmed_entry = {}
        entry_name = re.search('<keb>(.*?)</keb>', entry).group(1)
        trimmed_entry[entry_name] = {}
        entry_reading = re.search('<reb>(.*?)</reb>', entry).group(1)
        trimmed_entry[entry_name]['reading'] = entry_reading
        entry_senses = re.findall(re.compile('<sense>(.*?)</sense>', re.DOTALL), entry)
        entry_glosses = re.findall('<gloss>(.*?)</gloss>', entry_senses[0])
        trimmed_entry[entry_name]['meaning'] = entry_glosses
        yield trimmed_entry


def fill_in_jlpt(compound_dict):
    """ Fills in JLPT levels using KANJIDIC data"""

    try:
        f = open("kanji_dict.json", 'rb')
        kanji_dict = json.load(f)
        f.close()
    except FileNotFoundError:
        print("kanji_dict.json not found, cannot get jlpt data")
        raise FileNotFoundError
    for i in compound_dict:
        jlpt_list = []
        for j in i:  # gets jlpt for each kanji in the compound and puts them in a list
            try:
                jlpt_list.append(kanji_dict[j]["jlpt"][0])
            except IndexError:
                compound_dict[i]["jlpt"] = jlpt_list
        jlpt_final = []
        for jlpt in jlpt_list:
            if jlpt == ' ':
                jlpt_final.append('not listed in JLPT')
            else:
                jlpt_final.append(jlpt)
        compound_dict[i]["jlpt"] = jlpt_final
    return compound_dict


def build_compounddict():
    """ Creates a python dictionary from the generator produced from trim_data() and fills in JLPT data"""

    compound_dict = {}
    for entry in trim_data():
        compound_dict.update(entry)
    # Entries that need to be manually filled in due to errors in the JMdict data
    compound_dict['新平民']['meaning'] = ['name given to the lowest rank of the '
                                       'Japanese caste system after its abolition​'
                                       ]
    compound_dict['春塵']['meaning'] = ["spring dust",
                                      "frost and snow that's blown like dust in the air by the spring wind​"]
    compound_dict['雲白肉']['meaning'] = ['dish of spicy boiled pork', 'usu. served with slices of cucumber']
    compound_dict['神幸']['meaning'] = ['transferring a shintai in a portable shrine']
    return fill_in_jlpt(compound_dict)


def export_to_json(compound_dict):
    """ Exports dictionary to json file"""

    f = open("compound_dict.json", 'w')
    json.dump(compound_dict, f)
    f.close()


# Script for creating a new compound dictionary
a = input("Create new compound_dict.json? [y/n]: ")
while (a != 'y') and (a != 'n'):
    print("Invalid Input...")
    a = input("Create new compound_dict.json? [y/n]: ")

if a == 'y':
    print("Creating compound_dict.json...")
    comp = build_compounddict()
    export_to_json(comp)
    print("Compound dictionary created and exported to compound_dict.json")
    print("Compound dictionary contains " + str(len(comp)) + " entries.")
else:
    print("Exiting JMdictParser.py...")
