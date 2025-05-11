from math import floor
from datetime import date

def getEasters(yy: int) -> date:
    """
    Calculates the date of Easter Sunday for a given year using the 
    Gaussian algorithm.

    Parameters:
    ----------
    yy : int
        The year for which the date of Easter Sunday is to be calculated.

    Returns:
    -------
    date
        A 'datetime.date' object representing the date of Easter Sunday 
        in the given year.
    """

    a = yy % 19                             # Calculation of the cycle for the lunar year (Year modulo 19)
    b = yy % 4                              # Calculation of the rest of the year modulo 4 (Year modulo 4)
    c = yy % 7                              # Calculation of the rest of the year modulo 7 (Year modulo 7)
    k = floor(yy / 100)                     # Century calculation (yy / 100)
    p = floor((13 + 8 * k) / 25)            # Century correction by leap rule
    q = floor(k / 4)                        # Leap century correction
    m = (15 - p + k - q) % 30               # Golden number (lunar cycle correction)
    n = (4 + k - q) % 7                     # Day of the week correction
    d = (19 * a + m) % 30                   # Intermediate calculation of Easter day
    e = (2 * b + 4 * c + 6 * d + n) % 7     # Day of the week calculation

    # Day of Easter
    day_of_easter = 22 + d + e # Day of Easter - starting day of Easter in March
    month_of_easter = 3 # Month of easter - default month is March

    # If the day exceeds 31 (i.e. Easter falls in April)
    if day_of_easter > 31:
        day_of_easter = d + e - 9 # Convert day to April
        month_of_easter = 4

    # Correction of special cases (exceptions in Gaussian algorithm)
    if d == 29 and e == 6:
        day_of_easter = 19 # Special case for d = 29, e = 6

    if d == 28 and e == 6 and (11 * m + 11 ) % 30 < 19:
        day_of_easter = 18 # Special case for d = 28, e = 6

    return date(yy, month_of_easter, day_of_easter)
