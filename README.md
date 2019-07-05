# Mouse-Maze

## Credits

#### [TheHeroOfNoOne](https://github.com/EetuAaltonen)

## Characters

| Character  | Value              |
| -----------|:------------------:|
| m          | Spawn              |
| w          | Goal               |
| p          | Path               |
| #          | Wall               |
| C (memory) | Last location      |
| S (memory) | Out of array range |



## Requirements

[Python 3.6.x or newer](https://www.python.org/downloads/)

## Run mouse.py script

Add <map file name>.txt with valid map
    
Map must be square. Validator in progress.

> C:\location\>python mouse.py mapfile.txt  
> Ctrl + C to abord

## Example Map

```
w,p,#,#,p,p,p,p,#,p,p,p,#,#,#
#,p,p,#,p,#,#,p,#,p,#,p,p,p,p
#,#,p,p,p,#,#,p,p,p,#,#,#,#,p
#,#,#,#,p,#,#,#,#,#,#,#,#,#,#
#,#,#,#,p,#,#,#,p,p,p,p,p,p,p
#,#,#,#,p,#,#,#,p,#,#,#,#,#,#
#,#,#,#,p,#,#,#,p,#,p,#,#,#,#
#,#,#,#,p,#,#,#,p,#,p,#,#,#,#
#,#,#,#,p,#,#,#,p,#,p,#,#,#,#
#,#,#,#,p,p,m,p,p,p,p,#,#,#,#
#,#,#,#,#,#,#,#,#,#,#,#,#,#,#
```

## In Progess

* Map generator
* Lose condition
* Memory use when respawn
* Map rendering from memory when respawn

## News

---

> 2019-07-05 16.00pm: Mouse skills improved

---

> **2019-07-05 15.30pm: GitHub project created**
> Program featurs:
> * load map from .txt file
> * no map size limit
> * square map required
> * win condition

> Mouse Skills:
> * path finding
> * memory
> * out of map index recognizing

---
