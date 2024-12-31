from node import Node
class AVLTree:
    def __init__(self, compare_function):
        self.root = None
        self.size = 0
        self.comparator = compare_function

    def get_height(self, node):
        if not node:
            return 0
        height_value = node.height
        return height_value

    def update_height(self, node):
        if node:
            left_height = self.get_height(node.left)
            right_height = self.get_height(node.right)
            node.height = 1 + max(left_height, right_height)

    def get_balance(self, node):
        if not node:
            return 0
        left_height = self.get_height(node.left)  # Get the height of the left subtree
        right_height = self.get_height(node.right)  # Get the height of the right subtree
        balance_value = left_height - right_height
        return balance_value

    def rotate_right(self, current_node):
        left_child = current_node.left  # Store the left child of the current node
        current_node.left = left_child.right  # Move the right subtree of the left child to the left of the current node
        if left_child.right:
            left_child.right.parent = current_node  # Update the parent of the moved subtree
        left_child.right = current_node
        left_child.parent = current_node.parent
        if current_node.parent:
            if current_node.parent.left == current_node:
                current_node.parent.left = left_child  # Update the parent's left pointer
            else:
                current_node.parent.right = left_child  # Update the parent's right pointer
        current_node.parent = left_child  # Update the parent of the current node
        self.update_height(current_node)
        self.update_height(left_child)
        return left_child

    def rotate_left(self, current_node):
        right_child = current_node.right  # Store the right child of the current node
        current_node.right = right_child.left  # Move the left subtree of the right child to the right of the current node
        if right_child.left:
            right_child.left.parent = current_node  # Update the parent of the moved subtree
        right_child.left = current_node
        right_child.parent = current_node.parent
        if current_node.parent:
            if current_node.parent.left == current_node:
                current_node.parent.left = right_child  # Update the parent's left pointer
            else:
                current_node.parent.right = right_child  # Update the parent's right pointer
        current_node.parent = right_child  # Update the parent of the current node
        self.update_height(current_node)
        self.update_height(right_child)
        return right_child

    def rebalance(self, node):
        self.update_height(node)
        balance_factor = self.get_balance(node)
        if balance_factor > 1:
            if self.get_balance(node.left) < 0:
                node.left = self.rotate_left(node.left)  # Perform left rotation if left subtree is unbalanced
            return self.rotate_right(node)
        if balance_factor < -1:
            if self.get_balance(node.right) > 0:
                node.right = self.rotate_right(node.right)  # Perform right rotation if right subtree is unbalanced
            return self.rotate_left(node)
        return node

    def insert_node(self, value):
        new_node = Node(value)
        self.root = self._insert(self.root, new_node)
        self.size += 1

    def _insert(self, current_root, new_node):
        if not current_root:
            return new_node
        comparison_result = self.comparator(new_node.obj, current_root.obj)
        if comparison_result < 0:
            current_root.left = self._insert(current_root.left, new_node)  # Insert in the left subtree if smaller
            current_root.left.parent = current_root
        else:
            current_root.right = self._insert(current_root.right, new_node)  # Insert in the right subtree if larger
            current_root.right.parent = current_root
        return self.rebalance(current_root)

    def find_minimum(self, subtree_root):
        current_node = subtree_root
        while current_node.left:
            current_node = current_node.left  # Move to the leftmost node (smallest value)
        return current_node

    def find_maximum(self, subtree_root):
        current_node = subtree_root
        while current_node.right:
            current_node = current_node.right  # Move to the rightmost node (largest value)
        return current_node

    def delete_node(self, value):
        self.root = self._delete(self.root, value)
        self.size -= 1

    def _delete(self, current_root, value):
        if not current_root:
            return current_root  # Return None if node to delete is not found
        comparison_result = self.comparator(value, current_root.obj)  # Compare the value with the current node
        if comparison_result < 0:
            current_root.left = self._delete(current_root.left, value)  # Search the left subtree if value is smaller
        elif comparison_result > 0:
            current_root.right = self._delete(current_root.right, value)  # Search the right subtree if value is larger
        else:
            if not current_root.left:
                temp_node = current_root.right
                return temp_node
            elif not current_root.right:
                temp_node = current_root.left
                return temp_node
            temp_node = self.find_minimum(current_root.right)
            current_root.obj = temp_node.obj  # Replace current node's value with the successor's value
            current_root.right = self._delete(current_root.right, temp_node.obj)  # Delete the successor node
        if current_root is None:
            return current_root
        return self.rebalance(current_root)

    def inorder_traversal(self, node, result=None):
        if result is None:
            result = []
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.obj)
            self.inorder_traversal(node.right, result)
        return result
