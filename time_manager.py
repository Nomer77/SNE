import datetime


def now_sec_time():
    return datetime.datetime.now().hour * 3600 + datetime.datetime.now().minute * 60


def find_time(task):
    text = task.strip()
    nums = '1234567890'
    pos = text.find(':', len(text) - 5, len(text) - 1)
    try:
        if (pos != -1) and (text[pos - 1] in nums) and (text[pos + 1] in nums) and (text[pos + 2] in nums):
            try:
                a = int(text[pos - 2].strip())
            except ValueError:
                a = 0
            b = int(text[pos - 1])
            c = int(text[pos + 1])
            d = int(text[pos + 2])
            time = (a * 10 + b) * 3600 + (c * 10 + d) * 60
            if time > (now_sec_time()):
                return time
    except IndexError:
        pass
    return None



