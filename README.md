JMdictParser

**JMdictParser** is a script for parsing through JMdict data 
http://www.edrdg.org/jmdict/edict_doc.html for Japanese words that
are made up entirely of kanji and are of lengths greater than 1 character.
The script returns a Python dictionary containing readings, definitions, and 
JLPT data for each word and exports that dictionary to compound_dict.json.

Usage

**compound_dict.json** is already included along with a copy of the
JMdict_e file needed to build it.

Simply run the script in the same directory as
the JMdict file in order to build a new dictionary.

About the compound_dict dictionary

The current version of the dictionary contains 96390 entries,
all of which have relevant definitions, reading, and JLPT data.
Regarding usage, kanji words are keys that return sub-dictionaries
that use 'reading', 'meaning', 'jlpt' as keys to access the data.
 
License information

**JMdictParser.py** is free to use and modify. kanji_dict.json is
built using the script found at https://github.com/nramkissoon/Kanjidicparser
and utilizes data from the KANJIDIC project. JLPT data from the KANJIDIC projects is subject to conditions 
found at https://www.edrdg.org/edrdg/licence.html. JMdict data 
is subject to conditions found at http://www.edrdg.org/.

