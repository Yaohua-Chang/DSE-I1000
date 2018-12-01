
from table import Table
from attribute import Attribute

def create_table():
    # tabel_name = input("Please input new table name:")
    # attrs = []
    # while True:
    #     input_str = input("Please input the name and type (use , as delimiter) for one attribute(or input quit to stop):")
    #     if input_str == "quit":
    #         if len(attrs) == 0:
    #             print("You need to input at least 1 attribute for the new tabel")
    #         else:
    #             break
    #     else:
    #         input_split = input_str.replace(" ","").split(",")
    #         if len(input_split) != 2:
    #             print("The input is not correct, please input again.")
    #         else:
    #             attrs.append(Attribute(input_split[0], input_split[1]))

    # new_table = Table(tabel_name, attrs)

    fake_attrs = [Attribute("A", "string"),
            Attribute("B", "integer"),
            Attribute("C", "integer"),
            Attribute("D", "string"),
            Attribute("E", "string")]

    new_table = Table("Student", fake_attrs)

    while True:
        input_str = input("please input one constraint for the new tabel(or input quit to stop):")
        if input_str == "quit":
                break

        if "->->" in input_str:
            input_split = input_str.replace(" ","").split("->")
            feedback = new_table.add_mvd(input_split)
            print(feedback)
        elif "->" in input_str:
            input_split = input_str.replace(" ","").split("->")
            feedback = new_table.add_fd(input_split)
            print(feedback)
        elif ">" in input_str or "<" in input_str:
             feedback = new_table.add_boolean_conditions(input_str)
             print(feedback)
        else:
            print("Invalid constraint, please input again.")


    return new_table

def update_normal_form(table):
    if table.nf = "":
        table.get_normal_form()

    print("Currently this table has normal form: " + table.nf)

    if table.nf != "3NF" or table.nf != "BCNF":
        print("You can either delete this table or update its FD's.")
        decision = input("Either type \'d\' for deletion or \'u\' to update:")

        if decision == 'd':
            del table
        elif decision == 'u':
            done = False
            while not done:
                new_fd = input("Add a new FD: ")
                fd_split = new_fd.replace(" ","").split("->")
                feedback = table.add_fd(fd_split)
                print(feedback)
                new_nf = table.get_normal_form()
                again = input("The table now has normal form " + table.nf + " would you like to continue (y/n)?")
                if again == 'n':
                    done = True
        else:
            print("That's not a valid decision!")

if __name__ == "__main__":
    new_table = create_table()
    new_table.print_boolean_conditions()
