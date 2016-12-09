import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Table(object):
    def __init__(self, size):
        self.com = communication = {"adjacent":1.0,
                                    "diagonal":0.5
                                    }
        self.size = size
        self.diners = list(range(size))
        self.length = (size+1)//2
        self.layout = np.asarray([list(range(self.length)),list(range(self.length, 2*self.length))])
        self.social_interactions = self.get_course_interactions()

    def get_course_interactions(self):
        course_interations = np.zeros((self.size,self.size))
        for i in self.diners:
            pos = self.get_positon(i)
            for j in self.get_adjacents(pos):
                try:
                    course_interations[i][j] = self.com["adjacent"]
                except IndexError:
                    pass
            for k in self.get_diagonal(pos):
                try:
                    course_interations[i][k] = self.com["diagonal"]
                except IndexError:
                    pass
        return course_interations

    def get_positon(self, diner):
        position = np.where(self.layout==diner)
        y = position[0][0]
        x = position[1][0]
        return [y,x]

    def get_adjacents(self, p):
        adjacent_diners = []
        adjacent_diners.append(self.layout[1-p[0]][p[1]]) #opposite
        if p[1] == 0: #Is the diner on the far left?
            pass
        else:
            adjacent_diners.append(self.layout[p[0]][p[1]-1]) #left
        try:
            adjacent_diners.append(self.layout[p[0]][p[1]+1]) #right
        except IndexError: #Handles the diners on the far right
            pass
        return adjacent_diners

    def get_diagonal(self, p):
        diagonal_diners = []
        if p[1] == 0: #Is the diner on the far left?
            pass
        else:
            diagonal_diners.append(self.layout[1-p[0]][p[1]-1]) #diagonal left
        try:
            diagonal_diners.append(self.layout[1-p[0]][p[1]+1]) #diagonal right
        except IndexError: #Handles the diners on the far right
            pass
        return diagonal_diners

class Meal(object):
    def __init__(self, table, n_iterations, function):
        self.courses = n_iterations
        self.function = function
        self.table = table

    def eat_meal(self):
        for i in range(self.courses):
            current_social = self.table.social_interactions
            self.table.layout = self.function(self.table.layout)
            self.table.social_interactions = self.combine_interactions(current_social,self.table.get_course_interactions())
        self.table.social_interactions = np.log2((self.table.social_interactions)+1) #Function for managing diminishing returns

    def combine_interactions(self, new, previous):
        combined = np.dstack((new,previous))
        return np.apply_along_axis(self.combine, 2, combined)

    def combine(self, interactions):
        previous = interactions[0]
        new = interactions[1]
        return previous + new

def Example_Function(table):
    out_table = table.tolist()
    n = 3
    top = out_table[1][n-1::-1] + out_table[0][0:-n]
    bottom = out_table[1][n:] + out_table[0][:-(n+1):-1]
    return np.array([top,bottom])

def Null_Function(table):
    return table

def calculate_score(interactions):
    return (interactions.sum()/(interactions.size-len(interactions))) #Remove the diagonal zeros and calculate mean

def test_function(fun = Null_Function, min_diners = 10, max_diners = 50, min_courses =  3, max_courses = 3):
    resultses = []
    for func in [fun, Null_Function]:
        results = pd.DataFrame(index=list(range(min_diners,max_diners+1)), columns=list((range(min_courses,max_courses+1))))
        for ncourses in range(min_courses, max_courses+1):
            for ndiners in range(min_diners, max_diners+1):
                table = Table(ndiners)
                meal = Meal(table, ncourses, func)
                meal.eat_meal()
                results[ncourses][ndiners] = calculate_score(meal.table.social_interactions)
        resultses.append(results)
    return ((resultses[0]/resultses[1])*100)-100


n_course = 3
test = test_function(fun = Example_Function, )
print(test)

plt.plot(test.index.values, test[3])

plt.show()

