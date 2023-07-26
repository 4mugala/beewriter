import re
import glob
import os


FILE_SEP = os.sep

class NumStr(str):
    def __less_than(self, v, v1):
        a = re.match("(.*)(\((\d+)\))", v)
        b = re.match("(.*)(\((\d+)\))", v1)
        if a and b:
            if a.group(1) == b.group(1):
                if int(a.group(3)) < int(b.group(3)):
                    return v
                else:
                    return v1

    def __lt__(self, other):
        lt = self.__less_than(self, other)
        if lt:
            return lt == self
        return super().__lt__(other)



def find_links(arg, links=[]):
    link_match = re.search(r"([^0-9\s]{3,6})://(\S{2,}\.)+(\S+/?)+", arg)

    if link_match:
        link = link_match.group()
        if link not in links:
            links = links + [link, ]
        return find_links(arg[link_match.span()[1]:], links)
    else:
        return links


def item_unique_name(new_item, items_list):
    items_list = sorted([NumStr(x) for x in items_list])

    if new_item in items_list:
        ind = items_list.index(new_item)
        items_list = items_list[ind+1:]
    else:
        return new_item

    inc = 1
    for item in items_list:
        name = new_item + f" ({inc})"
        if item == name:
            inc += 1
        else:
            if name in items_list:
                inc += 1
            else:
                break

    return new_item + f" ({inc})"

def add_os_sep(path):
    if path.endswith(FILE_SEP):
        return path
    else:
        return path + FILE_SEP


def inc_rename_dir(filename, root_path, ext):
    def remove_ext(path):
        return path[:-len(ext)]

    file_pathname = filename
    if os.path.dirname(file_pathname) == root_path:
        if file_pathname.endswith(ext):
            file_pathname = remove_ext(filename)
    else:
        if file_pathname.endswith(ext):
            file_pathname = f"{add_os_sep(root_path)}{remove_ext(filename)}"

    note_paths = glob.glob(f"{add_os_sep(root_path)}*{ext}")
    fpn_list = [remove_ext(path) for path in note_paths]
    file_pathname = item_unique_name(file_pathname, fpn_list)
    return file_pathname + ext

