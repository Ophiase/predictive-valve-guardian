from enum import IntEnum


class DerivativeOrder(IntEnum):
    SIGNAL = 0
    SLOPE = 1
    CURVATURE = 2
