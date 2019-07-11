# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
from os import path


class PoliceNode:
    """
    Tree node: left and right child + policeId and FineAmt which can be any object
    """
    def __init__(self, policeId=0, fineAmt=0):
        """
        Node constructor

        @param tree root node and data(policeId and FineAmt) object
        """
        self.left = None
        self.right = None
        self.policeId = policeId
        self.fineAmt = fineAmt
        

    def insertByPoliceId(self, policeId, fineAmt):
        """
        Insert new node with policeId and FineAmt. Ordering based on policeId

        @param tree root node and data(policeId and FineAmt) object
        """
        if self.policeId:
            if policeId < self.policeId:
                if self.left is None:
                    self.left = PoliceNode(policeId, fineAmt)
                else:
                    self.left.insertByPoliceId(policeId, fineAmt)
            elif policeId > self.policeId:
                if self.right is None:
                    self.right = PoliceNode(policeId, fineAmt)
                else:
                    self.right.insertByPoliceId(policeId, fineAmt)
            elif policeId == self.policeId:
                self.fineAmt += fineAmt
        else:
            self.policeId = policeId
            self.fineAmt = fineAmt
            
    def insertByFineAmt(self, node):
        """
        Insert new node with data

        @param tree root node and new node to insert
        """
        if self.fineAmt:
            if node.fineAmt <= self.fineAmt:
                if self.left is None:
                    self.left = node
                else:
                    self.left.insertByFineAmt(node)
            elif node.fineAmt > self.fineAmt:
                if self.right is None:
                    self.right = node
                else:
                    self.right.insertByFineAmt(node)
        else:
            self.policeId = node.policeId
            self.fineAmt = node.fineAmt
            #self = node
            del node
            node = None
                        
                
    def reorderByFineAmount(self):
        tree_fine = PoliceNode()
        self.remove_node(tree_fine)
        return tree_fine
    
    def destroyPoliceTree(self):
        """
        Remove one by one from the last leaf node and insert it into the new tree

        @param tree node
        """
        self.remove_tree()
        self = None
        
        
        
    def remove_tree(self, parent=None):
        """
        Remove one by one from the last leaf node

        @param tree node,parent of tree node
        """
        node = self
        if self.left:
            self.left.remove_tree(self)
        if self.right:
            self.right.remove_tree(self)
        if parent:
            if parent.left is node:
                parent.left = None
            else:
                parent.right = None
            del node
        else :
            del node       
                
    def remove_node(self,  fine_node, parent=None):
        """
        Remove one by one from the last leaf node and insert it into the new tree

        @param tree node, root of new tree, parent of tree node
        """
        node = self
        if self.left:
            self.left.remove_node(fine_node, self)
        if self.right:
            self.right.remove_node(fine_node, self)
        if parent:
            if parent.left is node:
                parent.left = None
            else:
                parent.right = None
            fine_node.insertByFineAmt(node)
        else :
            fine_node.insertByFineAmt(node)
      
        
        
    def printPoliceTree(self):
        """
        Print tree content inorder
        
        @param tree parent node
        """
        if self:
            if self.left:
                self.left.printPoliceTree()
            if self.policeId:
                print("Polide ID: ", self.policeId, "\t", "Fine Amount ", self.fineAmt, "\n" ) 
            if self.right:
                self.right.printPoliceTree()
            
    def findMaxFine(self):
        """
        Return right most leaf which will be the max fine amount        
        
        @param tree parent node
        """
        if self.fineAmt:
            current = self
            while current.right is not None:
                current = current.right
            return current.fineAmt
        else :
            return 0
    
    def printBonusPolicemen(self) :
        """
        Print all nodes with Fine amount greated that 90% od max fine amount        
        
        @param tree parent node
        """
        orig_stdout = sys.stdout
        maxFineAmt = 0
        #print(sys.stdout)
        f = open('out.txt', 'w')
        sys.stdout = f
        maxFineAmt = self.findMaxFine() 
        threshold = 0.9 * maxFineAmt
        self.print_value_above(threshold)
        sys.stdout = orig_stdout
        f.close()
        
    
    def print_value_above(self, threshold):
        """
        Print into a file all nodes with Fine amount greater that threshold        
        
        @param tree parent node
        """
        if self.right:
            self.right.print_value_above(threshold)
        if self.policeId:
            if (self.fineAmt >= threshold) :
                print(self.policeId, "\t", self.fineAmt, "\n" ) 
            else:
                return
        if self.left:
            self.left.print_value_above(threshold)

