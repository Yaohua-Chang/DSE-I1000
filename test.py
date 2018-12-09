from attribute import Attribute
from database import Database
from table import Table


db = Database()

# Adding attributes
A = Attribute("A", "integer")
B = Attribute("B", "integer")
C = Attribute("C", "integer")
D = Attribute("D", "string")
E = Attribute("E", "integer")
F = Attribute("F", "string")

t_one = Table("test1", [A,B,C,D,E,F])

# Adding  boolean conditions
t_one.add_boolean_conditions("A>10")
t_one.add_boolean_conditions("A<20")
t_one.add_boolean_conditions("B>=10")
t_one.add_boolean_conditions("B<=20")

# Adding conflicting boolean conditions
t_one.add_boolean_conditions("C>10")
t_one.add_boolean_conditions("C<5")

# invalid input
t_one.add_boolean_conditions("D")
t_one.add_boolean_conditions("D>")
t_one.add_boolean_conditions("G")
t_one.add_boolean_conditions("A")


# empty input
t_one.add_boolean_conditions("")

# what are we left with?
t_one.print_boolean_conditions()


# Adding fd's
# t_one.add_fd("AB->C")
# t_one.add_fd("BC->A")
# t_one.add_fd("BC->D")
# t_one.add_fd("CF->B")

# adding repeated fd
t_one.add_fd("A->B")

# trivial FD
t_one.add_fd("A->A")
t_one.add_fd("AB->A")

# invalid attributes
t_one.add_fd("G->A")

# empty input
t_one.add_fd("")

# invalid input
t_one.add_fd("A")
t_one.add_fd("G")
t_one.add_fd("G->H")
t_one.add_fd("A->->B")
t_one.add_fd("*AB -> BCD")

# what are we left with?
t_one.print_fds()

# removing FD
# t_one.remove_fd("A->B")
# t_one.print_fds()


# Adding  MVD
t_one.add_mvd("B->->C")
t_one.add_mvd("A->->BC")

# trivial MVD
t_one.add_mvd("A->->B")

# invalid input
t_one.add_mvd("D")
t_one.add_mvd("D->->")
t_one.add_mvd("G->->H")
t_one.add_mvd("A->D")


# empty input
t_one.add_mvd("")

# what are we left with?
t_one.print_mvds()

print(t_one)

# testing closure operator
attr = "CF"
out = t_one.closure(attr)
print("closure of " + attr + " = " + str(out))
t_one.get_keys()
t_one.print_keys()

# test normal forms
t_one.get_normal_form()

# test user_define_key
