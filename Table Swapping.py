import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Table(object):
    """A table object contains the information about the current state of a table and about the quality of interactions
    between guests at any point"""
    def __init__(self, size):
        self.com = communication = {"adjacent": 1.0,
                                    "diagonal": 0.5
                                    }  # These a weights given to the quality of interactions
        self.size = size
        self.diners = list(range(size))
        self.length = (size + 1) // 2
        self.layout = np.asarray([list(range(self.length)), list(range(self.length, 2 * self.length))])
        self.social_interactions = self.get_course_interactions()

    def get_course_interactions(self):
        """This takes the state of the table and creates a numpy array of """
        course_interations = np.zeros((self.size, self.size))
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
        position = np.where(self.layout == diner)
        y = position[0][0]
        x = position[1][0]
        return [y, x]

    def get_adjacents(self, p):
        adjacent_diners = []
        adjacent_diners.append(self.layout[1 - p[0]][p[1]])  # opposite
        if p[1] == 0:  # Is the diner on the far left?
            pass
        else:
            adjacent_diners.append(self.layout[p[0]][p[1] - 1])  # left
        try:
            adjacent_diners.append(self.layout[p[0]][p[1] + 1])  # right
        except IndexError:  # Handles the diners on the far right
            pass
        return adjacent_diners

    def get_diagonal(self, p):
        diagonal_diners = []
        if p[1] == 0:  # Is the diner on the far left?
            pass
        else:
            diagonal_diners.append(self.layout[1 - p[0]][p[1] - 1])  # diagonal left
        try:
            diagonal_diners.append(self.layout[1 - p[0]][p[1] + 1])  # diagonal right
        except IndexError:  # Handles the diners on the far right
            pass
        return diagonal_diners


class Meal(object):
    """A meal is object is filling an delicious"""
    def __init__(self, table, n_iterations, function):
        self.courses = n_iterations
        self.function = function
        self.table = table

    def eat_meal(self):
        for i in range(self.courses):
            current_social = self.table.social_interactions
            self.table.layout = self.function(self.table.layout)
            self.table.social_interactions = self.combine_interactions(current_social,
                                                                       self.table.get_course_interactions())
        self.table.social_interactions = np.log2(
            (self.table.social_interactions) + 1)  # Function for managing diminishing returns

    def combine_interactions(self, new, previous):
        combined = np.dstack((new, previous))
        return np.apply_along_axis(self.combine, 2, combined)

    def combine(self, interactions):
        previous = interactions[0]
        new = interactions[1]
        return previous + new


class Test(object):
    """A Test object can be used to test a table swapping function with the range of diner and course counts specified"""
    def __init__(self, function):
        self.min_diners = 6
        self.max_diners = 30
        self.min_courses = 3
        self.max_courses = 4
        self.function = function
        self.results_df = self.test_function()
        self.average_improvement = self.final_verdict()

    def calculate_score(self, interactions):
        return (
        interactions.sum() / (interactions.size - len(interactions)))  # Discounts the diagonal zeros and calculates mean

    def test_function(self):
        """Returns the average social interaction ratings as a percentage change in the quality of social
        interactions from a table where nobody moves (the lambda function).
        Results in a dtaframe with each course count as a cloumn and each diner count as a row"""
        resultses = []
        for func in [self.function, lambda x: x]:
            results = pd.DataFrame(index=list(range(self.min_diners, self.max_diners + 1)),
                                   columns=list((range(self.min_courses, self.max_courses + 1))))
            for ncourses in range(self.min_courses, self.max_courses + 1):
                for ndiners in range(self.min_diners, self.max_diners + 1):
                    table = Table(ndiners)
                    meal = Meal(table, ncourses, func)
                    meal.eat_meal()
                    results[ncourses][ndiners] = self.calculate_score(meal.table.social_interactions)
            resultses.append(results)
        social_interaction_benefit = ((resultses[0] / resultses[1]) * 100) - 100
        return social_interaction_benefit

    def final_verdict(self):
        """Currently just averages the dataframe, maybe it should do something cleverer?"""
        verdict = self.results_df.mean().mean()
        return verdict

    def plot_results(self):
        legend = []
        for course in range(self.min_courses, self.max_courses + 1):
            plt.plot(self.results_df.index.values, self.results_df[course])
            legend.append(str(course) + " courses")
        plt.legend(legend, loc='lower right')
        plt.xlabel('Number of dinner guests')
        plt.ylabel('Percent increase in social interaction rating')
        plt.title('Improvement in social interactions from the\n'+
                  'swapping function, relative to stationary benchmark')
        plt.annotate('This function has an\naverage improvement of:\n' +
                     str(self.average_improvement), xy = (self.min_diners ,35))
        plt.show()

def Example_Function(table):
    """This function makes all guests moving 3 places around the table"""
    out_table = table.tolist()
    n = 3
    top = out_table[1][n - 1::-1] + out_table[0][0:-n]
    bottom = out_table[1][n:] + out_table[0][:-(n + 1):-1]
    return np.array([top, bottom])

if __name__ == "__main__":
    example_test = Test(function=Example_Function)
    example_test.plot_results()
