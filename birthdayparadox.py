


import random
import datetime as dt
 
# Min/max birthdays that can go to generator
RNG_BIRTHDAYS: range = range(2, 100)
 
def get_birtdays(numBirthdays) -> list[str]:
    """Returns a list of random datetime objects"""
    birthdays: list[str] = []
 
    for i in range(numBirthdays):
        month: int = random.randint(1, 12)
        last_day: int = 30
 
        match month:
            case 1 | 3 | 5 | 7 | 8 | 10 | 12: # 31 day months
                last_day = 31
            case 2:
                last_day = 28 # February
            case _:
                pass # Keep default
       
        day: int = random.randint(1, last_day)
        # Year is unimportant
        birthday: dt.datetime = dt.datetime(year=1900, month=month, day=day)
       
 
        birthdays.append(birthday.strftime("%b %-d"))
    return birthdays
 
# TODO def Get match
 
def get_match(birthdays) -> dt.datetime | None:
    """Returns a datetime object for a birthday that occurs more than once."""
 
    if len(birthdays) == len(set(birthdays)):
        pass
    else:
        for a in birthdays:
            for b in birthdays[1:]:
                if a == b:
                    match = a
                    print(a, b)
                    return match
    return None
   
 

def main() -> None:
   
    # TODO Display intro
 
    # Get user to input number of birthdays to generate
    # Loops until user inputs valid information.
    while True:
       
        break
 

    # TODO Generate and display the birthdays
    birthdays: list[str] = get_birtdays(42)
       
 
    # TODO Determine if two birthdays match
    match = get_match(birthdays)
    # TODO Display result
 
    # TODO Run through 100_000 simulations
 
    # TODO Display simulation results
 
if __name__ == '__main__':
    main()
 
 
