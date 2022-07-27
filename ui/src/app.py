"""

A small application to show a user interface for VAC, using Flask-MQTT.

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
app.config['MQTT_BROKER_URL'] = 'mosquitto'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
print('Configured MQTT IP Address: ' + app.config['MQTT_BROKER_URL'])

messages_recieved = {}
messages_old = {}
clock_start = 10
debug_level = 0 # 0 to hide debug prints, 1 to show them

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping/')
def ping():
    return messages_recieved

# MQTT / Socket IO functions

@socketio.on('connect')
def confirm_connect():
    if debug_level == 1:
        print('connected!')

@socketio.on('subscribe')
def handle_subscribe(data):
    mqtt.subscribe(data)

    if debug_level == 1:
        print('subscribed to {}!'.format(data))

@mqtt.on_message()
def handle_messages(client, userdata, message):
    global clock_start

    if debug_level == 1:
        print('Received message on topic {}: {}'.format(message.topic, message.payload.decode()))

    # before sending new message, decrement clock for older messages
    decrement_messages_clock()

    messages_recieved.update({message.topic: (message.payload.decode(), clock_start)})

    check_messages_clock()
    clean_messages_dict()
    clear_messages_old()

def decrement_messages_clock():
    for item in messages_recieved.items():
        clock = item[1][1]
        clock -= 1
        message = (item[1][0], clock)
        messages_recieved.update({item[0]: message})
        
        if debug_level == 1:
            print('\n updated clock for', item[0])

def check_messages_clock():
    for item in messages_recieved.items():
        topic = item[0]
        value = item[1]
        if value[1] <= 0:
            add_to_be_deleted({topic: value})

def clean_messages_dict():
    if len(messages_old) > 0:
        # if messages_old not empty remove each key of messages_old, from messages_recieved
        for item in messages_old.items():
            topic = item[0]
            delete_dict_topic(str(topic))
    else:
        if debug_level == 1:
            print("nothing deleted")

def add_to_be_deleted(item):
    messages_old.update(item)

def delete_dict_topic(topic):
    messages_recieved.pop(topic)

def clear_messages_old():
    messages_old.clear()

handle_subscribe('test/pls')
handle_subscribe('test/hey')

# to be activated when using definitive mqtt broker URL
# handle_subscribe('hermes/handler/#')
# handle_subscribe('hermes/button/#')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)