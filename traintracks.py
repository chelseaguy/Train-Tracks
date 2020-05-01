import time
from itertools import permutations
from collections import defaultdict

'''
This program solves the TrackTracks puzzles seen in The Times.
[With acknowledgement to Chris Walker https://github.com/thechriswalker
for the binary mask techique to set the direction of each piece of track.]

Guy Walker April 2020
'''

def isvalidcell(grid,x,y):
    # Check the next cells are within the permissible grid
    if any((x<0,y<0,x>numrows-1,y>numcols-1)):
        return False
    # Check if row and column totals are less or equal to their target
    if sum(1 for i in grid[x] if i>0)>rowtarget[x]:
        return False
    if sum(min(i[y],1) for i in grid)>coltarget[y]:
        return False
    # Check if cell is one of the given fixed pieces of track
    # and has the correct entry direction
    if (x,y) in otherpieces and \
       otherpieces[(x,y)]-grid[x][y] not in NESWcode.values():
        return False
    return True

def printtracks(grid):    
    for row in grid:
        print(''.join(piece[i] for i in row),
              ''.join(str(min(1,i)) for i in row),sep='     ')
    print('----------------------------')

def checkgrid(grid):
    # Check if all the given fixed pieces are in the right place
    if otherpieces and any(grid[k[0]][k[1]]!=v for k,v in otherpieces.items()):
        return False
    rtot=[0 for i in range(numrows)]
    ctot=[0 for i in range(numcols)]
    # Grid has direction codes rather than 1s and 0s, hence need to item count
    # all grid entries with a non-zero value, and then check they equal targets
    for i in range(numrows):
        for j in range(numcols):
          if grid[i][j]:
              rtot[i]+=1
              ctot[j]+=1
    if ctot==coltarget and rtot==rowtarget:
        return True
    return False

def findpaths(row,col,entrydir,visited):
    # Recusive function, takes current cell co-ordinates, the direction of entry
    # for that cell and the array of already visted cells, with each cell having
    # the direction code for the track used.
    global cnt
    visited[row][col]=NESWcode[entrydir]
    if [row,col]==endcell:
        # Reached the end cell, so need to set final exit direction as South
        visited[row][col]=NESWcode[entrydir]|NESWcode["South"]
        # Need to check if all column totals match their targets
        if checkgrid(visited):
            printtracks(visited)
        # This the count of the number of times reached end-cell, without
        # breaching the row/col totals, but not necessarily matching them
        cnt+=1        
        visited[row][col]=0
        return    
    if isvalidcell(visited,row,col):
        # Try South
        if row+1<numrows and not visited[row+1][col]:
            visited[row][col]=NESWcode[entrydir]|NESWcode["South"]
            findpaths(row+1,col,"North",visited)
        # Try North
        if row-1>=0 and not visited[row-1][col]:
            visited[row][col]=NESWcode[entrydir]|NESWcode["North"]
            findpaths(row-1,col,"South",visited)
        # Try East
        if col+1<numcols and not visited[row][col+1]:
            visited[row][col]=NESWcode[entrydir]|NESWcode["East"]
            findpaths(row,col+1,"West",visited)
        # Try West
        if col-1>=0 and not visited[row][col-1]:
            visited[row][col]=NESWcode[entrydir]|NESWcode["West"]
            findpaths(row,col-1,"East",visited)
    visited[row][col]=0
    return

t0=time.time()
'''
The encoding of the puzzle is as follows:
12-12345678-12345678-12SE

First two digits: row and column positions of the start and finish (1-based).
Note the given A "start-piece" is always in column 1, and the given B "end-
piece" is always in row 8.
The next 2 sequences of [8] numbers are the constraints for the column and row
totals. The programme should be able to deal with sizes other than the standard
8x8.

Optionally you can then specify fixed pieces, eg 12SE, indicating a piece in
row 1 col 1, orientation (ie entry and exit points) SE.
'''

puzzle="44-14134544-54234341-65ne"
puzzle="33-34422467-28222754"
puzzle="84-51256452-33575322-36WN"
puzzle="38-4413567232-7445441422-66EW"
puzzle="15-22337333-85231133"
puzzle="76-73124644-77442322-16se"
puzzle="47-43122463-46532212-36wn"
puzzle="18-21216674-47343134-36ne"
puzzle="78-34465452-44565531-46ws-56sn"
puzzle="13-11236454-53341145-36ns"
puzzle="74-31242874-24356443-47ew-77ew"
#puzzle="3A-7675543123-335478a3-61se-54se-76sn"


'''
Use a binary mask for the points of the compass to indicate the direcion of
each piece of track.  For each cell in the array "visited" we know the entry
point (NESW) and then try each compass point to find valid exit point (NESW).
The contents of the cell is the binary OR operator for these two compass points.
Hence entry from the West (value:8) and exit from East (value:4) would set
the value of the cell to 12 [8|4].
'''
NESWcode={"North":1,"South":2,"East":4,"West":8}
piece={0:" ",3:"┃",12:"━",5:"┗",9:"┛",6:"┏",10:"┓"}
dcode={x[0]+y[0]:NESWcode[x]|NESWcode[y]
       for x,y in permutations(NESWcode.keys(),2)}

# Create an array of the various input criteria
x=puzzle.split('-')
numcols=len(x[1])
numrows=len(x[2])
print(puzzle.upper())
print('Gridsize = {} rows x {} columns.'.format(numrows,numcols))

startcell=[int(x[0][0],16)-1,0]
endcell=[numrows-1,int(x[0][1],16)-1]
coltarget=[int(i,16) for i in x[1]]
rowtarget=[int(i,16) for i in x[2]]
cnt=0
# Create dictionary for the fixed pieces in the grid
# with key: co-ordinates, value: directional code, eg EW=12
otherpieces={(int(x[i][0],16)-1,int(x[i][1],16)-1):dcode[x[i][2:].upper()]
             for i in range(3,len(x))}
# Initialise nested array which will store the direction code of the track pieces
visited=[[0 for i in range(numcols)] for j in range(numrows)]
# Start recursion solving process, initial entry is from the West of the starting cell
findpaths(startcell[0],startcell[1],"West",visited)

print('Number of sub-optimal paths {}'.format(cnt))
print('{0:.3f} seconds'.format(time.time()-t0))
