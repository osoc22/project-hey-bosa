import json
import conversation
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    """Called when connected to MQTT broker."""
    client.subscribe("hermes/intent/#")
    client.subscribe("hermes/nlu/intentNotRecognized")
    client.subscribe("hermes/tts/sayFinished")
    client.subscribe("hermes/button/#")
    client.subscribe('hermes/dialogueManager/sessionEnded')
    client.subscribe('hermes/dialogueManager/sessionStarted')
    print("Connected. Waiting for intents to handle.",flush = True)


def on_disconnect(client, userdata, flags, rc):
    """Called when disconnected from MQTT broker."""
    client.reconnect()

def on_message(client, userdata, msg):
    """Called each time a message is received on a subscribed topic."""
    global session_id
    if msg != "dummy":
        current_conversation.remove(msg.topic)
    if not(isinstance(msg,str)):
        if "hermes/dialogueManager/sessionStarted" == msg.topic:
            payload = json.loads(msg.payload)
            session_id = payload["sessionId"]
        if "intent" in msg.topic:
            client.publish("hermes/dialogueManager/endSession",json.dumps({"sessionId":session_id}))
    if current_conversation.can_proceed(): 
        old,idx = current_conversation.proceed()
        for publish in old.on_leave()[idx]:
            client.publish(publish.get("topic"), json.dumps({k: v for k, v in publish.items() if k != "topic"}))
        for publish in current_conversation.get_current_component().on_entry():
            client.publish(publish.get("topic"), json.dumps({k: v for k, v in publish.items() if k != "topic"}))
        on_message(client,userdata,"dummy")
current_conversation = conversation.create_conversation_graph()
session_id = ""
# Create MQTT client and connect to broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect("mosquitto", 1883)
client.loop_forever()