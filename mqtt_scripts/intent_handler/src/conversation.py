import itertools
import networkx as nx
import random
from abc import ABC, abstractmethod

class Conversation():
    def __init__(self) -> None:
        self.conversation = nx.DiGraph()
        self.id = 2
        self.objects = {0:ConversationStart(),1:ConversationStop()}
        self.current = 0
        self.waiting_for = self.objects.get(0).to_leave()
        self.conversation.add_node(0)
        self.conversation.add_node(1)
    
    def get_current_component(self):
        return self.objects[self.current]

    def can_proceed(self) -> bool:
        return not(all(self.waiting_for))

    def proceed(self):
        idxs = [i for i, val in enumerate(self.waiting_for) if not val]
        print(idxs)
        idx = random.choice(idxs)
        old = self.get_current_component()
        paths = old.leave_path()[idx]
        possible_currents = []
        for (f, t, path) in self.conversation.edges.data('path', default='stop'):
            if f == self.current:
                if path == paths:
                    possible_currents.append(t)
        print(possible_currents)
        if possible_currents:
            self.current = random.choice(possible_currents)
        else:
            self.current = 0
        self.waiting_for = self.get_current_component().to_leave()
        return old,idx

    def remove(self,topic) -> bool:
        before_remove = len(list(itertools.chain(*self.waiting_for)))
        print(self.waiting_for)
        self.waiting_for = [list(filter(lambda condition: condition != topic,conditions)) for conditions in self.waiting_for]
        current = self.get_current_component()
        self.waiting_for = [val + ["block"] if topic in current.not_leave()[i] else val for i, val in enumerate(self.waiting_for)]
        print(self.waiting_for)
        return before_remove != len(list(itertools.chain(*self.waiting_for)))

    def add_say_text(self,text,origin,path = "default"):
        id = self.id
        self.id += 1
        self.conversation.add_node(id)
        self.conversation.add_edge(origin,id,path = path)
        self.objects.update({id:ConversationSay(text)})
        return id

    def add_exhaustive_choice(self,intents,origin,path = "default"):
        id = self.id
        self.id += 1
        self.conversation.add_node(id)
        self.conversation.add_edge(origin,id,path = path)
        self.objects.update({id:ConversationChoices(intents)})
        return id
    
class ConversationComponent(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def on_entry(self):
        pass
    
    @abstractmethod
    def to_leave(self):
        pass

    @abstractmethod
    def leave_path(self):
        pass
    
    @abstractmethod
    def not_leave(self):
        pass

    @abstractmethod
    def on_leave(self):
        pass

class ConversationStart(ConversationComponent):
    def __init__(self) -> None:
        super().__init__()
    
    def on_entry(self):
        return []
    
    def to_leave(self):
        return [["hermes/button/start"]]
        
    def not_leave(self):
        return [[]]

    def leave_path(self):
        return ["default"]

    def on_leave(self):
        return [[{"topic":"hermes/handler/conversation/start"}]]

class ConversationStop(ConversationComponent):
    def __init__(self) -> None:
        super().__init__()
    
    def on_entry(self):
        return []
    
    def to_leave(self):
        return [[]]

    def not_leave(self):
        return [[]]
    
    def leave_path(self):
        return ["default"]

    def on_leave(self):
        return [[{"topic":"hermes/handler/conversation/stop"}]]

class ConversationSay(ABC):
    def __init__(self,text) -> None:
        super().__init__()
        self.text = text
    
    def on_entry(self):
        return [{"topic":"hermes/tts/say","text":self.text,"siteId":"sattelite"}]
    
    def to_leave(self):
        return [["hermes/tts/sayFinished"]]

    def not_leave(self):
        return [[]]

    def leave_path(self):
        return ["default"]
    
    def on_leave(self):
        return [[]]

class ConversationChoices(ABC):
    def __init__(self,intents) -> None:
        super().__init__()
        self.intents = intents
    
    def on_entry(self):
        return [{
            "topic":"hermes/hotword/default/detected",
            "modelId": "default",
            "currentSensitivity": 1,
            "siteId": "sattelite"
            }]
    
    def to_leave(self):
        recognised = [[f"hermes/intent/{intent}"] for intent in self.intents]
        
        return recognised + [
            ["hermes/nlu/intentNotRecognized"],
            []
            ]
    
    def not_leave(self):
        recognised = [[] for _ in self.intents]

        return recognised + [
            [],
            [f"hermes/intent/{intent}" for intent in self.intents] + ["hermes/nlu/intentNotRecognized"]
        ]

    def leave_path(self):
        recognised = [intent for intent in self.intents]

        return recognised + [
            "notText",
            "notRelevant"
            ]

    def on_leave(self):
        recognised = [[] for _ in self.intents]
        return recognised + [
            [],
            []]

def create_conversation_graph():
    conversation = Conversation()
    greeting = conversation.add_say_text("Hello! I am vac. I can help you on what to do if you have seen or experienced sexual harrasment.",0)
    information = conversation.add_say_text("I can give you more information on the types of harassment displayed on the screen. About what form would you like to have more information.",greeting)
    choice = conversation.add_exhaustive_choice(["Verbal","Visual","Written","Physical"],information)
    conversation.add_say_text("verbal",choice,"Verbal")
    conversation.add_say_text("visual",choice,"Visual")
    conversation.add_say_text("written",choice,"Written")
    conversation.add_say_text("physical",choice,"Physical")
    return conversation
    """conversation.add_choices()
    conversation.add_say_text
    d = {
        1:"I can give you more information on the types of harassment displayed on the screen. About what form would you like to have more information.",
        2:"If someone verbally abuses you, try to involve friends,if they are not available record it and report it to the organisation or the police",
        3:"When someone is sending you inappropriate texts I would suggest you document it and report it to the organisation and/or police.",
        4:"If someone is making inappropriate gestures, first, let them know you don't feel comfortable and ask to stop if they don't respond, try to document it, report it to the organisation or the police",
        5:"If you see someone getting touched inappropriatly you can isolate the attacker by standing in front of the victim or distract them.",
        6:"",
    }"""