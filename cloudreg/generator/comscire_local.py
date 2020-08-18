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

from cloudreg.generator.base import Generator


class ComScireLocal(Generator, id='comscire_local'):

    def __init__(self):
        self.os_windows = os.name == 'nt'
        if self.os_windows:
            import win32com.client
            self.qng = win32com.client.Dispatch('QWQNG.QNG')
        else:
            import ctypes
            import platform
            self.libqwqng_wrapper = ctypes.cdll.LoadLibrary('./libqwqng-wrapper-x86-64.so' if platform.machine().endswith('64') else './libqwqng-wrapper.so')
            self.libqwqng_wrapper.GetQwqngInstance.restype = ctypes.c_void_p
            self.libqwqng_wrapper.RandBytes.argtypes = [ctypes.c_void_p, ctypes.c_int]
            self.libqwqng_wrapper.RandBytes.restype = ctypes.POINTER(ctypes.c_char)
            self.libqwqng_wrapper.Clear.argtypes = [ctypes.c_void_p]
            self.qng_pointer = self.libqwqng_wrapper.GetQwqngInstance()

    def get_bytes(self, length):
        return self.get_bytes_windows(length) if self.os_windows else self.get_bytes_linux(length)

    def get_bytes_windows(self, length):
        self.qng.Clear()
        if length <= 8192:
            return bytes(self.qng.RandBytes(length))
        else:
            data = bytearray()
            for x in range(length // 8192):
                data.extend(bytearray(self.qng.RandBytes(8192)))
            bytes_needed = length % 8192
            if bytes_needed != 0:
                data.extend(bytearray(self.qng.RandBytes(bytes_needed)))
            return bytes(data)

    def get_bytes_linux(self, length):
        self.libqwqng_wrapper.Clear(self.qng_pointer)
        if length <= 8192:
            return self.libqwqng_wrapper.RandBytes(self.qng_pointer, length)[:length]
        else:
            data = bytearray()
            for x in range(length // 8192):
                data.extend(self.libqwqng_wrapper.RandBytes(self.qng_pointer, 8192)[:8192])
            bytes_needed = length % 8192
            if bytes_needed != 0:
                data.extend(self.libqwqng_wrapper.RandBytes(self.qng_pointer, bytes_needed)[:bytes_needed])
            return bytes(data)