class HashNode:    
    def initialize_hash(self):
        size = 30
        self.table = [[] for i in range(size)]
        return self

    def insert_hash(self, lic):
        def hash_map(key):
            return hash(key) % len(self.table) # hashing the key is lic has alphabets, hash(num) = num

        hash_index = hash_map(lic)
        key_present = False
        create_bucket = self.table[hash_index]
        for i, kv in enumerate(create_bucket):
            k, v = kv

            if lic == k:
                key_present = True
                break
        if key_present:
            print("This License Number is already present, updating only the violations")
            create_bucket[i] = ((lic, v+1)) # This is assuming driver_hash is a tuple
        else:
            print("This License Number is not present, updating the key, val")
            create_bucket.append((lic, 1))
            
    def print_violators(self):
        """
        --------------Violators-------------
        <license no>, no of violations
        """
        orig_stdout = sys.stdout
        #print(sys.stdout)
        f = open('Violators.txt', 'w')
        sys.stdout = f
        for i, kv in enumerate(self.table):
            for k, v in kv:
                if v >= 1:
                    print("{}, {} \n".format(k, v))        
        sys.stdout = orig_stdout
        f.close()


    def destroy_hash(self):
        """
        def destroyHash (driverhash): This function destroys all the entries inside the hash table. This
        is a clean-up code.
        """
        self.table = [None]

           
          
if __name__ == '__main__':
    tree_police = PoliceNode()
    hash_pointer = HashNode()
    hash_pointer.initialize_hash()
    if (path.exists("inputPS3.txt")) :
        print("Reading the Input File and creating the tree sorted by Police ID")
        with open("inputPS3.txt", "r") as ins:
            for line in ins:
                line = line.split('\n')[0]
                inputs = (line.split('/'))
                inputs[0] = inputs[0].rstrip()
                inputs[0] = inputs[0].lstrip()
                inputs[1] = inputs[1].rstrip()
                inputs[1] = inputs[1].lstrip()
                inputs[2] = inputs[2].rstrip()
                inputs[2] = inputs[2].lstrip()
                if (not((str.isdigit(inputs[0])) and (str.isdigit(inputs[1])) and (str.isdigit(inputs[2])))) :
                    print("The following entry is Not a Number which is not valid and so Skipping it")
                    print(inputs[0], inputs[2])
                    continue
                if ((int(inputs[0]) < 0) or (int(inputs[1]) < 0) or (int(inputs[2]) < 0)) :
                    print("The following entry is negavtive which is not valid and so Skipping it")
                    print(inputs[0], inputs[2])
                    continue              
                tree_police.insertByPoliceId(int(inputs[0]),int(inputs[2]))
                hash_pointer.insert_hash(int(inputs[1]))
        hash_pointer.print_violators()
        print("Tree created")
        print("Printing from Tree sorted by Police ID  - Inorder Traversal")
        tree_police.printPoliceTree()
        print("Reordering from the tree to another tree sorted by Fine Amount")
        tree_fine = tree_police.reorderByFineAmount()
        print("Reordering Done")
        print("Printing from Tree sorted by Fine Amount - Inorder Traversal")
        tree_fine.printPoliceTree()
        print("Generating the Bunus List Output file")
        tree_fine.printBonusPolicemen()
        print("Generation Done")
        print("Destroying Both the Police Trees")
        tree_police.destroyPoliceTree()
        tree_fine.destroyPoliceTree()
        print("Destroyed Both the Police Trees")

    else :
        print("The input file is not present")
    