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
        out += "\n\r"
        return out

    def __str__(self):
        out = "Table: " + self.name + "\n\r"
        for name in sorted(self.attributes_names):
            out += " | " + name
        out += " |\n\r" + "-" * 5 * len(self.attributes)
        for k in self.tuples:
            out += "\n\r | "
            t = self.tuples[k]
            for c in t:
                out += str(c) + " | "
        out += "\n\r"
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
            if attr.more_than_or_equal_to_value != None:
                print(attr.name , " >= " + str(attr.more_than_or_equal_to_value), end='\n')
            if attr.less_than_or_equal_to_value != None:
                print(attr.name , " <= " + str(attr.less_than_or_equal_to_value), end='\n')
            if attr.more_than_value != None:
                print(attr.name , " > " + str(attr.more_than_value), end='\n')
            if attr.less_than_value != None:
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

    def check_input_split(self, input_split):
        if len(input_split) != 2 or input_split[1] == "":
            return "This is invaild input."

        if not input_split[0] in self.attributes_names:
            return "There is no the attribute in the table"

        return "";

    def get_attr_by_name(self, attr_name):
        for attr in self.attributes:
            if attr.name == attr_name:
                return attr

    def add_boolean_conditions(self, input_str):
        if "<=" in input_str:
            input_split = input_str.replace(" ","").split('<=')

            feedback = self.check_input_split(input_split)
            if feedback != "":
                return feedback

            attr = self.get_attr_by_name(input_split[0])
            if attr.type != "integer":
                return "Can't add boolean conditions to attribute whoes type is not integer."

            less_than_or_equal_to_value = int(input_split[1])
            if attr.more_than_or_equal_to_value != None:
                if less_than_or_equal_to_value > attr.more_than_or_equal_to_value:
                    attr.set_less_than_or_equal_to_value(less_than_or_equal_to_value)
                    return "Add boolean conditions successfully"
                else:
                    return "This is conflicting Boolean conditions"
            else:
                attr.set_less_than_or_equal_to_value(less_than_or_equal_to_value)
                return "Add boolean conditions successfully"

        elif ">=" in input_str:
            input_split = input_str.replace(" ","").split('>=')

            feedback = self.check_input_split(input_split)
            if feedback != "":
                return feedback

            attr = self.get_attr_by_name(input_split[0])
            if attr.type != "integer":
                return "Can't add boolean conditions to attribute whoes type is not integer."

            more_than_or_equal_to_value = int(input_split[1])
            if attr.less_than_or_equal_to_value != None:
                if more_than_or_equal_to_value < attr.less_than_or_equal_to_value:
                    attr.set_more_than_or_equal_to_value(more_than_or_equal_to_value)
                    return "Add boolean conditions successfully"
                else:
                    return "This is conflicting Boolean conditions"
            else:
                attr.set_more_than_or_equal_to_value(more_than_or_equal_to_value)
                return "Add boolean conditions successfully"
        elif "<" in input_str:
            input_split = input_str.replace(" ","").split('<')

            feedback = self.check_input_split(input_split)
            if feedback != "":
                return feedback

            attr = self.get_attr_by_name(input_split[0])
            if attr.type != "integer":
                return "Can't add boolean conditions to attribute whoes type is not integer."

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

            feedback = self.check_input_split(input_split)
            if feedback != "":
                return feedback

            attr = self.get_attr_by_name(input_split[0])
            if attr.type != "integer":
                return "Can't add boolean conditions to attribute whoes type is not integer."

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
        if len(self.keys) == 0:
            print("There is no key in the table [" + self.name + "].")
            return False
        k = input("What key would you like to use? (type \'rand\' to have it selected for you): ")
        if k == "rand":
            self.master_key = random.sample(self.keys,1)[0]
            print("You have been given the key: " + self.master_key)
            return True
        valid_key = k in self.keys
        while not valid_key:
            print("Unfortunately that's not a viable key. Here are you options:\n" + str(self.keys))
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
        non_prime_attrs = self.attributes_names.copy()
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

    def add_tuple(self, t):
        if self.master_key == "":
            self.user_define_key()

        if len(t) != len(self.attributes_names):
            print("Invalid tuple input, must be value for every attribute")
            return False

        # type check
        for i, el in enumerate(t):
            attr_types = [a.type for a in sorted(self.attributes)]
            if attr_types[i] == "integer":
                valid_tuple = isinstance(el, int)
            else:
                valid_tuple = isinstance(el, str)
            if not valid_tuple:
                print("The type check failed on: " + str(el) + " at position " + str(i))
                return False

        # condition check
        for i, attr in enumerate(self.attributes):
            if attr.less_than_value:
                valid_tuple = t[i] < attr.less_than_value
            elif attr.more_than_value:
                valid_tuple = t[i] > attr.more_than_value
            elif attr.less_than_or_equal_to_value:
                valid_tuple = t[i] <= attr.less_than_or_equal_to_value
            elif attr.more_than_or_equal_to_value:
                valid_tuple = t[i] >= attr.more_than_or_equal_to_value
            if not valid_tuple:
                print("The conditional check failed on: " + str(t[i]) + " at position " + str(i))
                return False

        k = ""
        for i, c in enumerate(sorted(self.attributes_names)):
            if c in self.master_key:
                k += str(t[i])

        # check FD consistency
        for fd in self.fds:
            lhs, rhs = fd.split("->")
            idx_lhs = [i for i, c in enumerate(sorted(self.attributes_names)) if c in lhs]
            idx_rhs = [i for i, c in enumerate(sorted(self.attributes_names)) if c in rhs]
            dict_check = {}
            tmp_tuples = self.tuples.copy()
            tmp_tuples.update({k:t})
            for key in tmp_tuples:
                str_tup = ''.join(map(str, tmp_tuples[key]))
                lhs_value, rhs_value = "", ""
                for idx in idx_lhs:
                    lhs_value += str_tup[idx]
                for idx in idx_rhs:
                    rhs_value += str_tup[idx]
                if rhs_value in dict_check:
                    dict_check[rhs_value].add(lhs_value)
                    if len(dict_check[rhs_value]) > 1:
                        # RHS points at two distinct LHS values; therefore violates prop. of FD
                        print("This breaks the consistency implied by the FD: " + fd)
                        return False
                else:
                    dict_check[rhs_value] = set()
                    dict_check[rhs_value].add(lhs_value)

        # check for foreign key designation
        if self.parent_database:
            for _, table in self.parent_database.tables.items():
                if table == self:  # ignore the current table reference
                    continue
                if table.master_key == "":
                    print("The table " + table.name + " doesn't have a current master key. \n\r")
                    table.user_define_key()

                # does it exist in our current table's key?
                val_found = False
                for c in table.master_key:
                    current_idx = sorted(list(self.attributes_names)).index(c)
                    if c in self.master_key:
                        # what's the index in the other table?
                        other_idx = sorted(list(table.attributes_names)).index(c)
                        # iterate over the other table's tuples
                        for _, tuple in table.tuples.items():
                            if tuple[other_idx] == t[current_idx]:
                                val_found = True
                if not val_found:
                    print("You can try adding new tuples to the other table " + table.name + ", right now have foreign key error.\n")
                    print("There is no value " + str(t[current_idx]) + " in that table!")
                    return False
        else:
            print("This table is not part of a database! No foreign key to check")

        # add tuple
        self.tuples[k] = t
        return True

    def get_tuple(self, key):
        try:
            return self.tuples[key]
        except KeyError:
            print("There is no tuple with key: " + key)

    def remove_tuple(self, key):
        try:
            del self.tuples[key]
        except KeyError:
            print("There is no tuple with key: " + key)

    ############
    # GROUPING #
    ############

    def get_attr_idx(self, attr_name):
        # pick out index of attributes
        if len(attr_name) == 1:
            return sorted(self.attributes_names).index(attr_name)
        else:
            return [sorted(self.attributes_names).index(c) for c in attr_name]

    def group_by(self, attr_name):
        grouping_dict = {}
        idx_group = self.get_attr_idx(attr_name)

        # iterate over available tuples & add values of grouped by attributes as keys to dict
        # while the keys for each tuples are included in the set() values of the dict
        for tuple_k, tuple_v in self.tuples.items():
            if len(attr_name) == 1:
                tuple_attr = tuple_v[idx_group]
            else:
                tuple_attr = tuple([tuple_v[i] for i in idx_group])
            if tuple_attr not in grouping_dict:
                grouping_dict[tuple_attr] = set()
            grouping_dict[tuple_attr].add(tuple_k)

        for group in grouping_dict:
            print("Grouping by: " + str(group))
            for k in grouping_dict[group]:
                print(self.get_tuple(k))
            print("#" * 15)

        return grouping_dict

    def get_tuple_conditions(self, attr_name, values, conditions):
        # pick out index of attributes being conditioned on
        idx_attr = self.get_attr_idx(attr_name)
        attr_dict = {}
        if len(attr_name) != len(values) or len(attr_name) != len(conditions):
            print("Must have same number of attributes, values, and conditions!")
        for i, v in enumerate(values):
            statement = conditions[i] + " " + str(v)
            attr_dict[statement] = set()  # store the keys satisfying the conditions
            # iterate over tuples, picking out attribute & checking
            for tuple_k, tuple_v in self.tuples.items():
                val_to_check = tuple_v[i]
                if conditions[i] == '>':
                    if val_to_check > values[i]:
                        attr_dict[statement].add(tuple_k)
                elif conditions[i] == '<':
                    if val_to_check < values[i]:
                        attr_dict[statement].add(tuple_k)
                elif conditions[i] == '<>':
                    if val_to_check != values[i]:
                        attr_dict[statement].add(tuple_k)
                elif conditions[i] == '==':
                    if val_to_check == values[i]:
                        attr_dict[statement].add(tuple_k)
                else:
                    print("Incorrect condition, must be one of: <, >, <>, or == ")
        return attr_dict
