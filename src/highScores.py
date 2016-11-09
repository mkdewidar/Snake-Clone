# High Scores
#
# module allows management of high scores through a high_scores dat file

# created by MKD

import shelve

def initScores(levels):
    """Checks if file exits, otherwise creates new with number of shelves = 
    number of elements in tuple passed"""
    # try to open the file normally,
    # can't use shelf since it doesn't throw error but overites
    try:
        scores = open("high_scores.dat", "r")
    except FileNotFoundError:
        # if FileNotFoundError exception is thrown
        # create a new file and put empty leaderboards in it 
        scores = shelve.open("high_scores", "n")
        emptyTable = [("-----", 0),
                      ("-----", 0),
                      ("-----", 0),
                      ("-----", 0),
                      ("-----", 0)]
        for level in levels:
            scores[level] = emptyTable
        scores.sync()
        
    scores.close()
    

def addNewScore(name, score, level):
    """Given a name and a score, it stores it in the list in the file for that level,
returns false if couldn't make it to top 5."""
    scores = shelve.open("high_scores", "c", writeback=True)
    # load all the high scores to memory
    highScores = scores[level]
    # add the new highscore to the list
    highScores += [(name, score)]

    # sort the list in descending order based on the score
    highScores.sort(key=lambda scoreEntry: scoreEntry[1], reverse=True)
    # if length is greater than 5 remove last item
    if len(highScores) > 5:
        highScores.pop()
    
    scores.sync()

    scores.close()

def getScores():
    """Access's the high_scores file and returns all the scores"""
    scores = shelve.open("high_scores", "r")
    # the following piece of code makes a copy of the dictionary in the shelf
    allNames = list(scores.keys())
    allScores = list(scores.values())
    scoresCopy = {}
    for index in range (len(allNames)):
        scoresCopy[allNames[index]] = allScores[index]

    scores.close()
    
    return scoresCopy

if __name__ == "__main__":
    print("You are executing this file, It should be imported.")
    input("Press enter to close...")
