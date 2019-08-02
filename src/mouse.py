import sys
import csv
import time
import os
import collections
import copy
from collections import namedtuple
from enum import Enum
from enum import IntEnum

DELAY = 0.05

class Dir(IntEnum):
    right = 0
    up = 1
    left = 2
    down = 3
    
class State(Enum):
    start = 0
    search = 1
    reverse = 2
    stop = 3
    remember = 3

class Mouse(object):
    MAP = None        
    #------------------INIT------------------
    def __init__(self):
        self.memo = []
        #[x,y]
        self.pos = [0,0]
        self.lastPos = [0,0]
        #[Right, Up, Left, Down]
        self.curShell = ["", "", "", ""]
        self.dir = Dir.right
        self.state = State.start
    
    #------------------POS------------------
    def getPos(self):
        return self.pos
    
    #------------------OPPOSIT-DIR------------------
    def oppositDir(self):
        oDir = self.dir - 2
        if oDir < 0:
            oDir = 4 + oDir
        return oDir
    
    #------------------MEMORIZE------------------
    def memorize(self):
        x = self.pos[0]
        y = self.pos[1]
                
        #Set next shell with oppositDir
        if self.state == State.reverse:
            lastMemo = self.memo.pop()
            self.pos = lastMemo[0]
            self.curShell = lastMemo[1]
            if len(self.memo) == 0 or "C" in self.curShell:
                self.curShell[self.oppositDir()] = "#"
            self.state = State.search
        else:
            self.curShell[self.dir] = "p"
            self.memo.append([[x,y],self.curShell])
            
            self.curShell = ["", "", "", ""]
            self.curShell[self.oppositDir()]= "C"
            self.lastPos = [x, y]
    #------------------CHECK-IN-MEMORY------------------
    def checkInMemory(self, newPos):
        x = newPos[0]
        y = newPos[1]
        
        for memo in self.memo:
            _pos = memo[0]
            if _pos[0] == x and _pos[1] == y:
                _shell = memo[1]
                _shell[self.oppositDir()] = "#"
                return 1
        return 0
            
    #------------------START-REVERSE------------------
    def startReverse(self):
        self.state = State.reverse
        emptyDir = self.getEmptyDir()
        if emptyDir < 0:
            self.state = State.stop
            print("Mouse didn't found out :(")
            return
        self.dir = emptyDir
        
    #------------------GET-EMPTY-DIR------------------
    def getEmptyDir(self):
        if self.state == State.reverse:
            if "C" in self.curShell:
                return self.curShell.index("C")
            return -1     
        elif self.state == State.remember:
            if "S" in self.curShell:
                return self.curShell.index("S")
            return -1
        else:
            if "" not in self.curShell:
                return -1
            return self.curShell.index("")
    
    #------------------GET-EMPTY-DIR------------------
    def hasVisited(self):
        return self.curShell[self.dir] == "#"
    
    #------------------SEARCH------------------
    def searchPath(self):
        x = self.pos[0]
        y = self.pos[1]
        map = list(Mouse.MAP)
        if map != None:
            arrLen = len(map[0])
            arrHeig = len(map)
        
            if map[y][x] == 'w':
                self.state = State.stop
                print("Mouse found out the way out!")
                return
            else:
                self.move()
                return
        else:
            mouse.state = State.stop
            print("No map")
            return
    
    #------------------MOVE------------------
    def move(self):
        x = self.pos[0]
        y = self.pos[1]
        _x = None
        _y = None
        
        if self.dir == Dir.right:
            _x = x+1
        elif self.dir == Dir.up:
            _y = y-1
        elif self.dir == Dir.left:
            _x = x-1
        elif self.dir == Dir.down:
            _y = y+1
        
        if _x != None:
            #Right/Left
            self.moveHorizontal(_x)
        elif _y != None:
            #Up/Down
            self.moveVertical(_y)
    
    #------------------MOVE-HORIZONTAL------------------
    def moveHorizontal(self, _x):
        x = self.pos[0]
        y = self.pos[1]
        
        map = list(Mouse.MAP)
        arrLen = len(map[0])
        arrHeig = len(map)
        
        if _x == self.lastPos[0] and y == self.lastPos[1]:
            if self.state == State.reverse:
                self.memorize()
            else:
                self.dir = Dir(emptyDir)
        else:
            if _x == arrLen or _x < 0:
                self.curShell[self.dir] = "S"
                emptyDir = self.getEmptyDir()
                if emptyDir < 0:
                    self.startReverse()
                    self.memorize()
                    return
                self.dir = Dir(emptyDir)
            else:  
                if map[y][_x] != "#":
                    if self.checkInMemory([_x, y]):
                        if self.curShell[self.dir] != "C":
                            self.curShell[self.dir] = "#"
                        emptyDir = self.getEmptyDir()
                        if emptyDir < 0: 
                            self.startReverse()
                            self.memorize()
                            return
                        self.dir = Dir(emptyDir)
                    elif self.hasVisited():
                        emptyDir = self.getEmptyDir()
                        if emptyDir < 0:
                            self.startReverse()
                            self.memorize()
                            return
                        self.dir = emptyDir
                    else:
                        self.memorize()
                        self.pos[0] = _x
                else:
                    self.curShell[self.dir] = "#"
                    emptyDir = self.getEmptyDir()
                    if emptyDir < 0:
                        self.startReverse()
                        self.memorize()
                        return
                    self.dir = Dir(emptyDir)
        
    #------------------MOVE-VERTICAL------------------
    def moveVertical(self, _y):
        x = self.pos[0]
        y = self.pos[1]
        
        map = list(Mouse.MAP)
        arrLen = len(map[0])
        arrHeig = len(map)
        
        
        if x == self.lastPos[0] and _y == self.lastPos[1]:
            if self.state == State.reverse:
                self.memorize()
            else:
                self.dir = Dir(emptyDir)
        else:
            if _y == arrHeig or _y < 0:
                self.curShell[self.dir] = "S"
                emptyDir = self.getEmptyDir()
                if emptyDir < 0:
                    self.startReverse()
                    self.memorize()
                    return
                self.dir = Dir(emptyDir)
            else:
                if map[_y][x] != "#":
                    if self.checkInMemory([x, _y]):
                        if self.curShell[self.dir] != "C":
                            self.curShell[self.dir] = "#"
                        emptyDir = self.getEmptyDir()
                        if emptyDir < 0: 
                            self.startReverse()
                            self.memorize()
                            return
                        self.dir = Dir(emptyDir)
                    elif self.hasVisited():
                        emptyDir = self.getEmptyDir()
                        if emptyDir < 0:
                            self.startReverse()
                            self.memorize()
                            return
                        self.dir = emptyDir
                    else:
                        self.memorize()
                        self.pos[1] = _y
                else:
                    self.curShell[self.dir] = "#"
                    emptyDir = self.getEmptyDir()
                    if emptyDir < 0:
                        self.startReverse()
                        self.memorize()
                        return
                    self.dir = Dir(emptyDir)

