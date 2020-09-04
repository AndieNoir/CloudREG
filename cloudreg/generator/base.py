# Copyright (C) 2020 AndieNoir
#
# CloudREG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CloudREG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CloudREG.  If not, see <https://www.gnu.org/licenses/>.

import math
from enum import Enum

from cloudreg import config


class Generator:

    LOOKUP_TABLE = [
        -8, -6, -6, -4, -6, -4, -4, -2, -6, -4, -4, -2, -4, -2, -2,  0,
        -6, -4, -4, -2, -4, -2, -2,  0, -4, -2, -2,  0, -2,  0,  0,  2,
        -6, -4, -4, -2, -4, -2, -2,  0, -4, -2, -2,  0, -2,  0,  0,  2,
        -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
        -6, -4, -4, -2, -4, -2, -2,  0, -4, -2, -2,  0, -2,  0,  0,  2,
        -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
        -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
        -2,  0,  0,  2,  0,  2,  2,  4,  0,  2,  2,  4,  2,  4,  4,  6,
        -6, -4, -4, -2, -4, -2, -2,  0, -4, -2, -2,  0, -2,  0,  0,  2,
        -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
        -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
        -2,  0,  0,  2,  0,  2,  2,  4,  0,  2,  2,  4,  2,  4,  4,  6,
        -4, -2, -2,  0, -2,  0,  0,  2, -2,  0,  0,  2,  0,  2,  2,  4,
        -2,  0,  0,  2,  0,  2,  2,  4,  0,  2,  2,  4,  2,  4,  4,  6,
        -2,  0,  0,  2,  0,  2,  2,  4,  0,  2,  2,  4,  2,  4,  4,  6,
         0,  2,  2,  4,  2,  4,  4,  6,  2,  4,  4,  6,  4,  6,  6,  8
    ]

    LAST_BYTE_LOOKUP_TABLE_LSB0 = [
        -7, -5, -5, -3, -5, -3, -3, -1, -5, -3, -3, -1, -3, -1, -1,  1,
        -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
        -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
        -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
        -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
        -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
        -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
        -1,  1,  1,  3,  1,  3,  3,  5,  1,  3,  3,  5,  3,  5,  5,  7,
        -7, -5, -5, -3, -5, -3, -3, -1, -5, -3, -3, -1, -3, -1, -1,  1,
        -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
        -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
        -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
        -5, -3, -3, -1, -3, -1, -1,  1, -3, -1, -1,  1, -1,  1,  1,  3,
        -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
        -3, -1, -1,  1, -1,  1,  1,  3, -1,  1,  1,  3,  1,  3,  3,  5,
        -1,  1,  1,  3,  1,  3,  3,  5,  1,  3,  3,  5,  3,  5,  5,  7
    ]

    LAST_BYTE_LOOKUP_TABLE_MSB0 = [
        -7, -7, -5, -5, -5, -5, -3, -3, -5, -5, -3, -3, -3, -3, -1, -1,
        -5, -5, -3, -3, -3, -3, -1, -1, -3, -3, -1, -1, -1, -1,  1,  1,
        -5, -5, -3, -3, -3, -3, -1, -1, -3, -3, -1, -1, -1, -1,  1,  1,
        -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
        -5, -5, -3, -3, -3, -3, -1, -1, -3, -3, -1, -1, -1, -1,  1,  1,
        -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
        -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
        -1, -1,  1,  1,  1,  1,  3,  3,  1,  1,  3,  3,  3,  3,  5,  5,
        -5, -5, -3, -3, -3, -3, -1, -1, -3, -3, -1, -1, -1, -1,  1,  1,
        -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
        -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
        -1, -1,  1,  1,  1,  1,  3,  3,  1,  1,  3,  3,  3,  3,  5,  5,
        -3, -3, -1, -1, -1, -1,  1,  1, -1, -1,  1,  1,  1,  1,  3,  3,
        -1, -1,  1,  1,  1,  1,  3,  3,  1,  1,  3,  3,  3,  3,  5,  5,
        -1, -1,  1,  1,  1,  1,  3,  3,  1,  1,  3,  3,  3,  3,  5,  5,
         1,  1,  3,  3,  3,  3,  5,  5,  3,  3,  5,  5,  5,  5,  7,  7
    ]

    def __init_subclass__(cls, id, bit_numbering, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.id = id
        cls.bit_numbering = bit_numbering

    def get_bytes(self, length) -> bytes:
        pass

    def get_gaussian(self):
        deviation = 0
        random_bytes = self.get_bytes(config.BYTES_PER_TRIAL)
        for i in range(len(random_bytes) - 1):
            deviation += self.LOOKUP_TABLE[random_bytes[i]]
        if self.bit_numbering == BitNumbering.MSB0:
            deviation += self.LAST_BYTE_LOOKUP_TABLE_MSB0[random_bytes[-1]]
        else:
            deviation += self.LAST_BYTE_LOOKUP_TABLE_LSB0[random_bytes[-1]]
        return deviation / math.sqrt(len(random_bytes) * 8)


class BitNumbering(Enum):
    LSB0 = 'lsb0'
    MSB0 = 'msb0'
    UNKNOWN = 'unknown'
