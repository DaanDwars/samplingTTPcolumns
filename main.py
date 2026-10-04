import datetime
import math
# import json
# import numpy as np
import random
import time
import csv


def checkMaxStreakViolations(column, maxStreak):
    maxStreakViolations = []
    nMaxStreakViolations = 0

    plusMin = 0
    if column[0] < 0:
        plusMin = -1
    else:
        plusMin = 1

    for row in range(1, len(column)):
            if column[row] < 0 and plusMin < 0:
                plusMin = plusMin - 1
            if column[row] > 0 and plusMin > 0:
                plusMin = plusMin + 1

            if column[row] < 0 and plusMin > 0:
                if abs(plusMin) > maxStreak:
                    nMaxStreakViolations = nMaxStreakViolations + (abs(plusMin) - maxStreak)
                    maxStreakViolations.append(str(row) + " Streaksize: " + str(abs(plusMin)))
                plusMin = -1

            if column[row] > 0 and plusMin < 0:
                if abs(plusMin) > maxStreak:
                    nMaxStreakViolations = nMaxStreakViolations + (abs(plusMin) - maxStreak)
                    maxStreakViolations.append(str(row) + " Streaksize: " + str(abs(plusMin)))
                plusMin = 1

            if row == len(column) - 1:
                if abs(plusMin) > maxStreak:
                    nMaxStreakViolations = nMaxStreakViolations + (abs(plusMin) - maxStreak)
                    maxStreakViolations.append(str(column) + "," + str(row) + " Streaksize: " + str(abs(plusMin)))

    return nMaxStreakViolations, maxStreakViolations


def checkNoRepeatViolations(column):
    noRepeatViolations = []
    nNoRepeatViolations = 0

    for row in range(1, len(column)):
        if abs(column[row]) == abs(column[row - 1]):
            nNoRepeatViolations = nNoRepeatViolations + 1
            noRepeatViolations.append(row)
    return nNoRepeatViolations, noRepeatViolations



def makeColumnRandomPermutation(nTeams):
    newColumn = [0]*(nTeams * 2 - 2)

    # first, make a list of all opponents to be placed
    opponents = []
    for teamNr in range(1, nTeams):
        opponents.append(teamNr)
        opponents.append(-teamNr)
    random.shuffle(opponents)

    # put the opponents in the column, in random order
    for placement in range(0, len(newColumn)):
        newColumn[placement] = candidates[placement]

    return newColumn


def makeColumnAvoidNorepeat1(nTeams):
    # does the same as makeColumnAvoidNorepeat, except with neater code
    # create the column to be returned at the end of the function
    newColumn = [0] * (nTeams * 2 - 2)

    # make a list of the teams to be placed
    opponents = []
    for teamNr in range(1, nTeams):
        opponents.append(teamNr)
        opponents.append(-teamNr)
    random.shuffle(opponents)

    # the value '999999' signifies 'no banned opponent'
    bannedopponent = 999999

    #default: place the first opponent from the random list in the first slot
    newColumn[0] = opponents[0]
    opponents.remove(opponents[0])

    # fill all in the column, except the last
    for placement in range(1, len(newColumn)-1):

        # if the >opposite< game of the previously placed game is in opponents,
        # temporarily remove it ("ban" it) to prevent it from being placed.
        if -(newColumn[placement-1]) in opponents:
            bannedopponent = -(newColumn[placement-1])
            opponents.remove(bannedopponent)

        # if there are still opponents for placement left, pick
        # one at random and place it in the column
        if len(opponents)>0:
            toPlace = random.choice(opponents)
            newColumn[placement] = toPlace
            opponents.remove(toPlace)

        #put the temporarily banned canidate back in the opponents list
        if bannedopponent != 999999:
            opponents.append(bannedopponent)
            bannedopponent = 999999

    #place the last opponent (whether it causes noRepeat-violation or not):
    newColumn[len(newColumn)-1] = opponents[0]

    # check whether the last placement created a noRepeat-violation, and if so
    # re-place the prelast opponent by swapping with the preprelast opponent
    if newColumn[len(newColumn)-1] == - newColumn[len(newColumn)-2]:
        tmp = newColumn[len(newColumn)-3]
        newColumn[len(newColumn)-3] = newColumn[len(newColumn)-2]
        newColumn[len(newColumn)-2] = tmp

    return newColumn


