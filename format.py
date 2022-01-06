def highlight_lookup_word(quote, word, stem, tag='<b>'):
    tag = '<b>'
    if not (tag[:1]=='<' and tag[-1:]=='>'):
        raise ValueError(f"tag should be an html tag, eg <b>")
    close_tag = tag[:1]+'/'+tag[1:]

    # if word in quote, highlight directly
    if word in quote:
        quote = quote.replace(word, f"{tag}{word}{close_tag}")
    elif '・' in stem:
        tail_length = len(stem)-stem.find('・')-1
        word_stem = word[:-tail_length]
        quote = quote.replace(word_stem, f"{tag}{word_stem}{close_tag}")
    else:
        quote += f"(study word: {word})"

    return quote
    
    
    
# #%%
# quote = '淋しくて淋しくて、どうやって生きていっていいかわからないくらいだった。'
# word = '淋しい'
# stem = 'さびし・い'




#%%

#%%
