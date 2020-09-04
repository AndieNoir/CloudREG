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

import os

import websocket

from cloudreg.generator.base import Generator


class ComScireQuanttp(Generator, id='comscire_quanttp'):

    def __init__(self):
        self.ws = websocket.WebSocket()
        self.ws.connect('ws://%s/ws' % os.environ['QUANTTP_LOCATION'])

    def get_bytes(self, length):
        self.ws.send('RANDBYTES %d' % length)
        return self.ws.recv()
