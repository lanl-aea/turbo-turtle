def return_abaqus_constant(search_string):
    """If search_string is found in the abaqusConstants module, return the abaqusConstants object. Else None

    :param str search_string: string to search in the abaqusConstants module attributes

    :return value: abaqusConstants attribute, if it exists. Else None
    :rtype: abaqusConstants attribute type, if it exists. Else None
    """
    import abaqusConstants

    search_string = search_string.upper()
    attribute = None
    if hasattr(abaqusConstants, search_string):
        attribute = getattr(abaqusConstants, search_string)
    return attribute
