#!/usr/bin/python

def display_harvest_recursive(day: int, last_day: int) -> None:
    if (day <= 0):
        print("Harvest time!")
        return
    print(f"Day {last_day - day}")
    display_harvest_recursive(day-1, last_day)


def ft_count_harvest_recursive() -> None:
    days: int = int(input("Days until harvest: "))
    display_harvest_recursive(days, days+1)
