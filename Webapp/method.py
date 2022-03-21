import re

regex = re.compile(r"[a-zA-Z0-1\s\d,]{0,50}")

def safe_input(string):
    if string == None:
        return None
    safe_string = list_to_string(regex.findall(string))
    return safe_string[:-1]

def safe_input_list(list):
    if list == None:
        return None
    outlist = []
    for string in list:
        outlist.append(list_to_string(regex.findall(string))[:-1])
    return outlist


def Multicaster_ilike(list):
    if list == None:
        return None
    long =""
    for string in list:
        long = long  + f"Spells.Caster.ilike('%' + '{string}' + '%'),"

    return "," + long[:-1]

def list_to_string(list):
    string_out = ""
    for stuff in list:
        string_out = string_out + str(stuff) + ","


    return string_out[:-1]

def seleclist(ind):
    out = list()

    for val in ind:
        out.append([val, val])
    return out

def sqll_array_list(ind):
    out = str(ind).split(",")
    return out


def spell_quick_sort(ind):
    ind = list(ind)
    if len(ind) <= 1:
        return ind
    else:
        pivotpoint = ind.pop()

    more = list()
    less = list()
    for spell in ind:
        if spell.Level > pivotpoint.Level:
            more.append(spell)
        else:
            less.append(spell)

    return spell_quick_sort(less) + [pivotpoint] + spell_quick_sort(more)

