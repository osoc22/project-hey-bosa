import json
import conversation
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    """Called when connected to MQTT broker."""
    client.subscribe("hermes/intent/#")
    client.subscribe("hermes/nlu/intentNotRecognized")
    client.subscribe("hermes/tts/sayFinished")
    client.subscribe("hermes/button/#")
    print("Connected. Waiting for intents to handle.",flush = True)


def on_disconnect(client, userdata, flags, rc):
    """Called when disconnected from MQTT broker."""
    client.reconnect()

def on_message(client, userdata, msg):
    """Called each time a message is received on a subscribed topic."""
    if current_conversation.remove(msg.topic):
        print(current_conversation.can_proceed())
        if current_conversation.can_proceed():
            old,idx = current_conversation.proceed()
            for publish in old.on_leave()[idx]:
                client.publish(publish.get("topic"), json.dumps({k: v for k, v in publish.items() if v != "topic"}))
            for publish in current_conversation.get_current_component().on_entry():
                client.publish(publish.get("topic"), json.dumps({k: v for k, v in publish.items() if v != "topic"}))

current_conversation = conversation.create_conversation_graph()

# Create MQTT client and connect to broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect("mosquitto", 1883)
client.loop_forever()