#------------------MAIN------------------
def main():
    #Init
    inputMap = sys.argv[1]
    mapping = doMapping(inputMap)
    m = Mouse()
    Mouse.MAP = list(mapping[0])
    
    repeat = 1
 
    m.spawn = copy.copy(mapping[1])
    m.pos = copy.copy(mapping[1])
    m.state = State.search
    
    spawnMouse(m, mapping, repeat, DELAY)
    
    
        
#------------------SPAWN-MOUSE------------------
def spawnMouse(m, mapping, repeat, delay):
    #Main loop
    start = time.time()
    while(m.state != State.stop):
        drawMap(m, list(mapping[0]))
        time.sleep(delay)
        m.searchPath()  
        
    #Stop
    end = time.time()
    print("Time spent {0}s".format(round(end-start,2)))
    _resultMap = resultMapping(m, list(Mouse.MAP))
    #print(m.memo)
    
    input("Press Enter to continue...")
    if repeat == 1:
        Mouse.MAP = list(_resultMap)
        m = Mouse()
        m.spawn = copy.copy(mapping[1])
        m.pos = copy.copy(mapping[1])
        m.state = State.remember
        
        inputMap = sys.argv[1]
        mapping = doMapping(inputMap)
        
        repeat = 0
        delay = 2 
        spawnMouse(m, mapping, repeat, delay)

#------------------DRAW-MAP------------------
def drawMap(mouse, map):
    os.system("cls")
    x = 0
    y = 0
    for row in map:
        _row = ""
        for shell in row:
            if mouse.pos[0] == x and mouse.pos[1] == y:
                if mouse.dir == Dir.right:
                    _row += ">"
                elif mouse.dir == Dir.up:
                    _row += "^"
                elif mouse.dir == Dir.left:
                    _row += "<"
                elif mouse.dir == Dir.down:
                    _row += "v"
            else:
                _row += shell
            x += 1
        y += 1
        x = 0
        print(_row)
    print("Pos{0} | Dir[{1}] | State[{2}] ".format(mouse.pos, mouse.dir, mouse.state.name))
    print("curShell{0}".format(mouse.curShell))
    print("lastPos{0}".format(mouse.lastPos))
    print("memo size {0}".format(len(mouse.memo)))
    #print("memo {0}".format(mouse.memo))
            
#------------------MAPPING------------------ 
def doMapping(map):
    _map = [[]]
    _spawn = [0,0]
    i = 0
    j = 0
    with open(map, encoding = 'utf-8', mode='r') as file:
        coordinates = str(file.read()).split(",")
        for shell in coordinates:
            if 'm' in shell:
                _shell = shell.split("\n")
                index = _shell.index('m')
                _spawn = [i+index,j]
            if '\n' in shell:
                _shell = shell.split("\n")
                _map[j].append(_shell[0])
                j += 1
                i = 0
                _map.append([])
                shell = _shell[1]
            _map[j].append(shell)
            i += 1
    return [_map, _spawn]

#------------------RESULT-MAPPING------------------ 
def resultMapping(mouse, map):
    memo = mouse.memo
    spawn = mouse.spawn
    i = 0
    j = 0
    for mapRow in map:
        for shell in mapRow:
            for shellInMemo in memo:
                pos = shellInMemo[0]
                curShell = shellInMemo[1]
                if pos[0] == i and pos[1] == j:
                    mapRow[i] = "S"
                    if i == spawn[0] and j == spawn[1]:
                        mapRow[i] = "m" 
            i += 1
        j += 1
        i = 0
        for _shell in mapRow:
            if _shell == "p":
                mapRow[i] = "#"
            i += 1
        i = 0
        print(mapRow)
    return map

if __name__ == "__main__":
    main()