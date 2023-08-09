import datetime
import os
import glob
from beesups import inc_rename_dir, add_os_sep


BEE_EXCEPTION_STR = "The format of the input text is not Bee (avoid new lines in author and priority properties)."
FILE_EXITS_EXCEPTION = "File already exists"


class FormatNotBeeError(Exception):
    pass


class BeeReader:
    def __init__(self, note="", *, src=None):
        self.__token_stack = []
        self.__source = src
        self.__title = None
        self.__author = None
        self.__priority = None
        self.__content = None

        if self.__source:
            with open(self.__source, "r") as file:
                self.__parse_doc(file.read())
        else:
            self.__parse_doc(note)

    def source(self):
        return self.__source

    def content_chars(self):
        count = 0
        for i in self.__content:
            if not i.isspace():
                count += 1
        return str(count)

    def content_words(self):
        return len(self.__content.split())

    def content_lines(self):
        return len(self.__content.split("\n"))

    def title(self):
        return self.__title

    def author(self):
        return self.__author

    def priority(self):
        return self.__priority

    def content(self):
        return self.__content

    def __extract_properties(self, prop, *, is_title=False):
        def do_multiple_pops(num):
            for i in range(num):
                self.__token_stack.pop()

        while True:
            if self.__token_stack:
                if prop is None:
                    do_multiple_pops(3)
                    prop = ""

                if is_title:
                    if self.__token_stack[-1] == " " and self.__token_stack[-2] == "?":
                        do_multiple_pops(2)
                else:
                    if self.__token_stack:
                        if self.__token_stack[-1] == "\n":
                            raise FormatNotBeeError(BEE_EXCEPTION_STR)

                if self.__token_stack:
                    prop = self.__token_stack.pop() + prop

            else:
                break
        return prop

    def __parse_doc(self, data):
        token_index = 0
        if data[0] != "?" and data[1] != " ":
            raise FormatNotBeeError(BEE_EXCEPTION_STR)

        for token in data:
            self.__token_stack.append(token)

            if len(self.__token_stack) >= 5:
                if (self.__token_stack[-1] == " " and self.__token_stack[-2] == "@"
                        and self.__token_stack[-3] == "\n" and self.__title is None):
                    self.__title = self.__extract_properties(self.__title, is_title=True)

            if len(self.__token_stack) >= 3:
                if (self.__title is not None and self.__token_stack[-1] == " "
                        and self.__token_stack[-2] == "#" and self.__token_stack[-3] == "\n"):
                    self.__author = self.__extract_properties(self.__author)

            if len(self.__token_stack) >= 3:
                if (self.__author is not None and self.__token_stack[-1] == "\n"
                        and self.__token_stack[-2] == "=" and self.__token_stack[-3] == "\n"):
                    self.__priority = self.__extract_properties(self.__priority)

            token_index += 1

            if self.__priority is not None:
                break

        if self.__content is None and self.__priority is not None:
            self.__content = data[token_index:]

        if self.__content is None:
            raise FormatNotBeeError(BEE_EXCEPTION_STR)


class BeeWriter:
    def __init__(self, *, author="", title="", content="", root_path="", note=None):
        if type(note) == BeeReader:
            self.__read_note(note)

        self.__author = author
        self.__title = title
        self.__content = content
        self.__root_path = root_path
        self.__priority = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")

    def __str__(self):
        return self.__make_note()

    def __read_note(self, note):
        self.__title = note.title()
        self.__author = note.author()
        self.__priority = note.priority()
        self.__content = note.content()

    def set_title(self, title):
        self.__title = title

    def set_author(self, author):
        self.__author = author

    def set_priority(self, priority):
        self.__priority = priority

    def set_content(self, content):
        self.__content = content

    def append_content(self, content):
        self.__content += content

    def __make_note(self):
        return f"? {self.__title}" \
               f"\n@ {self.__author}" \
               f"\n# {self.__priority}" \
               f"\n=\n{self.__content}"

    def save_file(self, *, filename_inc=False):
        note = self.__make_note()
        # no_extension_file_path_name
        no_ext_fpn = f"{add_os_sep(self.__root_path)}{self.__title}"
        if filename_inc:
            path = inc_rename_dir(no_ext_fpn, self.__root_path, ".bee")
        else:
            path = no_ext_fpn + ".bee"

        if not os.path.exists(self.__root_path):
            os.makedirs(self.__root_path)

        if os.path.exists(path):
            other_note = BeeReader(src=path)
            if other_note.title() != self.__title:
                raise Exception(FILE_EXITS_EXCEPTION)

        with open(path, "w") as file:
            file.write(note)
            file.close()


def find_notes(root_path):
    root_path = add_os_sep(root_path)
    note_paths = glob.glob(f"{root_path}*.bee")
    note_list = []
    for path in note_paths:
        try:
            note_list.append(BeeReader(src=path))
        except:
            continue
    return note_list
