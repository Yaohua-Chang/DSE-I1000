class Table:
    # Table class

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, name, attributes, delimiter = "->"):
        """Update"""
        self.name = name
        self.attributes = attributes
        self.master_key = ""
        self.keys = set()
        self.superkeys = set()
        self.fds = []
        self.mvds = []
        self.delimiter = delimiter
        self.left_list = []
        self.right_list = []
        self.nf = ""
        self.attributes_names = []

        for attr in attributes:
            self.attributes_names.append(attr.name)

    #########
    # PRINT #
    #########

    def print_attributes(self):
        print("The table named: ", self.name, " has attributes:")
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

    def add_fd(self, fd_split):

        left_set = set()
        left = list(filter(None,fd_split[0].split(" ")))
        for attr in left:
            left_set.add(attr)
        right_set = set()
        right = list(filter(None,fd_split[1].split(" ")))
        for attr in right:
            right_set.add(attr)

        # check the invalid input
        if len(fd_split) != 2:
            return "This is invalid input."

        # check the wrong FD
        if (not left_set.issubset(self.attributes_names)) or (not right_set.issubset(self.attributes_names)):
            return "This is wrong FD. There is no such attribute in the table"

        # remove the trivial FD
        if right_set.issubset(left_set):
            return "This is trivial FD"
        
        # Check whether FD already existed
        if fd in self.fds:                    
            return "This fd has existed in the table"
        
        # Update FDs and convert those FDs not in the standard non-trivial forms to standard non-trival forms
        if len(right_set) != 1:
            for element in right_set:
                fd = ' '.join(attr for attr in left) + "->" + element
                self.fds.append(fd)
        else:
            fd = ' '.join(attr for attr in left) + "->" + ' '.join(attr2 for attr2 in right)
            self.fds.append(fd)

        
        
        #Update right_list and left_list?
        """Update"""

        # add mvd that is implied from this fd
        implied_mvd = fd_split[0] + "->->" + fd_split[1]
        self.mvds.append(implied_mvd)
             
        fd = ' '.join(attr for attr in left) + "->" + ' '.join(attr2 for attr2 in right)
        
        self.fds = sorted(set(fds))
        
        return "Added a new fd successfully! " + fd
    
    
    def remove_fd(self, fd_split):
        fd_to_rm = fd_split[0] + "->" + fd_split[1]
        tmp_fds = [fd for fd in self.fds if fd != fd_to_rm]
        self.fds = tmp_fds
        return "The fd: " + fd + " was successfully removed."

    def add_mvd(self, mvd_split):
        """Update"""

        left_set = set()
        left_set.add(fd_split[0])
        right_set = set()
        right_set.add(fd_split[1])

        # check defining mvd for table of 2 attr
        if len(self.attributes <= 2):
            return "MVD trivial for a table with <= 2 attributes"
        # check invalid input
        if len(mvd_split) != 2:
            return "This is invalid input."
        # check attr not in table
        if not left_set.issubset(self.attributes_names) or not right_set.issubset(self.attributes_names):
            return "This is wrong FD. There is no all attributes of FD in the table"
        # remove trivial mvd
        if right_set.issubset(left_set):
            return "This is a trivial mvd"

        mvd = mvd_split[0] + "->->" + mvd_split[1]
        self.mvds.append(mvd)

        return "Added a new mvd successfully: " + mvd

    def add_boolean_conditions(self, input_str):
        if "<" in input_str:
            input_split = input_str.replace(" ","").split('<')
            if len(input_split) != 2:
                return "This is invaild input."
            else:
                if not input_split[0] in self.attributes_names:
                    return "There is no attribute in the table"
                else:
                    for attr in self.attributes:
                        if attr.name == input_split[0]:
                            less_than_value = int(input_split[1])
                            if attr.more_than_value != None: 
                                if less_than_value > attr.more_than_value:
                                    attr.set_less_than_value(less_than_value)
                                    return "Add boolean conditions -- successfully"
                                else:
                                    return "This is conflicting Boolean conditions"
                            else:
                                attr.set_less_than_value(less_than_value)
                                return "Add boolean conditions -- successfully"
        elif ">" in input_str:
            input_split = input_str.replace(" ","").split('>')
            if len(input_split)!=2:
                return "This is invaild input."
            else:
                if not input_split[0] in self.attributes_names:
                    return "There is no attribute in the table"
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

    ########
    # FD'S #
    ########
    def fd_split(self, fds):
        """Update"""
        for fd in self.fds:
            fd_split = fd.split("->")
            self.left_list.append(fd_split[0])
            self.right_list.append(fd_split[1])

    # Right now, can only add fd's once because not checking for duplicates when
    # pushing into self.fds at the end
    def add_fds(self, fd_str):
        """Update"""

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
        """Update"""

        for fd in self.fds:
            fd_split = fd.split("->")
            self.left_list.append(fd_split[0])
            self.right_list.append(fd_split[1])

        seed = attr

        outputs = set(seed)
        count_fds = len(self.left_list)

        # to compute closure of the seed
        for _ in range(count_fds):
            for index in range(count_fds):
                if set(self.left_list[index]).issubset(outputs):
                    outputs.add(self.right_list[index])
        return outputs

    def get_closure(self):
        """Update"""
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
        """Update"""
        keys = set()
        print(self.left_list)
        for seed in self.left_list:
            outputs =  set(seed)
            count_fds = len(self.left_list)

            # to compute closure of each seed
            for _ in range(count_fds):
                for index in range(count_fds):
                    if set(self.left_list[index]).issubset(outputs):
                        outputs.add(self.right_list[index])

            diff_attrs_outputs = set(self.attributes).difference(outputs)
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

    ################
    # NORMAL FORMS #
    ################

    def determine_1NF(self):
        """Update"""
        for key in self.keys:
            for lhs in self.left_list:
                if set(lhs).issubset(set(key)) and set(lhs) != set(key):
                    return True
        return False

    def determine_2NF(self):
        """Update"""
        non_prime_attrs = set(self.attributes)
        for key in self.keys:
            non_prime_attrs -= set(key)

        for i in range(len(self.left_list)) :
            if set(self.left_list[i]).issubset(non_prime_attrs) and set(self.right_list[i]).issubset(non_prime_attrs):
                return True
        return False

    def determine_3NF(self):
        """Update"""
        for key in self.keys:
            for i in range(len(self.right_list)) :
                # for a dependency A → B, A cannot be a non-prime attribute, if B is a prime attribute.
                if set(right_list[i]).issubset(key) and not set(left_list[i]).issubset(key):
                    return True
        return False

    def get_normal_form(self):
        """Update"""

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
