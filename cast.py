import re

def make_cast(cl_table):
    cast = Cast()
    for cl in cl_table:
        if cl[0] not in cast:
            cast += cl[0]
        cast.get_character(cl[0]).add_line(cl[1])
    return cast

def line_to_words(line):
    return re.findall(r"\b[A-Za-z]+(?:[-'][A-Za-z]+)?\b", line)

class Cast:

    def __init__(self):
        self.characters = []

    def filter(self, min_lines=0):
        self.characters = [c for c in self.characters if len(c.lines) >= min_lines]

    def get_character(self, name):
        return next((c for c in self.characters if c.name == name), None)

    def __add__(self, other):
        
        if isinstance(other, str):
            other = Character(other)

        if isinstance(other, Character):
            if not self.__contains__(other):
                self.characters.append(other)
            else:
                print("we")
            return self
        else:
            return NotImplementedError
        
    def __iter__(self):
        return iter(self.characters)
    
    def __contains__(self, key):
        if isinstance(key, Character):
            return key.name in [c.name for c in self.characters]
        
        if isinstance(key, str):
            return key in [c.name for c in self.characters]
        return NotImplementedError

    def __getitem__(self, key):
        return self.characters[key]

    def __str__(self):
        return "{{{}}}".format(", ".join((str(c) for c in self.characters)))

class Character:

    def __init__(self, name):
        self.name = name
        self.lines = []
        self.words = []

    def add_line(self, line):
        self.lines.append(line)
        self.words.extend(line_to_words(line))

    @property
    def average_wpL(self):
        return len(self.words) / len(self.lines)

    @property
    def average_lpw(self):
        return len(''.join(self.words)) / len(self.words)

    def __str__(self):
        return "{} ({})".format(self.name, len(self.lines))
