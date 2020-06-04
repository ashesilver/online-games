import socket
### Main client specs
"""
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("tters66.freeboxos.fr", 19999))
response = None
while response == None:
    s.recv(128)
print("connected to server !")"""
#socket exemple
"""
msg = s.recv(1024)
print(msg.decode("utf-8"))"""


def clean_console(func):
    import os
   
    def wrapper(*args,**kwargs):
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")
        result = func(*args,**kwargs)
        return result
    
    return wrapper

def var(*str):
    res =[]
    for x in str :
        try :
            res.append(globals()[x])
        except KeyError:
            globals()[x]=None
            res.append(globals()[x])
    return res

@clean_console
def input_type(func,reset=False):
    if reset :
        print("not a valid answer !\n")
    choice = input("what input type would you like to use ? ( A1 format or Numpad keys )\n  ")
    if "keys" in choice.lower() or "numpad" in choice.lower() :
        def wrapper(*args,**kwargs):
            kwargs['numpad'] = True
            result = func(*args,**kwargs)
            return result
    elif "a1" in choice.lower() or "format" in choice.lower() :
        def wrapper(*args,**kwargs):
            result = func(*args,**kwargs)
            return result
    else :
        wrapper = input_type(func,reset=True)
    return wrapper

@clean_console
def draw(grid):
    print(" / 1   2   3 \\\nA: {} | {} | {}\n  ___ ___ ___\n\nB: {} | {} | {}\n  ___ ___ ___\n\nC: {} | {} | {}".format(*tuple(grid)))

@clean_console
def beatiful_soup(str):
    print(str)


@input_type
def play(player,grid,numpad=False):
    fullslots = [[l,n] for l in ["A","B","C"] for n in ["1","2","3"]]
    if numpad :
        fullslots = [x for x in range(1,10)]
    freeslots = [x for x in fullslots if grid[fullslots.index(x)] is " "]
    selected = ask(player,freeslots);formal_answer = selected.upper()
    try:
        if numpad :
            selected = [ x for x in freeslots if str(x) in formal_answer ][0]
        else :
            selected = [ x for x in freeslots if x[0] in formal_answer and x[1] in formal_answer ][0]
    except IndexError:
        draw(grid)
        print(selected,"is no valid placement, please retry (format : {})".format("numpad integer" if numpad else "A1"))
        grid = play(player,grid)
    else :
        grid[fullslots.index(selected)] = var("player_{}".format(player))[0]
    finally :
        return grid[:]
    
def ask(player,freeslots):
    return input("player {}'s turn, select a slot : {}\n  ".format(player,freeslots))

def grid_pack(l):
    s=""
    for x in l :
        s+=x
    return s

def grid_unpack(s):
    return list(s)

def await_data_from_server(s):
    running = True
    data=bytearray()
    while running:
        data.extend(s.recv(1))
        if ("-TRover-" in data.decode("utf-8")) :
            running =False
            data = data.decode("utf-8")
    return data[:-8]

if __name__ == '__main__':
    var("empty", "player_1", "player_2")
    empty = " "; player_1 = "X"; player_2 = "O"

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("tters66.freeboxos.fr", 19999))

    response = None
    try:
        while response == None:
            response = await_data_from_server(s)
    except ConnectionResetError:
        s.close()

    s = None
    print(f"conneting to port {response}")

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("tters66.freeboxos.fr", int(response)))
    response = None
    while response == None:
        response = await_data_from_server(s)
    print(f"connected to server !\n{response}")

    data = None
    while data!="END" :
        data = await_data_from_server(s)
        if data.startswith("GRID") :
            grid = grid_unpack(data[4:])
        elif data.startswith("DRAW"):
            draw(grid)
        elif data.startswith("PLAY"):
            grid = play(int(data[4]),grid_unpack(data[5:]))
            s.send(bytes("GRID"+ grid_pack(grid)+"-TRover-","utf-8"))
        elif data.startswith("AWAIT"):
            draw(grid)
            print("Awaiting for your opponent to play")
        elif data.startswith("RES"):
            beatiful_soup(data[3:])

    s.close()


input("press enter to close the PyVM")