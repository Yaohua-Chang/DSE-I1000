class Table:

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, db, name, attributes, delimiter = "->"):
        self.name = name
        self.attributes = sorted(attributes)
        self.attributes_names = set([a.name for a in attributes])
        self.master_key = ""
        self.keys = set()
        self.superkeys = set()
        self.fds = []
        self.mvds = []
        self.delimiter = delimiter
        self.seen_fd = set()
        self.nf = ""
        self.tuples = {}
        self.parent_database = db  # need reference to Database object for foreign keys

    #########
    # PRINT #
    #########

    def print_attributes(self):
        print("The table named: ", self.name, "\nHas attributes:")
        for attr in self.attributes:
            print(attr.name , "  " + attr.type, end = '\n')

    def print_fds(self):
        print("The table named: ", self.name, "\nHas FD's: ", self.fds)

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

    # do we handle case of decomposition, i.e. AB->CD becomes AB->C & AB->D
    def add_fd(self, fd):

        try:
            lhs, rhs = fd.split(self.delimiter)
        except ValueError:  # if can't split & unpack into 2 separate values
            print("Must have a LHS & RHS!")
            return False

        # check for attributes not in table
        if not set(lhs).issubset(self.attributes_names) or not set(rhs).issubset(self.attributes_names):
            return "This is wrong FD. There is no all attributes of FD in the table"

        # remove trivial FDs
        if set(rhs).issubset(set(lhs)):
            return "This is trivial FD"

        # add fd
        if fd not in self.seen_fd:
            self.fds.append(lhs + self.delimiter + rhs)
            self.seen_fd.add(fd)
        else:
            print("The fd: " + fd + " has already been added!")
            return False

        # add mvd that is implied from this fd
        self.mvds.append(lhs + "->->" + rhs)

        print("Added a new fd successfully: " + fd)
        return True

    def remove_fd(self, fd_to_rm):
        tmp_fds = [fd for fd in self.fds if fd != fd_to_rm]
        self.fds = tmp_fds
        return "The fd: " + fd_to_rm + " was successfully removed."

    def add_mvd(self, mvd_split):

        try:
            lhs, rhs = fd.split("->->")
        except ValueError:  # if can't split & unpack into 2 separate values
            print("Must have a LHS & RHS!")
            return False

        # check defining mvd for table of 2 attr
        if len(self.attributes) <= 2:
            return "MVD trivial for a table with <= 2 attributes"
        # check attr not in table
        if not lhs.issubset(self.attributes_names) or not rhs.issubset(self.attributes_names):
            return "This is wrong MVD. There is no all attributes of MVD in the table"
        # remove trivial mvd
        if rhs.issubset(lhs):
            return "This is a trivial mvd"

        self.mvds.append(lhs + "->->" + rhs)

        return "Added a new mvd successfully: " + mvd

    def add_boolean_conditions(self, input_str):
        if "<" in input_str:
            input_split = input_str.replace(" ","").split('<')
            if len(input_split) != 2:
                return "This is invaild input."
            else:
                if not input_split[0] in self.attributes_names:
                    return "There is no the attribute in the table"
                else:
                    for attr in self.attributes:
                        if attr.name == input_split[0]:
                            less_than_value = int(input_split[1])
                            if attr.more_than_value == None:
                                attr.set_less_than_value(less_than_value)
                                return "Add boolean conditions successfully"
                            elif less_than_value > attr.more_than_value:
                                attr.set_less_than_value(less_than_value)
                                return "Add boolean conditions successfully"
                            else:
                                return "This is conflicting Boolean conditions"
        elif ">" in input_str:
            input_split = input_str.replace(" ","").split('>')
            if len(input_split)!=2:
                return "This is invaild input."
            else:
                if not input_split[0] in self.attributes_names:
                    return "There is no the attribute in the table"
                else:
                    for attr in self.attributes:
                        if attr.name == input_split[0]:
                            more_than_value = int(input_split[1])
                            if attr.less_than_value == None:
                                attr.set_more_than_value(more_than_value)
                                return "Add boolean conditions successfully"
                            elif more_than_value < attr.less_than_value:
                                attr.set_more_than_value(more_than_value)
                                return "Add boolean conditions successfully"
                            else:
                                return "This is conflicting Boolean conditions"

    ########
    # FD'S #
    ########

    # this function can be removed (no need to use in any above functions; I removed it from up there)
    def fd_split(self, fds):
        for fd in self.fds:
            fd_split = fd.split("->")
            self.left_list.append(fd_split[0])
            self.right_list.append(fd_split[1])

    # this is redundant, should be handled by DBMS_system
    # my take: any interface type functions can be handled by DBMS system which calls Table class methods
    # like add_fd one at a time (or until user quits)
    # same is true of get_closure below which I think we can delete
    def add_fds(self, fd_str):

        fds = fd_str.replace(" ", "").split(",")

        # All trivial FDs, such as AB->B, and wrong FDs, are identified and ignored
        fds_copy = fds.copy()
        for fd in fds_copy:
            fd_split = fd.split("->")
            # remove wrong FD
            if len(fd_split) != 2:
                fds.remove(fd)
                continue;

            left_set = set(fd_split[0])
            right_set = set(fd_split[1])
            # remove the wrong FD
            if not left_set.issubset(self.attributes) or not right_set.issubset(self.attributes):
                fds.remove(fd)
                continue;
            # remove the trivial FD
            if right_set.issubset(left_set):
                fds.remove(fd)
                continue;

            # Convert those FDs not in the standard non-trivial forms to standard non-trival forms
            if len(right_set) != 1:
                for element in right_set:
                    fds.append(fd_split[0] + "->" + element)
                fds.remove(fd)
        # Repeated FDs are identified and ignored
        self.fds = sorted(set(fds))
        self.fd_split(self.fds)
        return self.fds

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

    # this is redundant; can be handled by DBMS
    # see add_fds for more
    def get_closure(self):
        while True:
            seed = input("Please type any set of attributes as the seed(or input quit to stop):")
            if seed == "quit":
                break
            c = self.closure(seed)
            print("The closure of {} is {}".format(sorted(set(seed)), sorted(c)))

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

            diff_attrs_outputs = set(self.attributes_names).difference(outputs)
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
        print("All keys for this table are : ", str(self.keys))

    def user_define_key(self, k):
        valid_key = k in self.keys
        while not valid_key:
            print("Unfortunately that's not a viable key. Here are you options:\n" + str(table.keys))
            k = input("Try a different key: ")
            valid_key = k in self.keys
        print("Great selection! " + k + " is a viable key")
        table.master_key = k

    ################
    # NORMAL FORMS #
    ################

    def determine_1NF(self):
        for key in self.keys:
            for lhs in self.left_list:
                if set(lhs).issubset(set(key)) and set(lhs) != set(key):
                    return True
        return False

    def determine_2NF(self):
        non_prime_attrs = set(self.attributes)
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
                if set(right_list[i]).issubset(key) and not set(left_list[i]).issubset(key):
                    return True
        return False

    def get_normal_form(self):

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
    def add_tuple(t):
        # need a master key before beginning to add tuples
        if self.master_key == "":
            self.user_define_key()

        # pick out the master key from the input tuple
        k = ""
        for i, c in enumerate(self.attributes_names):
            if c in self.master_key:
                k += t[i]

        # check FD consistency
        for fd in self.fds:
            lhs, rhs = fd.split("->")
            idx_lhs = self.attributes_names.index(lhs)
            idx_rhs = self.attributes_names.index(rhs)

            # iterate over other tuples in table and check for consistency
            dict_check = {}
            for tuple in self.tuples:
                # pull out rhs & lhs from each tuple
                lhs_value = tuple[idx_lhs:(idx_lhs + len(lhs))]
                rhs_value = tuple[idx_rhs:(idx_rhs + len(rhs))]
                # the lhs_value is already in the table; now we can check if consistency remains
                if lhs_value in dict_check:
                    dict_check[lhs_value] = set()
                    dict_check[lhs_value].add(rhs_value)
                else:
                    dict_check[lhs_value].add(rhs_value)
                    # if any set has more than one object it implies RHS -> LHS has been violated
                    # b/c RHS points to 2 distinct values of LHS
                    if len(dict_check[lhs_value]) > 1:
                        print("This breaks the consistency implied by the FD: " + fd)
                        return False

        # check for foreign key
        # for table_name in self.parent_database.tables.keys():

        # add tuple
        self.tuples[k] = t

        return True