def makeColumnAvoidNorepeat2(nTeams):
    # does the same as makeColumnAvoidNorepeat2, except swaps the prelast
    # entry with ANY other entry

    # create the column to be returned at the end of the function
    newColumn = [0] * (nTeams * 2 - 2)

    # make a list of the opponents to be placed
    opponents = []
    for teamNr in range(1, nTeams):
        opponents.append(teamNr)
        opponents.append(-teamNr)
    random.shuffle(opponents)

    # the value '999999' signifies 'no banned opponent'
    bannedopponent = 999999

    # default: place the first opponent from the random list in the first slot
    newColumn[0] = opponents[0]
    opponents.remove(opponents[0])

    # place all the opponents in the column, except the last
    for placement in range(1, len(newColumn)-1):

        # if the >opposite< game of the previously placed game is still
        # available, 'ban' it to prevent it from being selected.
        if -(newColumn[placement-1]) in opponents:
            bannedopponent = -(newColumn[placement-1])
            opponents.remove(bannedopponent)

        # if there are still opponents for placement left, pick
        # one at random and place it in the column
        if len(opponents)>0:
            toPlace = random.choice(opponents)
            newColumn[placement] = toPlace
            opponents.remove(toPlace)

        if bannedopponent != 999999:
            opponents.append(bannedopponent)
            bannedopponent = 999999

    #place the last opponent (whether it causes noRepeat-violation or not):
    newColumn[len(newColumn)-1] = opponents[0]

    #check whether the last placement created a noRepeat-violation,
    # and if so, re-place the pre-last opponent
    if newColumn[len(newColumn)-1] == - newColumn[len(newColumn)-2]:
        tmp = newColumn[len(newColumn)-2]
        swapopponentIndex = random.randint(0,len(newColumn)-4)
        newColumn[len(newColumn) - 2] = newColumn[swapopponentIndex]
        newColumn[swapopponentIndex] = tmp
        #print("Swapped with "+str(swapopponentIndex))
    return newColumn


def makeColumnAvoidNorepeat3(nTeams):
    # does the same as makeColumnAvoidNorepeat3, except swaps the prelast
    # entry with ANY other entry of the SAME sign (a negative number for a negative number)

    # create the column to be returned at the end of the function
    newColumn = [0] * (nTeams * 2 - 2)

    # make a list of the opponents to be placed
    opponents = []
    for teamNr in range(1, nTeams):
        opponents.append(teamNr)
        opponents.append(-teamNr)
    random.shuffle(opponents)

    # the value '999999' signifies 'no banned opponent'
    bannedopponent = 999999

    # default: place the first opponent from the random list in the first slot
    newColumn[0] = opponents[0]
    opponents.remove(opponents[0])

    # place all the opponents in the column, except the last
    for placement in range(1, len(newColumn)-1):

        # if the >opposite< game of the previously placed game is still
        # available, 'ban' it to prevent it from being selected.
        if -(newColumn[placement-1]) in opponents:
            bannedopponent = -(newColumn[placement-1])
            opponents.remove(bannedopponent)

        # if there are still opponents for placement left, pick
        # one at random and place it in the column
        if len(opponents)>0:
            toPlace = random.choice(opponents)
            newColumn[placement] = toPlace
            opponents.remove(toPlace)

        if bannedopponent != 999999:
            opponents.append(bannedopponent)
            bannedopponent = 999999

    #place the last opponent (whether it causes noRepeat-violation or not):
    newColumn[len(newColumn)-1] = opponents[0]

    # check whether the last placement created a noRepeat-violation,
    # and if so, re-place the pre-last opponent
    if newColumn[len(newColumn)-1] == - newColumn[len(newColumn)-2]:
        tmp = newColumn[len(newColumn)-2]
        sameSignOpponentsIndices = []
        for signSeeker in range (0,len(newColumn)-2):
            if tmp < 0 and newColumn[signSeeker] < 0:
                sameSignOpponentsIndices.append(signSeeker)
            if tmp > 0 and newColumn[signSeeker] > 0:
                sameSignOpponentsIndices.append(signSeeker)

        swapopponentIndex = random.choice(sameSignOpponentsIndices)

        #print(newColumn)
        #print(sameSignOpponentsIndices)
        #print("swapping "+str(newColumn[len(newColumn) - 2]) +" at position " +str(len(newColumn) - 2) +
        #" with "+str(newColumn[swapopponentIndex])+" at position "+str(swapopponentIndex))

        newColumn[len(newColumn) - 2] = newColumn[swapopponentIndex]
        newColumn[swapopponentIndex] = tmp
        #print(newColumn)
    return newColumn


