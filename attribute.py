class Attribute:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.less_than_value = None
        self.more_than_value = None
        self.less_than_or_equal_to_value = None
        self.more_than_or_equal_to_value = None

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "Attribute: " + self.name + "\n\rType: " + self.type

    def set_less_than_value(self, value):
         self.less_than_value = value

    def set_more_than_value(self, value):
         self.more_than_value = value

    def set_less_than_or_equal_to_value(self, value):
         self.less_than_or_equal_to_value = value

    def set_more_than_or_equal_to_value(self, value):
         self.more_than_or_equal_to_value = value
