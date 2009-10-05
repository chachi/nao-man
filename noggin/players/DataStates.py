import man.motion.SweetMoves as SweetMoves

NUM_FRAMES_TO_SAVE = 150

def gameReady(player):
    player.brain.resetLocalization()
    return player.goNow('saveFrames')

def gameSet(player):
    player.brain.resetLocalization()
    return player.goNow('saveFrames')

def gamePlaying(player):
    player.brain.resetLocalization()
    return player.goNow('saveFrames')

def standup(player):
    if player.firstFrame():
        player.brain.tracker.stopHeadMoves()
        player.standup()
        player.setSpeed(0,0,0)

    elif not player.brain.isBodyActive():
        return player.goLater('saveFrames')

    return player.stay()

def saveFrames(player):
    player.brain.sensors.saveFrame()

    if player.firstFrame():
        player.brain.tracker.photoPan()

    if player.counter > NUM_FRAMES_TO_SAVE:
        return player.goNow('computeSD')

    return player.stay()

def computeSD(player):


    return player.stay()

def doneState(player):
    if player.firstFrame():
        player.executeMove(SweetMoves.SIT_POS)
        player.brain.tracker.stopHeadMoves()
        player.brain.sensors.resetSaveFrame()

#     if player.stateTime > 8.0:
#         shutoff = motion.StiffnessCommand(0.0)
#         player.brain.motion.sendStiffness(shutoff)

    return player.stay()

#gameInitial = gameReady