def makeStreakPattern(nTeams):
    localMaxStreak = 3
    nMatches = 2*nTeams - 2
    minNumberOfStreaks = 2*(math.ceil(nMatches/(2*localMaxStreak)))
    maxNumberOfStreaks = nMatches

    nStreaks = random.randint(minNumberOfStreaks,maxNumberOfStreaks)
    #print(minNumberOfStreaks)
    #print(nStreaks)

    firstGroup = [1]*math.ceil(nStreaks/2)
    secondGroup = [1]*math.floor(nStreaks/2)

    firstGroupToDo = int(nMatches/2 - len(firstGroup))
    secondGroupToDo = int(nMatches/2 - len(secondGroup))

    # the indices need to be kept not to exceed maxStreak
    indexLoadFirstGroup = []
    for counter in range(0,len(firstGroup)):
        indexLoadFirstGroup.append(counter)

    indexLoadSecondGroup = []
    for counter in range(0, len(secondGroup)):
        indexLoadSecondGroup.append(counter)

    #print(indexLoadFirstGroup)
    #print(indexLoadSecondGroup)

    for counter in range(0,firstGroupToDo):
        place = random.choice(indexLoadFirstGroup)
        firstGroup[place] += 1

        if firstGroup[place] == localMaxStreak:
            indexLoadFirstGroup.remove(place)


    for counter in range(0, secondGroupToDo):
        place = random.choice(indexLoadSecondGroup)
        secondGroup[place] += 1

        if secondGroup[place] == localMaxStreak:
            indexLoadSecondGroup.remove(place)

    #print(firstGroup)
    #print(secondGroup)

    streak = [0]*(len(firstGroup)+len(secondGroup))
    beginAtHomeOrAway = 1
    if random.randint(0,1) == 0:
        beginAtHomeOrAway = -1

    for counter in range(0, len(firstGroup)):
        streak[counter*2] = beginAtHomeOrAway*firstGroup[counter]

    for counter in range(0, len(secondGroup)):
        streak[1+counter*2] = -1*beginAtHomeOrAway*secondGroup[counter]

    #print(streak)

    streakInLetters = []
    for counter in range(0, len(streak)):
        if streak[counter] == 1:
            streakInLetters.append('H')
        if streak[counter] == 2:
            streakInLetters.extend(['H','H'])
        if streak[counter] == 3:
            streakInLetters.extend(['H','H','H'])
        if streak[counter] == -1:
            streakInLetters.append('A')
        if streak[counter] == -2:
            streakInLetters.extend(['A','A'])
        if streak[counter] == -3:
            streakInLetters.extend(['A','A','A'])

    return streakInLetters


def makeColumnfromStreakPattern(nTeams, streakPattern):

    newColumn = []

    opponentsHome = []
    opponentsAway = []
    for teamNr in range(1, nTeams):
        opponentsHome.append(teamNr)
        opponentsAway.append(-teamNr)
    random.shuffle(opponentsHome)
    random.shuffle(opponentsAway)
    #print(opponentsHome)
    #print(opponentsAway)

    for counter in range(0, len(streakPattern)):
        placementCandidate = 0

        # placement routine for a home-match
        if streakPattern[counter] == 'H':
            bannedCandidate = 0
            if counter > 0 and streakPattern[counter - 1] == 'A' and -newColumn[counter - 1] in opponentsHome:
                bannedCandidate = -newColumn[counter - 1]
                opponentsHome.remove(bannedCandidate)

            if len(opponentsHome) != 0:
                placementCandidate = random.choice(opponentsHome)
            else:
                print("WARNING line 354")
                placementCandidate = bannedCandidate
                opponentsHome.append(bannedCandidate)


            #print("opponentshome:"+str(opponentsHome)+","+str(placementCandidate))
            newColumn.append(placementCandidate)
            opponentsHome.remove(placementCandidate)

            if bannedCandidate != 0:
                opponentsHome.append(bannedCandidate)

        # placement routine for a away-match
        if streakPattern[counter] == 'A':
            bannedCandidate = 0
            if counter > 0 and streakPattern[counter-1] == 'H' and -newColumn[counter-1] in opponentsAway:
                bannedCandidate = -newColumn[counter-1]
                opponentsAway.remove(bannedCandidate)

            if len(opponentsAway) != 0:
                placementCandidate = random.choice(opponentsAway)
            else:
                print("WARNING line 370")
                placementCandidate = bannedCandidate
                opponentsHome.append(bannedCandidate)

            newColumn.append(placementCandidate)

            if placementCandidate in opponentsAway:
                opponentsAway.remove(placementCandidate)
            else:
                print("WARNING line 378.")

            if bannedCandidate != 0:
                opponentsAway.append(bannedCandidate)

    return newColumn


