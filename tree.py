from collections import deque


class TreeNode():
    """
    TreeNode class represents binary tree node
    """

    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        """
        It is a good practice to represent define repr as something
        that can recreate the object, i.e. we can recreate this object
        from return value of repr function
        """
        return f'TreeNode({self.value}, {self.left}, {self.right})'

    def __str__(self):
        return f'{self.value}'


class BinaryTree():
    """
    Represents a binary tree and methods on them.
    TODO:
    """

    def __init__(self, root=None):
        self.root = root

    def insert(self, node):
        #TODO
        root_node = self.root

    def iterative_in_order(self):
        current = self.root
        if not current:
            # note: this is pythonic way to keep the function
            # return a generator while still returning nothing
            # https://stackoverflow.com/questions/13243766/python-empty-generator-function
            return
            yield
        stack = []
        while stack or current:
            # go as left as possible from root
            # and keep adding nodes found
            if current:
                stack.append(current)
                # if there is no left child,
                # current will be None
                # that's when we go to else branch and pop
                current = current.left
            else:
                yield stack.pop()
                current = current.right

    def iterative_pre_order(self):
        current = self.root
        if not current:
            # https://stackoverflow.com/questions/13243766/python-empty-generator-function
            return
            yield
        stack = [current]  # for pre-order, we need to print the root first
        # so we will just pop and add it in our result
        while stack:
            # as opposed to inorder, we will ensure that the current node
            # is always non-empty
            current = stack.pop()
            yield current
            # push right child first so that left is popped before it
            if current.right:
                stack.append(current.right)
            if current.left:
                stack.append(current.left)

    def iterative_post_order(self):
        current = self.root
        if not current:
            return
            yield
        stack = []
        last_visited_node = None
        while current or stack:
            if current:
                stack.append(current)
                current = current.left
            else:
                # post-order, so we don't want to visit root just yet
                # we will visit its children first
                peek_node = stack[-1]
                # right child may have a subtree of its own
                # and since we are visiting right child before parent,
                # it's possible that we might hit the right child again
                # the second if condition avoids looking at the right child
                # all over again
                if peek_node.right and peek_node.right != last_visited_node:
                    current = peek_node.right
                else:
                    last_visited_node = stack.pop()
                    yield last_visited_node

    def level_order(self):
        # straightforward BFS
        current = self.root
        if not current:
            return
            yield
        queue = deque()
        queue.append(current)
        while queue:
            current = queue.popleft()
            yield current
            children = []
            if current.left:
                children.append(current.left)
            if current.right:
                children.append(current.right)
            queue.extend(children)

    def morris_in_order_traversal(self):
        # https://en.wikipedia.org/wiki/Threaded_binary_tree
        # All the previous traversals use extra space (stack or deque)
        # For systems with limited memory, it might be useful to traverse
        # tree without extra space
        current = self.root
        if not current:
            return
            yield
        while current:
            if current.left:
                # we first create links from a node's predecessor to it
                pre = current.left
                # find the predecessor
                while pre.right and pre.right != current:
                    pre = pre.right

                if not pre.right:
                    # we haven't created the link from predecessor to
                    # node, create it
                    pre.right = current
                    current = current.left
                else:
                    yield current
                    current = current.right
                    # node and left subtree is visited, so remove the link
                    # from predecessor
                    pre.right = None
            else:
                yield current
                current = current.right


if __name__ == "__main__":
    a = TreeNode('a')
    b = TreeNode('b')
    c = TreeNode('c')
    d = TreeNode('d')
    e = TreeNode('e')
    f = TreeNode('f')
    g = TreeNode('g')

    b.left = d
    b.right = e

    c.left = f
    c.right = g

    a.left = b
    a.right = c
    tree = BinaryTree(a)

    # print("In order", tree.iterative_in_order())
    # print("Pre order", tree.iterative_pre_order())
    # print("Post order", tree.iterative_post_order())
    # print("Level order", tree.level_order())
    print("Morris in-order", tree.morris_traversal())
    # print(tree)
