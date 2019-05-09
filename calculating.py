import random

def scale_input(value_to_scale,mini=25,maxi=60): #make sure the number is between two values (25 and 60 for array size of the input)
    if value_to_scale <=mini: return mini #crop any number to a definite min or max
    elif value_to_scale >=maxi: return maxi
    else: return value_to_scale

def generate_random_array(size_of_final_array=24,range_of_values=15): #fill a list with random tuples of values and return the list
    array_to_return = []
    for points in range(scale_input(size_of_final_array)):
        random_x = random.randint(-range_of_values,range_of_values)
        random_y = random.randint(-range_of_values,range_of_values)
        array_to_return.append((random_x,random_y))

    return array_to_return #return the filled list
