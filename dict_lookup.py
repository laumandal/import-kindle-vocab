#%%
import CoreServices.DictionaryServices as ds
import re
import pandas as pd


def lookup(word):
    """
    Look up a word in the OSX dictionary and return the definition.
    Reference function here: 
    https://developer.apple.com/documentation/coreservices/1446842-dcscopytextdefinition?preferredLanguage=occ
    """
    defn = ds.DCSCopyTextDefinition(None, word, (0, len(word)))
    return defn


def filter_defn(defn):
    """Filter the relevant parts from the results of the query."""
    if defn == None:
        return ""

    # remove unneccesary parts of the definition
    strip_defn = re.compile(
        r"""
        ^
        (.+?)\s                        # reading of the looked up word (capture)
        (?:[\u3040-\u309f―]+?\s)?      # hiragana, pronunciation related (?)
        [0-9]*(?:【.+?】)?              # kanji
        (?:\（.+?\）)?                  # type of word
        (?:[\u30a0-\u30ff\u4e00-\u9fbf]+?\s)?  # kanji/katakana of type
        (?:《.+?》)?(?:〔.+?〕)?        # potential further explanations
        (.+?)                          # definition (capture)
        (?:〔.+?〕)?                    # potential additional info we don't need
        (?:〈子項目〉.+)?                # potential items related to lookup 
        (?:〈親項目〉.+)?                # potential items related to lookup 
        (?:〈句項目〉.+)?                # potential items related to lookup 
        (?:派生.+)?                     # derivation info
        $
        """,
        re.VERBOSE,
    )
    defn_reading, defn_meaning = re.search(strip_defn, defn).group(1, 2)

    # remove usage examples from the definition string
    remove_examples = re.compile(
        r"""
        「[^「]*?―[^「]*?」     # quote (will contain '―'to show where to use the word)
        (?:〈.+?〉)?           # potential quote source
        """,
        re.VERBOSE,
    )
    defn_meaning = re.sub(remove_examples, "", defn_meaning)

    # replace punctuation in the reading string
    defn_reading = defn_reading.replace("・", "")

    return f"{defn_reading}: {defn_meaning}"


def lookup_and_filter(word):
    """return the filtered result of dictionary lookup"""
    defn = lookup(word)
    defn_filtered = filter_defn(defn)

    return defn_filtered

