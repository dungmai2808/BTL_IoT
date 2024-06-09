from datetime import datetime, timedelta
from my_task import *

class RNodeScheduler:
    def __init__(self, data):
        self.name = data['name']
        startTime = datetime.strptime(data['startTime'], "%Y-%m-%d %H:%M") #xu ly bien thoi gian
        self.startTime = startTime
        self.cycle = data['cycle']
        self.mixer1 = data['mixer1']
        self.mixer2 = data['mixer2']
        self.mixer3 = data['mixer3']
        self.area = data['area']
        self.type = "relay"
        self.next = None
        self.task = Relay_Task(self.mixer1, self.mixer2, self.mixer3, 
                               self.area, self.cycle, self.startTime)
        
class SNodeScheduler:
    def __init__(self, name, startTime):
        self.name = name
        self.type = "sensor"
        self.startTime = startTime
        self.next = None
        self.task = Sensor_Task()

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, nodeSch):
        if not self.head:  # Empty list
            self.head = nodeSch
            self.tail = nodeSch
            return

        if nodeSch.startTime < self.head.startTime:  # At head of the list
            nodeSch.next = self.head
            self.head = nodeSch
            return

        currentSch = self.head
        while currentSch.next and nodeSch.startTime >= currentSch.next.startTime:
            currentSch = currentSch.next

        if not currentSch.next:  # At tail of the list
            self.tail.next = nodeSch
            self.tail = nodeSch
        else:  # At middle of the list
            nodeSch.next = currentSch.next
            currentSch.next = nodeSch


    def isAvailable(self, nameSch):
        if not self.head: # Empty list
            return False
        
        currentSch = self.head
        while currentSch:
            if currentSch.name == nameSch:
                return True
            currentSch = currentSch.next
        return False
    
    def findFirst(self, type):
        if not self.head: # Empty list
            return None
        
        currentSch = self.head
        while currentSch:
            if currentSch.type == type:
                return currentSch
            currentSch = currentSch.next
        return None

    def delete(self, nameSch):
        if not self.head: # Empty list
            return

        if self.head.name == nameSch:  # At head of the list
            self.head = self.head.next
            if not self.head:
                self.tail = None
            return

        currentSch = self.head
        while currentSch.next and currentSch.next.name != nameSch:
            currentSch = currentSch.next

        if currentSch.next and currentSch.next.name == nameSch:
            if currentSch.next == self.tail:  # At tail of the list
                self.tail = currentSch
                currentSch.next = None
            else:
                currentSch.next = currentSch.next.next

    def print_list(self):
        current_node = self.head
        while current_node:
            print(current_node.name, end=" ")
            print(current_node.startTime, end=" ")
            print(current_node.type, end=" ")
            if current_node.type == "relay":
                print(current_node.cycle, end=" ")
                print(current_node.mixer1, end=" ")
                print(current_node.mixer2, end=" ")
                print(current_node.mixer3, end=" ")
                print(current_node.area, end=" ")
            print("---")
            current_node = current_node.next

# current_time = datetime.now()
# print("Current time is:", current_time)

# next_day = current_time + timedelta(days=1)
# print("Next day:", next_day)

# next_five_minutes = current_time + timedelta(minutes=5)
# print("Next five minutes:", next_five_minutes)