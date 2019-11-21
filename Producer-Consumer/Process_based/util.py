def wait(buff, i):
    while buff[i] <= 0:
        pass
    buff[i] -= 1

def signal(buff, i):
    buff[i] += 1
