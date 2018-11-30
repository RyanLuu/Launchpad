import parser

def make_cast(cl_table):
    cast = Cast()
    for cl in cl_table:
        if cl[0] not in cast:
            cast.add_character(cl[0])
        cast.get_character(cl[0]).add_line(cl[1])
    return cast

def combine(casts):
    full_cast = Cast()
    for cast in casts:
        for char in cast:
            if char not in full_cast:
                full_cast.add_character(char.name)
            full_cast.get_character(char.name).add_lines(char.lines)

    return full_cast

class Cast:

    def __init__(self):
        self.characters = [] 

    @property
    def all_lines(self):
        lines = []
        for c in self.characters:
            lines.extend(c.lines)
        return lines

    @property
    def all_words(self):
        words = []
        for c in self.characters:
            words.extend(c.words)
        return words

    def filter(self, min_lines=0):
        self.characters = [c for c in self.characters if len(c.lines) >= min_lines]
        return self

    def add_character(self, char):
        if isinstance(char, str):
            char = Character(char)
        if char not in self:
            self.characters.append(char)

    def get_character(self, name):
        return next((c for c in self.characters if c.name == name), None)

    def __len__(self):
        return len(self.characters)

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

    def add_lines(self, lines):
        for line in lines:
            self.add_line(line)

    def add_line(self, line):
        self.lines.append(line)
        self.words.extend(parser.line_to_words(line))

    @property
    def average_wpL(self):
        return len(self.words) / len(self.lines)

    @property
    def average_lpw(self):
        return len(''.join(self.words)) / len(self.words)

    def __str__(self):
        return "{} ({})".format(self.name, len(self.lines))
