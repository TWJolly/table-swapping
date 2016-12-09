from pandas import DataFrame

from table_swapping import *


def compare_functions(dictionary_of_functions):
    """This function takes a dictionery of function_names: functions and returns a df of their results"""
    results = {}
    for name, function in dictionary_of_functions.items():
        result = Test(function)
        results[name] = result.final_verdict()
    verdicts_df = DataFrame.from_dict(results, orient = 'index')
    verdicts_df.columns = ['Average score']
    verdicts_df.sort_index(inplace = True)
    return verdicts_df

def move_one_round(table):
    """This function makes all guests moving 1 places around the table"""
    out_table = table.tolist()
    n = 1
    top = out_table[1][n - 1::-1] + out_table[0][0:-n]
    bottom = out_table[1][n:] + out_table[0][:-(n + 1):-1]
    return np.array([top, bottom])

def move_two_round(table):
    """This function makes all guests moving 2 places around the table"""
    out_table = table.tolist()
    n = 2
    top = out_table[1][n - 1::-1] + out_table[0][0:-n]
    bottom = out_table[1][n:] + out_table[0][:-(n + 1):-1]
    return np.array([top, bottom])

def move_three_round(table):
    """This function makes all guests moving 3 places around the table"""
    out_table = table.tolist()
    n = 3
    top = out_table[1][n - 1::-1] + out_table[0][0:-n]
    bottom = out_table[1][n:] + out_table[0][:-(n + 1):-1]
    return np.array([top, bottom])



comparison = compare_functions(dict([('Move 1', move_one_round),
                                     ('Move 2', move_two_round),
                                     ('Move 3', move_three_round)
                                     ]))

print(comparison)