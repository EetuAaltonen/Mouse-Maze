import sys
import csv
import time
import os
import collections
from collections import namedtuple
from enum import Enum
from enum import IntEnum

MapData = collections.namedtuple('Mapdata', 'map spawn')
delay = 2

class Dir(IntEnum):
    right = 0
    up = 1
    left = 2
    down = 3
    
    def turnLeft(self):
        value = self.value
        value += 1
        if (value > 3):
            print(Dir.right)
            return Dir.right
        return Dir(value)
    
    def turnRight(self):
        value = self.value
        value -= 1
        if value < 0:
            return Dir.down
        return Dir(value)
    
class State(Enum):
    start = 0
    search = 1
    reverse = 2
    stop = 3

class Mouse(object):
    map = None        
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
    
    #------------------SEARCH------------------
    def searchPath(self):
        x = self.pos[0]
        y = self.pos[1]
        map = Mouse.map
        if map != None:
            arrLen = len(map[0])
            arrHeig = len(map)
        
            if map[y][x] == 'w':
                self.state = State.stop
                return
            else:
                if self.dir == Dir.right:
                    self.moveRight()
                #------------------UP------------------
                elif self.dir == Dir.up:
                    self.moveUp()
                #------------------LEFT------------------
                elif self.dir == Dir.left:
                    self.moveLeft()
                #------------------DOWN------------------
                elif self.dir == Dir.down:
                    self.moveDown()
                return
        else:
            mouse.state = State.stop
            print("No map")
            return
    
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
            self.curShell = lastMemo[1]
            self.pos = lastMemo[0]
            if len(self.memo) == 0:
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
        self.dir = self.getEmptyDir()
        
    #------------------GET-EMPTY-DIR------------------
    def getEmptyDir(self):
        if self.state == State.reverse:
            index = self.curShell.index("C")
        else:
            if "" not in self.curShell:
                return -1
            index = self.curShell.index("")
        return index
        
    #------------------RIGHT------------------
    def moveRight(self):
        x = self.pos[0]
        y = self.pos[1]
        _x = x+1
        
        map = Mouse.map
        arrLen = len(map[0])
        arrHeig = len(map)
        
        emptyDir = self.getEmptyDir()
        if emptyDir < 0:
            self.startReverse()
            return
        
        if _x == self.lastPos[0] and y == self.lastPos[1]:
            if self.state == State.reverse:
                self.memorize()
            else:
                self.dir = Dir(emptyDir)
        else:
            if _x == arrLen:
                self.curShell[self.dir] = "S"
                emptyDir = self.getEmptyDir()
                self.dir = Dir(emptyDir)
            else:  
                if map[y][_x] != "#":
                    if self.checkInMemory([_x, y]):
                        self.curShell[self.dir] = "#"
                        emptyDir = self.getEmptyDir()
                        if emptyDir < 0: 
                            return
                        self.dir = Dir(emptyDir)
                    else:
                        self.memorize()
                        self.pos[0] = _x
                else:
                    self.curShell[self.dir] = "#"
                    emptyDir = self.getEmptyDir()
                    if emptyDir < 0:
                        return
                    self.dir = Dir(emptyDir)
    
    #------------------UP------------------
    def moveUp(self):
        x = self.pos[0]
        y = self.pos[1]
        _y = y-1
        
        map = Mouse.map
        arrLen = len(map[0])
        arrHeig = len(map)
        
        emptyDir = self.getEmptyDir()
        if emptyDir < 0:
            self.startReverse()
            return
        
        if x == self.lastPos[0] and _y == self.lastPos[1]:
            if self.state == State.reverse:
                self.memorize()
            else:
                self.dir = Dir(emptyDir)
        else:
            if _y == arrHeig:
                self.curShell[self.dir] = "S"
                emptyDir = self.getEmptyDir()
                self.dir = Dir(emptyDir)
            else:
                if map[_y][x] != "#":
                    if self.checkInMemory([x, _y]):
                        self.curShell[self.dir] = "#"
                        emptyDir = self.getEmptyDir()
                        if emptyDir < 0: 
                            return
                        self.dir = Dir(emptyDir)
                    
                    self.memorize()
                    self.pos[1] = _y
                else:
                    self.curShell[self.dir] = "#"
                    emptyDir = self.getEmptyDir()
                    if emptyDir < 0:
                        return
                    self.dir = Dir(emptyDir)
    #------------------LEFT------------------
    def moveLeft(self):
        x = self.pos[0]
        y = self.pos[1]
        _x = x-1
        
        map = Mouse.map
        arrLen = len(map[0])
        arrHeig = len(map)
        
        emptyDir = self.getEmptyDir()
        if emptyDir < 0:
            self.startReverse()
            return
        
        if _x == self.lastPos[0] and y == self.lastPos[1]:
            if self.state == State.reverse:
                self.memorize()
            else:
                self.dir = Dir(emptyDir)
        else:
            if _x < 0:
                self.curShell[self.dir] = "S"
                emptyDir = self.getEmptyDir()
                self.dir = Dir(emptyDir)
            else:
                if map[y][_x] != "#":
                    if self.checkInMemory([_x, y]):
                        self.curShell[self.dir] = "#"
                        emptyDir = self.getEmptyDir()
                        if emptyDir < 0: 
                            return
                        self.dir = Dir(emptyDir)
                    
                    self.memorize()
                    self.pos[0] = _x
                else:
                    self.curShell[self.dir] = "#"
                    emptyDir = self.getEmptyDir()
                    if emptyDir < 0:
                        return
                    self.dir = Dir(emptyDir)
    #------------------DOWN------------------
    def moveDown(self):
        x = self.pos[0]
        y = self.pos[1]
        _y = y+1
        
        map = Mouse.map
        arrLen = len(map[0])
        arrHeig = len(map)
        
        emptyDir = self.getEmptyDir()
        if emptyDir < 0:
            self.startReverse()
            return
        
        if x == self.lastPos[0] and _y == self.lastPos[1]:
            if self.state == State.reverse:
                self.memorize()
            else:
                self.dir = Dir(emptyDir)
        else:
            if _y == arrHeig:
                self.curShell[self.dir] = "S"
                emptyDir = self.getEmptyDir()
                self.dir = Dir(emptyDir)
            else:
                if map[_y][x] != "#":
                    if self.checkInMemory([x, _y]):
                        self.curShell[self.dir] = "#"
                        emptyDir = self.getEmptyDir()
                        if emptyDir < 0: 
                            return
                        self.dir = Dir(emptyDir)
                    
                    self.memorize()
                    self.pos[1] = _y
                else:
                    self.curShell[self.dir] = "#"
                    emptyDir = self.getEmptyDir()
                    if emptyDir < 0:
                        return
                    self.dir = Dir(emptyDir)

