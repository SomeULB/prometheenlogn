
NB_CRITERIA = 1
CRITERIA_Q = [2000, 20, 15, 1, 6]
CRITERIA_P = [10000, 35, 23, 24, 20]
CRITERIA_MAX = [True, True, True, True, True]
CRITERIA_W = [0.397, 0.437, 0.166, 0.23, 0.18]


CRITERIA_W = [x/sum(CRITERIA_W) for x in CRITERIA_W]


def get_number_criteria():
    return NB_CRITERIA


def get_criteria_Q():
    return CRITERIA_Q


def get_criteria_P():
    return CRITERIA_P


def get_criteria_W():
    return CRITERIA_W


def get_criteria_MAX():
    return CRITERIA_MAX
