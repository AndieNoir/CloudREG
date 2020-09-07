CloudREG
========

A Python web app for replicating [PEAR's psychokinesis experiment](http://noosphere.princeton.edu/rdnelson/reg.html).

Running
-------

1. WebPsi currently supports local and remote random number generation using ComScire QNG. For local, install
   [ComScire driver](https://comscire.com/downloads/). For remote, run [Quanttp](https://github.com/awasisto/quanttp)
   on the remote machine and set `QUANTTP_LOCATION` environment variable
   
   Example:

   ```
   # Windows
   set QUANTTP_LOCATION=192.168.0.136:8080/quanttp

   # Linux
   export QUANTTP_LOCATION=192.168.0.136:8080/quanttp
   ```

2. Run the following commands

   ```
   pip3 install -r requirements.txt
   python3 -m cloudreg
   ```

3. Open http://localhost:59632

Adding a new random number generator
------------------------------------

1.  Create a class that extends `Generator` and override the `get_bytes` method

    Example:

    ```python
    # cloudreg/generator/dev_hwrng.py
    
    from cloudreg.generator.base import Generator
    
    
    class DevHwrng(Generator, id='my_rng'):
    
       def get_bytes(self, length):
           with open('/dev/hwrng', 'rb') as f:
               return f.read(length)
    ```

2.  Set the generator class on `config.py`

    ```python
    # cloudreg/config.py
    
    from cloudreg.generator.dev_hwrng import DevHwrng
    
    
    GENERATOR_CLASS = DevHwrng
    ```

License
-------

    Copyright (C) 2020 AndieNoir
    
    CloudREG is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    CloudREG is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with CloudREG.  If not, see <https://www.gnu.org/licenses/>.
