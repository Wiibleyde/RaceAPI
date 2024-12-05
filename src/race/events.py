from enum import Enum

class RaceEvents(Enum):
    GREEN_FLAG = 1
    YELLOW_FLAG = 2
    RED_FLAG = 3
    SAFETY_CAR = 4
    BLACK_FLAG = 5

    def __str__(self):
        return self.name.replace("_", " ").title()