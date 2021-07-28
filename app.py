from time import sleep

day = hour = minute = second = 0

def init(light, sms):
    pass

def clock():
    global day, hour, minute, second
    second += 1
    if second == 60:
        second = 0
        minute += 1
    if minute == 60:
        minute = 0
        hour += 1
    if hour == 24:
        hour = 0
        day += 1

def attendance(crossRoad_id, nationalCode):
    pass