#------------------MAIN------------------
def main():
    #Init
    start = time.time()
    inputMap = sys.argv[1]
    _mapping = mapping(inputMap)
    Mouse.map = _mapping.map
    m = Mouse()
    m.pos = _mapping.spawn
    m.state = State.search
    
    #Main loop
    while(m.state != State.stop):
        drawMap(m)
        time.sleep(delay)
        m.searchPath()
    
    #Stop
    end = time.time()
    print("Mouse found out!")
    print("Time spent {0}s".format(round(end-start,2)))
    #drawMemo(m)
    print(m.memo)

#------------------DRAW-MAP------------------
def drawMap(mouse):
    os.system("cls")
    map = Mouse.map
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
    print("memo size {0}".format(len(mouse.memo)))
    print("memo {0}".format(mouse.memo))

#------------------DRAW-MEMO------------------
def drawMemo(mouse):
    map = mouse.memo
    x = 0
    y = 0
    for row in map:
        _row = ""
        for shell in row:
            print(shell)
            x += 1
        y += 1
        x = 0
        print("{0}".format(_row))
            
#------------------MAPPING------------------ 
def mapping(map):
    _map = [[]]
    _spawn = [0,0]
    i = 0
    j = 0
    with open(map, encoding = 'utf-8', mode='r') as file:
        coordinates = str(file.read()).split(",")
        print(coordinates)
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
            
    return MapData(map=_map, spawn=_spawn)
if __name__ == "__main__":
    main()