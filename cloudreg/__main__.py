# Copyright (C) 2020 AndieNoir
#
# CloudREG is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CloudREG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with CloudREG.  If not, see <https://www.gnu.org/licenses/>.

import datetime
import json
import os
import threading
import time

import schedule
from flask import Flask, render_template
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from cloudreg import config


app = Flask(__name__)
sockets = Sockets(app)

log_file = None
if config.ENABLE_LOGGING:
    log_file = open('log.csv', 'a')
    if os.stat('log.csv').st_size == 0:
        log_file.write('dt,z_score,viewer_count,generator_id\n')
        log_file.flush()


generator = config.GENERATOR_CLASS()

websockets = []

cumdev = [0]

def update_cumdev():
    global cumdev
    dt = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    viewer_count = len(websockets)
    gaussian = generator.get_gaussian()
    if log_file is not None and (viewer_count > 0 or (viewer_count == 0 and config.LOG_ZERO_VIEWERS)):
        log_file.write(f'{dt},{gaussian:.3f},{viewer_count},{generator.id}\n')
        log_file.flush()
    if len(cumdev) >= 100:
        cumdev = [0]
    else:
        cumdev.append(cumdev[-1] + gaussian)
    for websocket in websockets:
        websocket.send(json.dumps({
            'cumdev': cumdev,
            'viewer_count': viewer_count
        }))

schedule.every(0.5).seconds.do(update_cumdev)

def loop():
    while True:
        schedule.run_pending()
        time.sleep(0.01)

threading.Thread(target=loop).start()


@app.route('/')
def home():
    return render_template('home.html')


@sockets.route('/ws')
def ws_trials(websocket):
    websockets.append(websocket)
    websocket.send(json.dumps({
        'cumdev': cumdev,
        'viewer_count': len(websockets)
    }))
    while not websocket.closed:
        websocket.receive()
    websockets.remove(websocket)


server = pywsgi.WSGIServer(('0.0.0.0', 59632), application=app, handler_class=WebSocketHandler)
server.serve_forever()
