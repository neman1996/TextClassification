
from __future__ import print_function



training_data = []


header = []

import json

with open('data.txt', mode='r') as f:
    content = f.readlines()
    content = [x.strip() for x in content]
    content.remove(content[0])

    symptoms = dict()
    symptomsList = []
    diseases = dict()
    
    #res = []
    for item in content:
        p = item.split("\t")
        
        if(p[0] not in symptoms):
            symptomsList.append(p[0])
            symptoms[p[0]] = 0

        if(p[1] not in diseases):
            diseases[p[1]] = []

        symptoms[p[0]] += 1
        diseases[p[1]].append(p[0])
    
    data = []

    i=0
    for key in diseases:
        data.append([])
        for symptom in symptomsList:
            if(symptom in diseases[key]):
                data[i].append(1)
            else:
                data[i].append(0)
        data[i].append(key)
        i += 1

    training_data = data
    header = symptomsList

training_data = training_data[:100]

print(len(training_data))

import random
for item in training_data:
    new_row = item
    for j in range(20):
        r = random.randint(0, len(symptomsList)-1)
        if(new_row[r] == 0):
            new_row[r] = 1
        else:
            new_row[r] = 0
    training_data.append(new_row)

print(len(training_data))

def unique_vals(rows, col):
    
    return set([row[col] for row in rows])




def class_counts(rows):
    
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts




def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)




class Question:
    

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        # Compare the feature value in an example to the
        # feature value in this question.
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))




def partition(rows, question):
    
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows




def gini(rows):
    
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity




def info_gain(left, right, current_uncertainty):
    """Information Gain.

    The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)




def find_best_split(rows):
    """Find the best question to ask by iterating over every feature / value
    and calculating the information gain."""
    best_gain = 0  # keep track of the best information gain
    best_question = None  # keep train of the feature / value that produced it
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1  # number of columns

    for col in range(n_features):  # for each feature

        values = set([row[col] for row in rows])  # unique values in the column

        for val in values:  # for each value

            question = Question(col, val)

            # try splitting the dataset
            true_rows, false_rows = partition(rows, question)

            # Skip this split if it doesn't divide the
            # dataset.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the information gain from this split
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            # You actually can use '>' instead of '>=' here
            # but I wanted the tree to look a certain way for our
            # toy dataset.
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question



class Leaf:
   

    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:
    

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):
    


    gain, question = find_best_split(rows)

    
    if gain == 0:
        return Leaf(rows)

    
    true_rows, false_rows = partition(rows, question)


    true_branch = build_tree(true_rows)

    
    false_branch = build_tree(false_rows)

    
    return Decision_Node(question, true_branch, false_branch)


def print_tree(node, spacing=""):
    

    
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    
    print (spacing + str(node.question))

    
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

   
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


def classify(row, node):
   

 
    if isinstance(node, Leaf):
        return node.predictions

   
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)




def print_leaf(counts):
    """A nicer way to print the predictions at a leaf."""
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


if __name__ == '__main__':

    my_tree = build_tree(training_data)

    print_tree(my_tree)

    
    """testing_data = [
        ['Round','Green', 3, 'Apple'],
        ['Oval','Yellow', 4, 'Apple'],
        ['Oval','Red', 2, 'Grape'],
        ['Oval','Red', 1, 'Grape'],
        ['Round','Yellow', 3, 'Lemon']
    ]"""

    """testing_data = [
        ['6.2', '3.4', '5.4', '2.8', 'Iris-virginica'], ['5.9', '3.0', '5.1', '1.8', 'Iris-virginica'],
        ['4.4', '3.2', '1.3', '0.4', 'Iris-setosa']
    ]"""

    testing_data = []
    testing_data.append(training_data[-10])

    for row in testing_data:
        print ("Actual: %s. Predicted: %s" %
               (row[-1], print_leaf(classify(row, my_tree))))
