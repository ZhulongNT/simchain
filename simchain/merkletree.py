from .ecc import sha256d

class Node(object):
    """
    Merkle tree node. Holds value, child/parent pointers, and sibling info.
    """
    def __init__(self, data, prehashed=False):
        """
        Initialize a node.
        Args:
            data: bytes, raw or hashed value
            prehashed: bool, if True, data is already hashed
        """
        if prehashed:
            self.val = data
        else:
            self.val = sha256d(data)
        self.left_child = None
        self.right_child = None
        self.parent = None
        self.bro = None
        self.side = None

    def __repr__(self):
        """
        String representation for debugging.
        """
        return "MerkleTreeNode('{0}')".format(self.val)

class MerkleTree(object):
    """
    Merkle tree structure. Supports root calculation and path generation.
    """
    def __init__(self,leaves = []):
        """
        Initialize MerkleTree.
        Args:
            leaves: list of bytes, already hashed
        """
        self.leaves = [Node(leaf,True) for leaf in leaves]
        self.root = None

    def add_node(self,leaf):
        """
        Add a new leaf node (raw data).
        Args:
            leaf: bytes
        """
        self.leaves.append(Node(leaf))

    def clear(self):
        """
        Clear tree structure, keep leaves only.
        """
        self.root = None
        for leaf in self.leaves:
            leaf.parent,leaf.bro,leaf.side = (None,)*3

    def get_root(self):
        """
        Calculate and return Merkle tree root hash.
        Returns:
            bytes: root hash
        """
        if not self.leaves:
            return None
        level = self.leaves[::]
        # Merge up until only one root node remains
        while len(level) != 1:
            level = self._build_new_level(level)
        self.root = level[0]
        return self.root.val

    def _build_new_level(self, leaves):
        """
        Build parent level from current leaves.
        Args:
            leaves: list of Node
        Returns:
            list of Node
        """
        new, odd = [], None
        if len(leaves) % 2 == 1:
            # Odd number, last node promoted
            odd = leaves.pop(-1)
        for i in range(0, len(leaves), 2):
            # Merge left and right node, create parent
            newnode = Node(leaves[i].val + leaves[i + 1].val)
            newnode.left_child, newnode.right_child = leaves[i], leaves[i + 1]  # fix typo
            leaves[i].side, leaves[i + 1].side = 'LEFT', 'RIGHT'
            leaves[i].parent, leaves[i + 1].parent = newnode, newnode
            leaves[i].bro, leaves[i + 1].bro = leaves[i + 1], leaves[i]
            new.append(newnode)
        if odd:
            new.append(odd)
        return new

    def get_path(self, index):
        """
        Get path from leaf to root for proof.
        Args:
            index: int, leaf index
        Returns:
            list of (hash, side)
        """
        path = []
        this = self.leaves[index]
        path.append((this.val, 'SELF'))
        while this.parent:
            path.append((this.bro.val, this.bro.side))
            this = this.parent
        path.append((this.val, 'ROOT'))
        return path