def makeColumnfromStreakPattern2(nTeams, streakPattern):

    newColumn = [0]*(2*nTeams-2)

    opponentsHome = []
    opponentsAway = []
    awayIndices = []
    for teamNr in range(1, nTeams):
        opponentsHome.append(teamNr)
        opponentsAway.append(-teamNr)
    random.shuffle(opponentsHome)
    random.shuffle(opponentsAway)

    #place home games
    for counter in range(0, len(streakPattern)):
        if streakPattern[counter] == 'H':
            newColumn[counter] = opponentsHome[0]
            opponentsHome.remove(opponentsHome[0])
        else:
            awayIndices.append(counter)

    # place away games
    for counter in range(0, len(streakPattern)):
        if streakPattern[counter] == 'A':
            bannedCandidateBefore = 0
            bannedCandidateAfter = 0

            if counter > 0 and streakPattern[counter-1] == 'H':
                bannedCandidateBefore = -newColumn[counter - 1]
            if counter + 1 < len(streakPattern) and streakPattern[counter + 1] == 'H':
                bannedCandidateAfter = -newColumn[counter + 1]

            if bannedCandidateBefore != 0 and bannedCandidateBefore in opponentsAway:
                opponentsAway.remove(bannedCandidateBefore)
            else:
                bannedCandidateBefore = 0

            if bannedCandidateAfter != 0 and bannedCandidateAfter in opponentsAway:
                opponentsAway.remove(bannedCandidateAfter)
            else:
                bannedCandidateAfter = 0

            #print("Banned: "+str(bannedCandidateBefore)+","+str(bannedCandidateAfter))

            if len(opponentsAway) > 0:
                newColumn[counter] = random.choice(opponentsAway)
                opponentsAway.remove(newColumn[counter])

            if bannedCandidateBefore !=0:
                opponentsAway.append(bannedCandidateBefore)
                bannedCandidateBefore = 0
            if bannedCandidateAfter !=0:
                opponentsAway.append(bannedCandidateAfter)
                bannedCandidateAfter = 0

            #print("placed " + str(newColumn[counter]))
            #print("todo " + str(opponentsAway))

    #repair routine
    if len(opponentsAway)>0:
        badTeam = opponentsAway[0]
        #print("repair "+str(newColumn)+", bad team is "+str(badTeam))

        swapCandidates = []
        for teamNr in range(1, nTeams):
            swapCandidates.append(-teamNr)


        for counter in range(0,len(newColumn)):
            if newColumn[counter] == 0:
                if counter>0 and streakPattern[counter-1] == 'H':
                    swapCandidates.remove(-newColumn[counter-1])
                if counter+1 < len(newColumn) and streakPattern[counter + 1] == 'H':
                    swapCandidates.remove(-newColumn[counter + 1])

        #print("Swapcandidates: " + str(swapCandidates))

        for counter in range(0,len(newColumn)):
            if newColumn[counter] in swapCandidates and counter > 0 and newColumn[counter-1] == -badTeam:
                swapCandidates.remove(newColumn[counter])
            if newColumn[counter] in swapCandidates and counter + 1 < len(newColumn) and newColumn[counter + 1] == -badTeam:
                swapCandidates.remove(newColumn[counter])

        #print("Swapcandidates: "+str(swapCandidates))

        if len(swapCandidates)>0:
            finalSwapCandidate = random.choice(swapCandidates)
            for counter in range(0, len(newColumn)):
                if newColumn[counter] == finalSwapCandidate:
                    newColumn[counter] = badTeam
                if newColumn[counter] == 0:
                    newColumn[counter] = finalSwapCandidate
        else:
            print("No swapcandidates!")
        #print(newColumn)

    return newColumn


validColumns = []
validColumnsFrequency = []

validColumnsHistogram = []
invalidColumnsHistogram = []

streakConfigHistogram = []

nTeams = 8
nTrials = 100000
start = time.time()
for trial in range(0, nTrials):
    if trial%10000 == 0:
        now = time.time()
        print("Trial: "+str(trial)+", Time:"+str(math.ceil(now-start))+
              ", Histogram length: "+str(len(validColumnsHistogram)))
    streakPattern = makeStreakPattern(nTeams)
    #print(streakPattern)
    column = makeColumnfromStreakPattern2(nTeams,streakPattern)
    #print(column)
    msv = checkMaxStreakViolations(column,3)
    nrv = checkNoRepeatViolations(column)
    if msv[0] > 0 or nrv[0] > 0:
        print("MaxStreakViolations: "+str(msv[0]))
        print("=============================================================NoRepeatViolations: " + str(nrv[0]))
        print(streakPattern)
        print(column)

    found = False
    for pointer in range(len(validColumnsHistogram)):
        if column == validColumnsHistogram[pointer][1]:
            found = True
            validColumnsHistogram[pointer][0] = int(validColumnsHistogram[pointer][0]) + 1

    if not found:
        validColumnsHistogram.append([int(1), column])

validColumnsHistogram.sort(reverse=True)

fileName = "histogram_"+str(nTeams)+"_"+str(nTrials)+"_trials"
with open(fileName, 'w+') as f:
    # write elements of list
    for items in validColumnsHistogram:
        f.write('%s\n' % items)

    print("File written successfully")

# close the file
f.close()

#print("Histogram:")
#for looper in range(0, len(validColumnsHistogram)):
#    print(str(validColumnsHistogram[looper][0]) + "," + str(validColumnsHistogram[looper][1]))

