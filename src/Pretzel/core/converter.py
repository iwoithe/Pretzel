def list_to_string(_list: list) -> str:
    list_string = ""

    for item in _list:
        list_string += item
        #if _list[_list.index(item)] != _list[-1]:
        #    list_string += ","
        list_string += ","

    return list_string