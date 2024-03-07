def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def keep_int_and_floats_in_list(S):
    i = 0
    while i < len(S):
        if isinstance(S[i], str):
            S.pop(i)
        else:
            i+=1
    return S

def group_formats(formats : list) -> list:
    #create a list of lists of formats that are close to each other (0.5 difference)
    formats = sorted(formats)
    groups = []
    current_group = []
    current_format = formats[0]
    for format in formats:
        if format - current_format <= 2:
            current_group.append(format)
        else:
            groups.append(current_group)
            current_group = [format]
        current_format = format
    groups.append(current_group)
    return groups

def find_max_list(list):
    list_len = [len(i) for i in list]
    return len(list) - 1 - list_len[::-1].index(max(list_len))

def find_good_key_in_dict(dict : dict, value) -> str:
    for key in dict.keys():
        if value in dict[key]:
            return key
    return None

def create_dict_and_assign_styles_from_format(formats : list) -> dict:
    #create a dictionary with the format as key and the style as value
    styles = {}
    content_format_index = find_max_list(formats)
    i = 0
    for l in formats[:content_format_index]:
        formats[content_format_index - i] += l
        del formats[formats.index(l)]
        i+=1
    number_of_styles = len(formats)
    styles["content"] = sorted(list(set(formats[0])))
    for i in range(1,len(formats)):
        styles["title"+str(number_of_styles-i)] = sorted(list(set(formats[i])))
    return styles

def get_style_of_line(size : float, fontname : str):
    if fontname == "XFQKGD+Consolas":
        return "code"
    elif (size >= 9 and size < 11.5) or fontname == "CRRYJU+Wingdings-Regular":
        return "content"
    elif size >= 11.5 and size <= 12.7:
        return "title5"
    elif size >= 12.8 and size <= 13.5:
        return "title4"
    elif size > 13.5 and size <= 15.5:
        return "title3"
    elif size > 15.5 and size <= 18.5:
        return "title2"
    elif size > 19 and size < 30:
        return "title1"
    else:
        return "unknown"