import re

# function to covert raw infobox text into a dictionary with key value pairs
def convert_to_dict(text):
    text = re.sub(r' *\| *',r'|',text)
    res = dict()
    text = text[2:-2]
    pos = text.find("|")
    line = text[:pos]
    entry = re.sub(r'<.*?>', ' ', line[8:])
    entry = re.sub(r'[^\w]', ' ', entry)
    res[line[:7]] = entry.strip()
    text = text[pos+1:]
    while(text != ""):
        pos_new = text.find('|')
        test_text = text[:pos_new]
        while((is_matched(test_text) != True) and pos_new != -1):
            pos_temp = text[pos_new+1:].find('|') + 1
            if pos_temp == 0:
                test_text = text
                break
            pos_new += pos_temp
            test_text = text[:pos_new+1]
            
        line = test_text
        pos_equals = line.find('=')
        key, val = line[:pos_equals],line[pos_equals+1:]
        key = key.strip()
        val = val.strip()
        if val != '':
           # print(key)
           res[key] = val
        text = text[pos_new+1:]
        try:
            if text[0] == '|':
                text = text[1:]
        except:
            continue
        if text.find('|') == -1:
            break
        
    return res  


"""
    Finds out how balanced an expression is.
    With a string containing only brackets.

    >>> is_matched('[]()()(((([])))')
    False
    >>> is_matched('[](){{{[]}}}')
    True
"""
def is_matched(expression):
    opening = tuple('({[')
    closing = tuple(')}]')
    mapping = dict(zip(opening, closing))
    queue = []

    for letter in expression:
        if letter in opening:
            queue.append(mapping[letter])
        elif letter in closing:
            if not queue or letter != queue.pop():
                return False
    return not queue
