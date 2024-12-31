from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException
from node import Node


class GCMS:
    def __init__(self):
        self.avl_cargo = AVLTree(self.comp_1)
        self.avl_tree_bin = AVLTree(self.comp_2)
        self.avl_bin_id = AVLTree(self.comp_3)
        self.avl_bin_inverse = AVLTree(self.comp_4)
    def comp_1(self, cargo1: Object, cargo2: Object):
        return cargo1.object_id - cargo2.object_id

    def comp_2(self, bin1: Bin, bin2: Bin):
        # Ascending order for bin_id
        capacity_diff = bin1.capacity - bin2.capacity
        if capacity_diff != 0:
            return capacity_diff
        return bin1.bin_id - bin2.bin_id

    def comp_3(self, bin1: Bin, bin2: Bin):
        return bin1.bin_id - bin2.bin_id

    def comp_4(self,bin1:Bin , bin2:Bin):
        # Descending order for bin_id
        capacity_diff = bin1.capacity - bin2.capacity
        if capacity_diff != 0:
            return capacity_diff
        return bin2.bin_id - bin1.bin_id

    def add_bin(self, bin_id, capacity):
        bin1 = Bin(bin_id, capacity)
        self.avl_tree_bin.insert_node(bin1)
        self.avl_bin_inverse.insert_node(bin1)
        self.avl_bin_id.insert_node(bin1)
    def add_object(self, object_id, size, color):
        new_cargo = Object(object_id, size, color)    # create new_object with given data
        self.avl_cargo.insert_node(new_cargo)         # insert this node in the avl tree having cargos

        # This is for Red Color Cargo adding
        if color == Color.RED:
            largest_bin = self.avl_bin_inverse.root    # initialize with root osf Reverse AVL tree of bin
            while largest_bin.right is not None:       # While loop finds right most node and hence the bin at right end i.e largest
                largest_bin = largest_bin.right
            if largest_bin.obj.capacity < new_cargo.size:  # check if bin can accomodate the object we are trying to add
                raise NoBinFoundException
            target_bin = largest_bin.obj    #target set to the found bin

        # This is for Blue Color Cargo adding
        elif color == Color.BLUE:
            least_id_compact = self.avl_tree_bin.root       # initialize with root of AVL Tree .
            closest_bin = None                              # make the final bin to found as None
            while least_id_compact is not None:             # While loop runs till lead_id_comp doesn't become None
                if least_id_compact.obj.capacity < new_cargo.size:
                    least_id_compact = least_id_compact.right
                else:
                    closest_bin = least_id_compact
                    least_id_compact = least_id_compact.left
            if closest_bin is None:  raise NoBinFoundException         # raise Exception when no such bin found
            target_bin = closest_bin.obj

        # This is for Yellow Color Cargo adding (same as Blue Color Cargo just within inverse avl tree)
        elif color == Color.YELLOW:
            current_node = self.avl_bin_inverse.root    # initialize with root of inverse AVL Tree bin
            best_fit = None                             # initialize the final node to be found by None
            while current_node is not None:             # While loop indirectly search the AVL tree for given bin Cap.
                if current_node.obj.capacity < new_cargo.size:
                    current_node = current_node.right
                else:
                    best_fit = current_node
                    current_node = current_node.left
            if best_fit is None: raise NoBinFoundException            # raise Exception when no such bin found
            target_bin = best_fit.obj

        # This is for Green Color Cargo adding (same as Red Color Cargo just within inverse avl tree)
        elif color == Color.GREEN:
            largest_bin = self.avl_tree_bin.root            # initialize with root osf Reverse AVL tree of bin
            while largest_bin.right is not None: largest_bin = largest_bin.right          # While loop finds right most node and hence the bin at right end i.e largest cap largest id
            if largest_bin.obj.capacity < new_cargo.size: raise NoBinFoundException  # check if bin can accomodate the object we are trying to add
            target_bin = largest_bin.obj                    #target set to found bin

        else:
            raise NoBinFoundException

        # Assign bin ID and update trees regardless of color
        new_cargo.bin_id = target_bin.bin_id
        self.avl_tree_bin.delete_node(target_bin)
        self.avl_bin_inverse.delete_node(target_bin)
        target_bin.add_object(new_cargo)
        self.avl_tree_bin.insert_node(target_bin)
        self.avl_bin_inverse.insert_node(target_bin)

    def delete_object(self, object_id):
        current_node = self.avl_cargo.root                  # start with root of object tree
        while current_node is not None:                     # check for matching object_id i.e cargo id
            if object_id < current_node.obj.object_id: current_node = current_node.left
            elif object_id == current_node.obj.object_id:  break
            else: current_node = current_node.right
        if current_node is None: return None                 #break if current Node is None i.e no object found with same id

        bin_id = current_node.obj.bin_id # extract bin id
        current_node.obj.bin_id = None
        bin_node = self.avl_bin_id.root                     #initialise with root of bin_id_avl tree
        while bin_node is not None:                         #while loop for finding bin having bin id found earlier
            if bin_id == None : return None
            if bin_id > bin_node.obj.bin_id: bin_node = bin_node.right
            elif bin_id == bin_node.obj.bin_id: break
            else: bin_node = bin_node.left
        temp = bin_node.obj                                 # else similar to logic of adding object to bin just remove here
        self.avl_tree_bin.delete_node(temp)
        self.avl_bin_inverse.delete_node(temp)
        temp.remove_object(current_node.obj.object_id)
        self.avl_tree_bin.insert_node(temp)
        self.avl_bin_inverse.insert_node(temp)

    def bin_info(self, bin_id):
        bin_node = self.avl_bin_id.root                      # find the bin with help of search from avl tree of bin arranged according to id's
        while bin_node is not None:                          # search implemented here
            if bin_id > bin_node.obj.bin_id: bin_node = bin_node.right
            elif bin_id == bin_node.obj.bin_id: break
            else: bin_node = bin_node.left
        if bin_node is None: raise NoBinFoundException        # if bin not found with bin id return None

        cargo_tree_root = bin_node.obj.avl_cargo.root         # initiate with root of avl_cargo
        object_list = []                                      # make a empty list to return at end in which obj will get added
        for i in self.avl_cargo.inorder_traversal(cargo_tree_root):
            object_list.append(i.object_id)
        return tuple([bin_node.obj.capacity, object_list])

    def object_info(self, object_id):
        temp = self.avl_cargo.root
        while temp!=None:
            if temp.obj.object_id < object_id:
                temp = temp.right
            elif temp.obj.object_id > object_id:
                temp = temp.left
            else:
                return temp.obj.bin_id