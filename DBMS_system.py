from database import Database
from table import Table
from attribute import Attribute

def create_table():
    table_name = input("Please input new table name:")
    attrs = []
    while True:
        input_str = input("Please input the name and type (use , as delimiter) for one attribute(or input quit to stop):")
        if input_str == "quit":
            if len(attrs) == 0:
                print("You need to input at least 1 attribute for the new table")
            else:
                break
        else:
            input_split = input_str.replace(" ","").split(",")
            if len(input_split) != 2:
                print("The input is not correct, please input again.")
            else:
                attrs.append(Attribute(input_split[0], input_split[1]))
                print("Successfully add a new attribute")

    new_table = Table(table_name, attrs)

    print("Please input at least one constraint. Input 'quit' at any time to stop.")

    while True:
        input_str = input("Please input Boolean condition:")
        if input_str == "quit":
            break
        feedback = new_table.add_boolean_conditions(input_str.replace(" ",""))
        print(feedback)

    while True:

        input_str = input("Please input FD:")
        if input_str == "quit":
            break
        feedback = new_table.add_fd(input_str.replace(" ",""))
        print(feedback)    
    new_table.fds = list(set(new_table.fds)) #Ensuring unique FDs only
    
    while True:

        input_str = input("Please input MVD:")
        if input_str == "quit":
            break
        feedback = new_table.add_mvd(input_str.replace(" ",""))
        print(feedback)

    return new_table

def update_normal_form(table):
    """Will update today"""
    if table.nf == "":
        table.get_normal_form()

    print("Currently this table has normal form: " + table.nf)

    if table.nf != "3NF" or table.nf != "BCNF":
        print("You can either delete this table or update its FD's.")
        decision = input("Either type \'del\' for deletion or \'u\' to update:")

        if decision == 'del':
            del table
        elif decision == 'u':
            done = False
            while not done:
                input_str = input("Type \'a\' to add a new FD or \'d\' to delete a FD':")
                if input_str == 'a':      
                    new_fd = input("Add a new FD: ")
                    feedback = table.add_fd(new_fd.replace(" ",""))
                    print(feedback)
                    new_nf = table.get_normal_form()
                    again = input("The table now has normal form " + table.nf + " would you like to continue (y/n)?")
                    if again == 'n':
                        done = True
                
                elif input_str == 'd':
                    del_fd = input("Enter FD to be deleted: ")
                    feedback = table.remove_fd(del_fd.replace(" ",""))
                    print(feedback)
                    new_nf = table.get_normal_form()
                    again = input("The table now has normal form " + table.nf + " would you like to continue (y/n)?")
                    if again == 'n':
                        done = True
                else:
                    print("That's not a valid decision!")
                                  
        else:
            print("That's not a valid decision!")

if __name__ == "__main__":
    new_table = create_table()
    new_table.print_attributes()
    new_table.print_boolean_conditions()
