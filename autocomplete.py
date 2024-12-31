from collections import deque
import heapq
import random
import string

class Node:
    #TODO
    def __init__(self):
        self.children = {}
        self.isEndOfTheWord = False # to check if it's the end of the word or not.
        self.frequencyOfChar = {}

class Autocomplete():
    def __init__(self, parent=None, document=""):
        self.root = Node()
        self.suggest = self.suggest_ucs #Default, change this to `suggest_dfs/ucs/bfs` based on which one you wish to use.

    def build_tree(self, document):
        for word in document.split():
            node = self.root
            for char in word:
                #TODO for students
                # check if the char is there or not. if not then add a node.
                if char not in node.children:
                    node.children[char] = Node()
                    node.frequencyOfChar[char] = 0 # setting the frequency of specific char to 0.
                node.frequencyOfChar[char] += 1 # incrementing the freq.
                node = node.children[char] # move to the next node.
            node.isEndOfTheWord = True # marking the end of the word
    

    def suggest_random(self, prefix):
        random_suffixes = [''.join(random.choice(string.ascii_lowercase) for _ in range(3)) for _ in range(5)]
        return [prefix + suffix for suffix in random_suffixes]

    #TODO for students!!!
    def suggest_bfs(self, prefix):
        # finding the node that matches the last char of the prefix.
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # Performing BFS from the node that got matched from the last char of the prefix.
        queue = deque([(node, prefix)])
        suggestions = []
        while queue:
            curr_node, curr_word = queue.popleft()
            if curr_node.isEndOfTheWord:
                suggestions.append(curr_word)

            for ch, child in curr_node.children.items():
                queue.append((child, curr_word + ch))
        return suggestions

            
    #TODO for students!!!
    def suggest_dfs(self, prefix):
        # finding the node that matches the last char of the prefix.
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        # Performing DFS from the node that got matched from the last char of the prefix.
        # implementing stack based dfs.
        # stack = [(node, prefix)]
        suggestions = []
        # while stack:
        #     curr_node, curr_word = stack.pop()
        #     if curr_node.isEndOfTheWord:
        #         suggestions.append(curr_word)
        #     for ch, child in curr_node.children.items():
        #         stack.append((child, curr_word + ch))
        # return suggestions

        # defining helper function to use recursion.
        def dfs(curr_node, curr_word):
            if curr_node.isEndOfTheWord:
                suggestions.append(curr_word)
            for ch, child in curr_node.children.items():
                dfs(child, curr_word + ch)
        dfs(node, prefix)
        return suggestions
    

    #TODO for students!!!
    def suggest_ucs(self, prefix):
        # finding the node that matches the last char of the prefix.
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        suggestions = []
        priority_queue = []

        heapq.heappush(priority_queue, (0, prefix, node))
        while priority_queue:
            total_cost, curr_word, curr_node = heapq.heappop(priority_queue)
            if curr_node.isEndOfTheWord:
                suggestions.append(curr_word)
            for ch, child in curr_node.children.items():
                freq = curr_node.frequencyOfChar[ch]
                cost = total_cost + (1/freq)
                heapq.heappush(priority_queue, (cost, curr_word + ch, child))
        return suggestions
