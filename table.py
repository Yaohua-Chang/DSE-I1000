import random

class Table:

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, name, attributes, delimiter = "->"):
        self.name = name
        self.attributes = sorted(attributes)
        self.attributes_names = set([a.name for a in attributes])
        self.master_key = ""
        self.keys = set()
        self.superkeys = set()
        self.fds = []
        self.mvds = []
        self.left_list = [] #For NF check
        self.right_list = [] #For NF check
        self.delimiter = delimiter
        self.seen_fd = set()
        self.nf = ""
        self.tuples = {}
        self.parent_database = None  # need reference to Database object for foreign keys

    def __repr__(self):
        out = "Table: " + self.name + "\n\r"
        for name in sorted(self.attributes_names):
            out += " | " + name
        out += " |\n\r" + "-" * 5 * len(self.attributes)
        for k in self.tuples:
            out += "\n\r | "
            t = self.tuples[k]
            for c in t:
                out += str(c) + " | "
        return out

    #########
    # PRINT #
    #########

    def print_attributes(self):
        print("The table named: ", self.name, "\nHas attributes:")
        for attr in self.attributes:
            print(attr.name , "  " + attr.type, end = '\n')

    def print_fds(self):
        print("The table named: ", self.name, "\nHas FD's: ", self.fds)

    def print_mvds(self):
        print("The table named: ", self.name, "\nHas MVD's: ", self.mvds)

    def print_boolean_conditions(self):
        print("The table named: ", self.name, " has boolean conditions:")
        for attr in self.attributes:
            if attr.more_than_value != None and attr.less_than_value != None:
                print(str(attr.more_than_value) + " < " + attr.name , " < " + str(attr.less_than_value), end='\n')
            elif attr.more_than_value != None:
                print(attr.name , " > " + str(attr.more_than_value), end='\n')
            elif attr.less_than_value != None:
                print(attr.name , " < " + str(attr.less_than_value), end='\n')

    ###############
    # CONSTRAINTS #
    ###############

    def add_fd(self, fd):

        try:
            lhs, rhs = fd.split(self.delimiter)
        except ValueError:  # if can't split & unpack into 2 separate values
            return "Must have a LHS & RHS!"

        # check for attributes not in table
        if not set(lhs).issubset(self.attributes_names) or not set(rhs).issubset(self.attributes_names):
            return "This is wrong FD. There is no such attribute in the table"

        # remove trivial FDs
        if set(rhs).issubset(set(lhs)):
            return "This is trivial FD"

        # add fd
        if fd not in self.seen_fd:
            if len(rhs) != 1: #Convert fds to non-trivial form if RHS has more than 1 attribute
                for element in rhs:
                    f_d = lhs + "->" + element #Not typo. f_d is not fd below
                    self.fds.append(f_d) #Not typo
                    self.seen_fd.add(f_d)
            else:
                self.fds.append(fd)
                self.seen_fd.add(fd)
        else:
            return "The fd: " + fd + " has already been added!"

        # add mvd that is implied from this fd
        self.mvds.append(lhs + "->->" + rhs)

        return "Added a new fd successfully: " + fd

    def remove_fd(self, fd_to_rm):
        if fd_to_rm not in self.fds:
            return "Invalid input. FD does not exist"
        else:
            tmp_fds = [fd for fd in self.fds if fd != fd_to_rm]
            self.fds = tmp_fds
            self.seen_fd = set(tmp_fds)
            return "The fd: " + fd_to_rm + " was successfully removed."

    def add_mvd(self, mvd):

        try:
            lhs, rhs = mvd.split("->->")
        except ValueError:  # if can't split & unpack into 2 separate values
            return "Must have a LHS & RHS!"

        # check defining mvd for table of 2 attr
        if len(self.attributes) <= 2:
            return "MVD trivial for a table with <= 2 attributes"
        # check attr not in table
        if not set(lhs).issubset(self.attributes_names) or not set(rhs).issubset(self.attributes_names):
            return "This is wrong MVD. There is no such attribute in the table"
        # remove trivial mvd
        if set(rhs).issubset(lhs):
            return "This is a trivial mvd"

        if mvd.replace("->->","->") in self.seen_fd:
            return "MVD that is trivialized by an existing FD"

        self.mvds.append(lhs + "->->" + rhs)

        return "Added a new mvd successfully: " + mvd

    def add_boolean_conditions(self, input_str):
        if "<" in input_str:
            input_split = input_str.replace(" ","").split('<')
            if len(input_split) != 2 or input_split[1] == "":
                return "This is invaild input."
            else:
                if not input_split[0] in self.attributes_names:
                    return "There is no the attribute in the table"
                else:
                    for attr in self.attributes:
                        if attr.name == input_split[0]:
                            less_than_value = int(input_split[1])
                            if attr.more_than_value != None:
                                if less_than_value > attr.more_than_value:
                                    attr.set_less_than_value(less_than_value)
                                    return "Add boolean conditions successfully"
                                else:
                                    return "This is conflicting Boolean conditions"
                            else:
                                attr.set_less_than_value(less_than_value)
                                return "Add boolean conditions successfully"

        elif ">" in input_str:
            input_split = input_str.replace(" ","").split('>')
            if len(input_split)!=2 or input_split[1] == "":
                return "This is invaild input."
            else:
                if not input_split[0] in self.attributes_names:
                    return "There is no the attribute in the table"
                else:
                    for attr in self.attributes:
                        if attr.name == input_split[0]:
                            more_than_value = int(input_split[1])
                            if attr.less_than_value != None:
                                if more_than_value < attr.less_than_value:
                                    attr.set_more_than_value(more_than_value)
                                    return "Add boolean conditions successfully"
                                else:
                                    return "This is conflicting Boolean conditions"
                            else:
                                attr.set_more_than_value(more_than_value)
                                return "Add boolean conditions successfully"

    ###########
    # CLOSURE #
    ###########

    def closure(self, attr):

        lhs_list = [fd.split(self.delimiter)[0] for fd in self.fds]
        rhs_list = [fd.split(self.delimiter)[1] for fd in self.fds]

        seed = attr

        outputs = set(seed)
        count_fds = len(lhs_list)

        # to compute closure of the seed
        for _ in range(count_fds):
            for index in range(count_fds):
                if set(lhs_list[index]).issubset(outputs):
                    outputs.add(rhs_list[index])
        return outputs

    ########
    # KEYS #
    ########

    def get_keys(self):
        keys = set()
        lhs_list = [fd.split(self.delimiter)[0] for fd in self.fds]
        rhs_list = [fd.split(self.delimiter)[1] for fd in self.fds]

        for seed in lhs_list:
            outputs =  set(seed)
            count_fds = len(lhs_list)

            # to compute closure of each seed
            for _ in range(count_fds):
                for index in range(count_fds):
                    if set(lhs_list[index]).issubset(outputs):
                        outputs.add(rhs_list[index])

            diff_attrs_outputs = self.attributes_names.difference(outputs)
            for element in diff_attrs_outputs:
                seed = seed + str(element)
            keys.add(seed)

        self.superkeys = set(keys)
        self.keys = self.superkeys
        record = set()

        # to remove super key
        for key_i in self.superkeys:
            for key_j in self.superkeys:
                if set(key_i).issuperset(key_j) and key_i != key_j:
                    record.add(key_i)

        for element in record:
            self.keys.remove(element)
        return self.keys

    def print_keys(self):
        if len(self.keys) == 0:
            self.get_keys()
        print("All keys for this table are : ", str(self.keys))

    def user_define_key(self):
        k = input("What key would you like to use? (type \'rand\' to have it selected for you): ")
        if k == "rand":
            self.master_key = random.sample(self.keys,1)[0]
            print("You have been given the key: " + self.master_key)
            return True
        valid_key = k in self.keys
        while not valid_key:
            print("Unfortunately that's not a viable key. Here are you options:\n" + str(table.keys))
            k = input("Try a different key: ")
            valid_key = k in self.keys
        print("Great selection! " + k + " is a viable key")
        self.master_key = k
        return True

    ################
    # NORMAL FORMS #
    ################

    def determine_1NF(self):
        subkey = []
        for key in self.keys:
            subkey.extend(set(key))

        for i in range(len(self.left_list)):
            for key in self.keys:
                if  set(self.left_list[i]).issubset(set(key)) \
                and set(self.left_list[i]) != set(key) and not set(self.right_list[i]).issubset(set(subkey)):
                    return True
        return False

    def determine_2NF(self):
        non_prime_attrs = self.attributes_names
        for key in self.keys:
            non_prime_attrs -= set(key)

        for i in range(len(self.left_list)) :
            if set(self.left_list[i]).issubset(non_prime_attrs) and set(self.right_list[i]).issubset(non_prime_attrs):
                return True
        return False

    def determine_3NF(self):
        for key in self.keys:
            for i in range(len(self.right_list)) :
                # for a dependency A → B, A cannot be a non-prime attribute, if B is a prime attribute.
                if set(self.right_list[i]).issubset(key) and not set(self.left_list[i]).issubset(key):
                    return True
        return False

    def get_normal_form(self):
        self.get_keys()

        for fd in self.fds:
            fd_split = fd.split("->")
            self.left_list.append(fd_split[0])
            self.right_list.append(fd_split[1])

        if self.determine_1NF():
            self.nf = "1NF"
        elif self.determine_2NF():
            self.nf = "2NF"
        elif self.determine_3NF():
            self.nf = "3NF"
        else:
            self.nf= "BCNF"
        print("This table has normal form: " + self.nf)
        return self.nf


    ##########
    # TUPLES #
    ##########

    # TODO: foreign key designation
    def add_tuple(self, t):
        # need a master key before beginning to add tuples
        if self.master_key == "":
            self.user_define_key()

        # pick out the master key from the input tuple
        k = ""
        for i, c in enumerate(sorted(self.attributes_names)):
            if c in self.master_key:
                k += str(t[i])

        # check FD consistency
        for fd in self.fds:
            lhs, rhs = fd.split("->")
            idx_lhs = sorted(list(self.attributes_names)).index(lhs)
            idx_rhs = sorted(list(self.attributes_names)).index(rhs)
            # iterate over other tuples in table and check for consistency
            dict_check = {}
            for key in self.tuples:
                # pull out rhs & lhs from each tuple
                lhs_value = ''.join(str(self.tuples[key][idx_lhs:(idx_lhs + len(lhs))]))
                rhs_value = ''.join(str(self.tuples[key][idx_rhs:(idx_rhs + len(rhs))]))
                # the lhs_value is already in the table; now we can check if consistency remains
                # if any set has more than one object it implies RHS -> LHS has been violated
                # b/c RHS points to 2 distinct values of LHS
                if lhs_value not in dict_check:
                    dict_check[lhs_value] = set()
                    dict_check[lhs_value].add(rhs_value)
                else:
                    dict_check[lhs_value].add(rhs_value)
                if len(dict_check[lhs_value]) > 1:
                    print("This breaks the consistency implied by the FD: " + fd)
                    return False

        # check for foreign key
        if self.parent_database:
            for _, table in self.parent_database.tables.items():
                # pull out the key of that table
                if table == self:  # ignore the current table reference
                    continue
                if table.master_key == "":
                    # add a key (table doesn't have one)
                    print("The table " + table.name + " doesn't have a current master key. \n\r")
                    table.user_define_key()
                tmp_key = table.master_key
                # does it exist in our current table's key?
                for c in tmp_key:
                    if c in self.master_key:
                        # if so, where is it?
                        pass # left off here; will finish today/tomorrow (Thurs/Fri)
        else:
            print("This table is not part of a database!")

        # add tuple
        self.tuples[k] = t
        return True

    def get_tuple(key):
        try:
            return self.tuples[key]
        except KeyError:
            print("There is no tuple with key: " + key)
