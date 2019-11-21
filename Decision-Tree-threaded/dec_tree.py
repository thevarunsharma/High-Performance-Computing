import numpy as np
import threading

def create_subtree(X, Y, A, children, v):
    children[v] = ID3DecisionTree(X, Y, A)

class Node:
    def __init__(self):
        """
        A node can have either a value (i.e. leaf node) or an attribute (i.e. decision node)
        """
        self.attr = None
        self.value = None
        self.children = dict()

class ID3DecisionTree:
    def __init__(self, X, Y, A, label_name = "output"):
        """
        X : array like, shape = (size, no.of attributes)
        Training attribute values
        Y : array like, shape = (size,)
        Training labels
        A : dict
        Attribute_name -> column_index pairs
        label_name : str
        Name of output quantity
        """
        self.root = None
        self.A = A
        self.label_name = label_name
        self.IG = None    # information gain
        self.train(X, Y)

    @staticmethod
    def entropy(Y, classes):
        """
        Y : array like, shape = (size,)
        Training labels
        classes : list
        Output classes
        """
        E = 0
        p = np.zeros((len(classes),))
        for i in range(len(classes)):
            p[i] = (Y == classes[i]).sum()/Y.size
            if p[i] == 0:
                continue
            E -= p[i]*np.log2(p[i])

        if (p==1).any():
            return 0
        return E

    @staticmethod
    def info_gain(X, Y, attr, classes):
        """
        X : array like, shape = (size, no.of attributes)
        Training attribute values
        Y : array like, shape = (size,)
        Training label
        attr : int
        Atribute column
        classes : list
        Output classes
        """
        values = set(X[:,attr])
        S = Y.size
        E = __class__.entropy(Y, classes)
        IG = E
        for v in values:
            Sv = (X[:,attr] == v).sum()
            Ev = __class__.entropy(Y[X[:,attr] == v], classes)
            IG -= Sv * Ev / S
        return IG, E

    def train(self, X, Y):
        classes = list(set(Y))
        self.root = Node()
        E = __class__.entropy(Y, classes)

        # zero entropy - hence terminate
        if E == 0:
            self.root.value = Y[0]
            return

        # all attributes considered, hence terminate
        if not self.A:
            p = np.zeros((len(classes,)))
            for i in range(len(classes)):
                p[i] = (Y == classes[i]).sum()
            self.root.value = classes[p.argmax()]
            return

        # else branch
        IGbest = -float('inf')
        Ebest = 1.0
        A_best = None
        for attr in self.A:
            IG, E = __class__.info_gain(X, Y, self.A[attr], classes)
            if IG > IGbest:
                IGbest = IG
                Ebest = E
                A_best = attr

        threads = list()
        self.root.attr = A_best
        self.IG = IGbest
        values = set(X[:,self.A[A_best]])
        for v in values:
            cond = X[:,self.A[A_best]] == v
            Atemp = self.A.copy()
            # remove current used attribute from Attribute dict
            Atemp.pop(A_best)
            th = threading.Thread(target=create_subtree, args=(X[cond], Y[cond], Atemp, self.root.children, v))
            threads.append(th)
            th.start()

        for th in threads:
            th.join()

    def predict(self, X):
        """
        X : array like, shape = (no. of attributes,)
        Prediction instance
        """
        root = self.root
        while root.attr:
            tree = root.children[X[self.A[root.attr]]]
            root = tree.root
        return root.value

    def get_accuracy(self, X, Y):
        """
        X : array like, shape = (size, no. of attributes)
        Test data
        Y : array like, shape = (size,)
        Output labels
        """
        equal = 0
        for i in range(Y.shape[0]):
            pred = self.predict(X[i])
            equal += pred == Y[i]
        return equal / Y.shape[0]

    def show_tree(self):
        def dfs(tree, tabs=1):
            root = tree.root
            if root.value is not None:
                print(self.label_name, ":", root.value)
                return
            print(root.attr, "(IG = %.3f):"%tree.IG)
            for v in root.children:
                print("   "*(tabs), "-", v, "->", end=" ")
                dfs(root.children[v], tabs+1)
        dfs(self)
