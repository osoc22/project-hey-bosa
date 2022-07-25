"""

A small Test application to test the VAC user interface using Flask-MQTT.

"""

from ast import If
import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
print('Configured MQTT IP Address: ' + app.config['MQTT_BROKER_URL'])

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)
messages_recieved = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping/')
def ping():
    return messages_recieved

# MQTT / Socket IO functions

@socketio.on('connect')
def confirm_connect():
    print('connected!')

@socketio.on('subscribe')
def handle_subscribe(data):
    mqtt.subscribe(data)


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()

@mqtt.on_message()
def handle_messages(client, userdata, message):
    print('Received message on topic {}: {}'.format(message.topic, message.payload.decode()))

    messages_recieved.update({message.topic: message.payload.decode()})


def display_p1():
    return render_template('page1.html')

def display_p2():
    return render_template('page2.html')


handle_subscribe('test/pls')
handle_subscribe('test/hey')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)