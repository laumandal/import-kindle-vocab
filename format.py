def highlight_lookup_word(quote, word, stem, tag='<b>'):
    """Highlight the study word with an html tag"""
    if not (tag[:1]=='<' and tag[-1:]=='>'):
        raise ValueError(f"tag should be an html tag, eg <b>")
    close_tag = tag[:1]+'/'+tag[1:]

    if word in quote:
        # if word in quote, highlight directly
        quote = quote.replace(word, f"{tag}{word}{close_tag}")
    elif '・' in stem:
        # if ・ is present, highlight the stem before this
        tail_length = len(stem)-stem.find('・')-1
        word_stem = word[:-tail_length]
        quote = quote.replace(word_stem, f"{tag}{word_stem}{close_tag}")
    else:
        # just add the study word after the quote
        quote += f"(study word: {tag}{word}{close_tag})"

    return quote
