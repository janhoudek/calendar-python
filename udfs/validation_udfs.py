def validStartYear(year):
    if not type(year) == int:
        raise ValueError('Number of years must be an integer')
    if year < 1970 or year > 2100:
        raise ValueError('Year must be between 1900 and 2100')

    return True

def validForYears(for_years):
    if not type(for_years) == int:
        raise ValueError('Number of years must be an integer')
    if for_years < 1:
        raise ValueError('Number of years must be greater than 0')
    
    return True