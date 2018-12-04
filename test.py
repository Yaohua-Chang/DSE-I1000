from attribute import Attribute
from database import Database
from table import Table


db = Database()

# Adding attributes
A = Attribute("A", "string")
B = Attribute("B", "string")
C = Attribute("C", "string")
D = Attribute("D", "string")

t_one = Table(db, "test1", [A,B,C,D])
t_one.print_attributes()

# Adding fd's
t_one.add_fd("A->B")
# adding repeated fd
t_one.add_fd("A->B")

# trivial FD
t_one.add_fd("A->A")
t_one.add_fd("AB->A")

# invalid attributes
t_one.add_fd("E->A")

# what are we left with?
t_one.print_fds()

# removing FD
# t_one.remove_fd("A->B")
# t_one.print_fds()

# testing closure operator
attr = "A"
out = t_one.closure(attr)
print("closure of " + attr + " = " + str(out))
t_one.get_keys()
t_one.print_keys()

# test normal forms

# test user_define_key

# test boolean conditions