# Project VAC
## Table of contents

## About
This project was **started on** July 4th, 2022.  
**Last tested on**: July 28th, 2022.  
**OS and versions:**
* **Raspberry Pi**: Raspberry Pi OS with desktop (release date April 4th 2022)
    * System: 64-bit
    * Kernel version: 5.15
    * Debian version: 11 (bullseye)
* **Server for the NLU / Intent handling / UI**: laptop running on Windows 10.

(not tested on MacOS)

[Checkout our page!](https://osoc22.github.io/project-hey-bosa/)

### The team
* Ana Gagua - *User Experience Researcher*
* Aurore Van Hoorebeke - *Full Stack developer*
* Frederik Stroobandt - *IOT specialist*
* Erinn Van Der Sande - *NLU expert*
### Coaches
* Bavo Lodewyckx
* Inti Valderas Caro
* Miel Van Opstal

### Made possible by
* [BOSA Digital Transformation Office](https://bosa.belgium.be/)
* [IO](https://www.iodigital.com/)
* [Dalberg Data Insights](https://dalberg.com/what-we-do/dalberg-data-insights/)
## Setup
### Hardware
* 1 Raspberry PI
* A USB headset
* A button to activate the bot
### Software
* **Raspberry**:  
    * Run this commmand in your terminal 
    ```
    docker run -it     -p 12101:12101     -v "$HOME/.config/rhasspy/profiles:/profiles"     --device /dev/snd     rhasspy/rhasspy     --profile en     --user-profiles /profiles^
    ```
* **Server-side**:
    * Install [Docker](https://www.docker.com/get-started/)
    * In the project folder, run `docker compose up`
    * You can find the different web interfaces to these adresses:
        * `http://localhost:5000/` (UI reacting to mqtt messages)
        * `http://localhost:12101/` (Rhasspy web interface)

## Current implementation
### Architecture overview
![Architecture diagram](documentation/architecture.drawio.svg)
* There are three hardware components which contain different parts of software.
    * **Raspberry Pie** The raspberry pie handles the **audio** (input and output) and wakeword of rhasspy communicating everything to an **external** mqtt broken (the current one is running on the server)
    * **Server** The server does all the hard work. It takes the audio from the raspberry pie and creates the **text** using **kaldi** (through Rhasspy). It gives the text to **rasa** to get the **intent** (Through Rhasspy). The **handler** will take this and guide the **conversation** (over mqtt).
    * **Arduino** The arduino acts as a medium to pass on the **button** signal. It sends the mqtt broker that the button has been pressed down.
### Rhasspy (Voice assistant)
#### Configuration
In the repository you can find 3 files in the 
``config/rhasspy/profiles/en/`` folder.

### Speech To Text
The speech to text system we use is called kaldi.
It trains a model using the ``sentences.ini`` file.
This follows the syntax from the [rhasspy documentation](https://rhasspy.readthedocs.io/en/latest/training/).

### NLU (Rasa)
The rasa model will train using the ``sentences.ini`` file. 
This follows the syntax from the [rhasspy documentation](https://rhasspy.readthedocs.io/en/latest/training/).

### TTS
For text to speech we use NanoTTS which is the recommended system of Rhasspy.

### Intent handling
The intent handler is a python script which is subscribed to some MQTT topics.
The intent handler uses a conversation data structure to guide the conversation.
The structure allows or different components to be added.
Rhasspy can add text, send a message over MQTT or give the user a choice.
This is extendible using the ``ConversationComponent`` class.
It has a ``on_entry``, ``to_leave``, ``leave_path``, ``not_leave`` and ``on_leave``.
The ``on_entry`` will send out an MQTT messages when the node is entered.
The ``to_leave``, ``leave_path`` and ``not_leave`` contain topics that will decide down which path the conversation will go.
The ``on_leave`` shows which MQTT messages to send when a node is left.
### UI

## Known Issues
* **Security**: while this assistant is meant to be working offline/using a local network, there might be some security concerns. While the hackathon, we assumed the local network the project is running on is correctly protected.

## Future work
Making an amazing product takes time, more time than a hackaton allows.  
You'll find here the ideas we had for the future of the product.

### Hardware
* The project is currently running with a headset for voice input and output. However, this could be changed using a *ReSpeaker* on a *Raspberry PI 3* for the microphone and a simple speaker to hear the bot's answer.
### Rhasspy (Voice assistant)
#### Configuration

### NLU (Rasa)

### TTS / STT

### Handler

### Intent handling
* Currently, we use a button to trigger the conversation with the user. It can easily be replaced with a wake word. For coherence, the mqtt topic `hermes/button/start` and `hermes/button/stop` could be renamed.
### UI
* Replace images shown with actual HTML and CSS.
* When the list is shown on the screen, hide or change the color of the list items already chosen by the user to make the remaining choices stand out more.
