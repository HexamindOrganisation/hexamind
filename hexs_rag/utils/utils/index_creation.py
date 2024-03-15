from hexs_rag.model.model.container import Container

INFINITE = 99999


def create_dic_levels(c: Container, dict_of_levels: dict = {}):
    if c.level == 0:
        dict_of_levels[c.level] = [0]
    for child in c.children:
        if child.level not in dict_of_levels:
            dict_of_levels[child.level] = [1 for _ in range(child.level)]
        create_dic_levels(child, dict_of_levels)
    if INFINITE in dict_of_levels.keys():
        dict_of_levels[INFINITE] = [1]
    return dict_of_levels


def create_good_indexes(c: Container, dict_of_levels: dict):
    actual_level = c.level
    c.index = dict_of_levels[actual_level].copy()
    actual_len = len(dict_of_levels[actual_level])
    temp_update = dict_of_levels[actual_level][-1]
    dict_of_levels[actual_level][-1] += 1
    for i in dict_of_levels.values():
        if len(i) > actual_len:
            i[actual_len - 1] = temp_update
    for child in c.children:
        c_lvl = child.level
        for i in dict_of_levels.values():
            if len(i) > c_lvl:
                i[c_lvl:] = [1 for _ in range(len(i[c_lvl:]))]
        create_good_indexes(
            child, dict_of_levels
        )  # Apply the function recursively to all children


def create_good_indexes_not_ordered_titles(c: Container, dict_of_levels: dict):
    actual_level = c.level
    c.index = dict_of_levels[actual_level].copy()
    actual_len = len(dict_of_levels[actual_level])
    temp_update = dict_of_levels[actual_level][-1]
    dict_of_levels[actual_level][-1] += 1
    for i in dict_of_levels.values():
        if len(i) > actual_len:
            i[actual_len - 1] = temp_update
    for child in c.children:
        c_lvl = child.level
        for i in dict_of_levels.values():
            if len(i) > c_lvl:
                i[c_lvl:] = [1 for _ in range(len(i[c_lvl:]))]
        create_good_indexes(
            child, dict_of_levels
        )  # Apply the function recursively to all children


def set_good_block_indexes(c: Container):
    for i in c.containers:
        for b in i.blocks:
            b.index = i.index


def set_indexes(c: Container):
    dict_levels = create_dic_levels(c)
    myKeys = list(dict_levels.keys())
    myKeys.sort()
    dict_levels = {key: dict_levels[key] for key in myKeys}
    if (
        c.children
        and c.children[0]
        and (c.children[0].level > min(list(dict_levels.keys())[1:]))
    ):
        c.children[0].level = min(list(dict_levels.keys())[1:])
        create_good_indexes_not_ordered_titles(c, dict_levels)
    else:
        create_good_indexes(c, dict_levels)
    set_good_block_indexes(c)
