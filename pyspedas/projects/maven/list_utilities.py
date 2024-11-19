
def initialize_list(the_list):
    """
    Recursively initializes a nested list by replacing each element with an empty list.

    Parameters:
        the_list (list): The list to be initialized.

    Returns:
        list: The initialized list.
    """
    index = 0
    for i in the_list:
        if hasattr(i, "__len__"):
            the_list[index] = initialize_list(i)
        else:
            the_list[index] = []
        index += 1
    return the_list


def place_values_in_list(the_list, location, to_append):
    """
    Appends a value to a list at the specified location.

    Parameters:
        the_list (list): The list to modify.
        location (int or list): The index or indices specifying the location in the list.
        to_append (any): The value to append to the list.

    Returns:
        None
    """
    testing = the_list
    if hasattr(location, "__len__"):
        for i in range(len(location)):
            testing = testing[location[i]]
        testing.append(to_append)
    else:
        testing = testing[location]
        testing.append(to_append)


def get_values_from_list(the_list, location):
    """
    Retrieves values from a nested list based on the provided location.

    Parameters:
        the_list (list): The nested list from which to retrieve values.
        location (int or list): The index or list of indices specifying the location of the desired values.

    Returns:
        The value(s) at the specified location in the nested list.
    """
    testing = the_list
    if hasattr(location, "__len__"):
        for i in range(len(location)):
            testing = testing[location[i]]
        return testing
    else:
        testing = testing[location]
        return testing

