
N = 4


class Nodes:  # using node class to organize the number collection for Futo game
    def __init__(self, grid, data):
        self.grid = grid
        self.data = data
        self.length = 0
        self.down = None
        self.right = None


def generate_futo_puzzle(n):  # generating the Futo puzzle items
    node_list = []
    value_list = []
    for i in range(1, n+1):
        value_list.append(i)
    for i in range(1, n+1):
        for j in range(1, n+1):
            new = Nodes((i, j), value_list)
            node_list.append(new)
            print(str(new.grid) + "generated")
            if new.grid[1] == 1:
                pass
            else:
                current.down = new
                print(str(current.grid) + " down connect to  " + str(new.grid))
            current = new
    for i in range(len(node_list)):
        if node_list[i].grid[0] == 1:
            new = node_list[i]
            if new.grid[1] == 1:
                pass
            else:
                current.right = new
                print(str(current.grid) + " right connect to  " + str(new.grid))
            current = new
    return node_list


def remove_item(item_list, x):  # a useful tool to remove item in the value list
    temp = []
    for i in range(len(item_list)):
        if item_list[i] == x:
            pass
        else:
            temp.append(item_list[i])
    return temp


def get_node(node_list, position):  # return node by searching the link
    x, y = position
    current = node_list[0]
    a, b = current.grid
    if x is a and y is b:
        return current
    while current is not None:
        if current.down is not None:
            current = current.down
        if current.right is not None:
            current = current.right
    return "Node not found"


def pre_set(node_list, node):  # pre set the fixed number into the Futo board
    x, y, z = node
    for i in range(len(node_list)):
        if node_list[i].grid[0] == x:  # remove z item from y column
            if node_list[i].grid[1] == y:
                node_list[i].data = [z]
            else:
                node_list[i].data = remove_item(node_list[i].data, z)
        if node_list[i].grid[1] == y:  # remove z item from x row
            if node_list[i].grid[0] == x:
                pass
            else:
                node_list[i].data = remove_item(node_list[i].data, z)
    return node_list


def less_than_set(node_list, position):  # less than set to the inequality constraint
    x, y = position
    for i in range(len(node_list)):
        if node_list[i].grid[0] == x and node_list[i].grid[1] == y:
            node_list[i].data = remove_item(node_list[i].data, 4)
    return node_list


def more_than_set(node_list, position):  # more than set to the inequality constraint
    x, y = position
    for i in range(len(node_list)):
        if node_list[i].grid[0] == x and node_list[i].grid[1] == y:
            node_list[i].data = remove_item(node_list[i].data, 1)
    return node_list


def print_list(node_list):  # print function
    print("----")
    for i in range(len(node_list)):
        print(node_list[i].grid, node_list[i].length, node_list[i].data)
    print("----")


def update_domain_length(node_list):  # update the domain length for each variable
    for i in range(len(node_list)):
        space = len(node_list[i].data)
        node_list[i].length = space
    return node_list


def arc_consistency_constraints(node_list, node):  # arc consistency to check if one value from a variable is valid
    temp_list = []
    for i in range(len(node_list)):
        grid = node_list[i].grid
        data = node_list[i].data
        new = Nodes(grid, data)
        new.length = node_list[i].length
        temp_list.append(new)
    a, b, c = node
    for i in range(len(temp_list)):
        x, y = temp_list[i].grid
        if x == a:  # check arc with x column
            if y == b:
                temp_list[i].data = [c]
            else:
                temp_list[i].data = remove_item(temp_list[i].data, c)
        if y == b:  # check arc with y row
            if x == a:
                pass
            else:
                temp_list[i].data = remove_item(temp_list[i].data, c)
    temp_list = update_domain_length(temp_list)
    violated = checking_consistency_empty(temp_list)
    print_list(temp_list)
    if violated is True:
        return False, str(node) + " arc consistency checking this is not valid"
    else:
        return True, str(node) + " arc consistency checking this is valid"


def backtracking(node_list):  # backtracking to use for loop checking one round each item value consistency
    for i in range(len(node_list)):
        x, y = node_list[i].grid
        queue = node_list[i].data
        value = []
        if len(queue) > 1:
            while len(queue) != 0:
                z = queue.pop(0)
                valid, arc = arc_consistency_constraints(node_list, (x, y, z))
                if valid is True:
                    value.append(z)
                print(valid, arc)
                print_list(node_list)
            node_list[i].data = value
            node_list = update_domain_length(node_list)
            print("update " + str(node_list[i].grid) + " " + str(node_list[i].length) + " " + str(node_list[i].data))
    return node_list


def recursive_backtracking(node_list):  # recursive run backtracking until the each item has only one value
    count = 0
    completed = False
    while completed is False:
        count += 1
        print("round counting for backtracking: ", count)
        node_list = update_domain_length(node_list)
        completed = checking_completed(node_list)
        backtracking(node_list)
    return node_list


def checking_consistency_empty(node_list):  # function to check the consistency if the value list is empty
    for i in range(len(node_list)):
        if node_list[i].length == 0:
            return True
    return False


def checking_completed(node_list):  # function to check if the node list consistency is completed
    for i in range(len(node_list)):
        if node_list[i].length > 1:
            return False
    return True


# based on the set of the Futo game to work

net = generate_futo_puzzle(N)
net = pre_set(net, (3, 4, 2))
net = pre_set(net, (4, 3, 3))
net = pre_set(net, (2, 3, 1))
net = pre_set(net, (3, 3, 4))
net = update_domain_length(net)
print("pre set:")
print_list(net)
net = less_than_set(net, (1, 1))
net = less_than_set(net, (3, 1))
net = less_than_set(net, (4, 1))
net = less_than_set(net, (2, 3))
net = more_than_set(net, (2, 1))
net = more_than_set(net, (2, 2))
net = more_than_set(net, (3, 2))
net = more_than_set(net, (4, 2))
net = more_than_set(net, (2, 4))
net = update_domain_length(net)
print("inequality: ")
print_list(net)
net = recursive_backtracking(net)
print("backtracking: ")
print_list(net)