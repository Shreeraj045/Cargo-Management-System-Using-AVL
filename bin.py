from avl import AVLTree
from object import Object

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.avl_cargo = AVLTree(self.comp_func_for_object)

    def add_object(self, obj):
        self.avl_cargo.insert_node(obj)
        self.capacity -= obj.size

    def remove_object(self, obj_id):
        current_node = self.avl_cargo.root
        while True:
            if obj_id > current_node.obj.object_id:
                current_node = current_node.right
            elif obj_id < current_node.obj.object_id:
                current_node = current_node.left
            else:
                break
        if current_node != None:
            self.capacity += current_node.obj.size
            self.avl_cargo.delete_node(current_node.obj)

    def comp_func_for_object(self, cargo1: Object, cargo2: Object):
        return cargo1.object_id - cargo2.object_id

