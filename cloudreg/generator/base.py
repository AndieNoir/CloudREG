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

from cloudreg import config


class Generator:

    RANDOM_WALK_LOOKUP_TABLE = [
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

    def __init_subclass__(cls, id, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.id = id

    def get_bytes(self, length) -> bytes:
        pass

    def get_gaussian(self):
        deviation = 0
        random_bytes = self.get_bytes(config.BYTES_PER_TRIAL)
        for byte in random_bytes:
            deviation += self.RANDOM_WALK_LOOKUP_TABLE[byte]
        return deviation / math.sqrt(config.BYTES_PER_TRIAL * 8)
