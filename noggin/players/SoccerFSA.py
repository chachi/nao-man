# Soccer FSA that implements an FSA but holds all the important
# soccer-playing functionality
#
#
from man.motion import HeadMoves
import man.motion as motion
from ..util import FSA
from ..navigator import NavHelper as helper
from . import CoreSoccerStates

class SoccerFSA(FSA.FSA):
    def __init__(self,brain):
        FSA.FSA.__init__(self, brain)
        #self.setTimeFunction(self.brain.nao.getSimulatedTime)
        self.addStates(CoreSoccerStates)
        self.brain = brain
        self.motion = brain.motion

        #set default behavior for soccer players - override it if you want
        self.setPrintStateChanges(True)
        # set printing to be done with colors
        self.stateChangeColor = 'red'
        self.setPrintFunction(self.brain.out.printf)

    def run(self):
        FSA.FSA.run(self)

    def executeMove(self,sweetMove):
        """
        Method to enqueue a SweetMove
        Can either take in a head move or a body command
        (see SweetMove files for descriptions of command tuples)
        """
        self.brain.nav.performSweetMove(sweetMove)
        ## for position in sweetMove:
        ##     if len(position) == 7:
        ##         move = motion.BodyJointCommand(position[4], #time
        ##                                        position[0], #larm
        ##                                        position[1], #lleg
        ##                                        position[2], #rleg
        ##                                        position[3], #rarm
        ##                                        position[6], # Chain Stiffnesses
        ##                                        position[5], #interpolation type
        ##                                        )

        ##     elif len(position) == 5:
        ##         move = motion.BodyJointCommand(position[2], # time
        ##                                        position[0], # chainID
        ##                                        position[1], # chain angles
        ##                                        position[4], # chain stiffnesses
        ##                                        position[3], # interpolation type
        ##                                        )

        ##     else:
        ##         self.printf("What kind of sweet ass-Move is this?")

        ##     self.brain.motion.enqueue(move)

    def setWalk(self,x,y,theta):
        """
        Wrapper method to easily change the walk vector of the robot
        """
        if x == 0 and y == 0 and theta == 0:
            self.stopWalking()
        else:
            self.brain.nav.walk(x,y,theta)
            # else:
            #     self.printf("WARNING NEW WALK of %g,%g,%g" % (x,y,theta) +
            #                 " is ignored")

    def getWalk(self):
        """
        returns a tuple of current walk parameters
        """
        nav = self.brain.nav
        return (nav.walkX, nav.walkY, nav.walkTheta)

    def setSteps(self, x, y, theta, numSteps=1):
        """
        Have the robot walk a specified number of steps
        """
        if self.brain.motion.isWalkActive():
            return False
        else:
            self.brain.nav.takeSteps(x, y, theta, numSteps)
            return True

    def standup(self):
        self.brain.nav.stop()

    def walkPose(self):
        """
        we return to std walk pose when we stop walking
        """
        self.brain.nav.stop()

    def stopWalking(self):
        """
        Wrapper method to navigator to easily stop the robot from walking
        """
        nav = self.brain.nav
        if not nav.isStopped():
            self.brain.nav.stop()

    def atDestinationGoalie(self):
        nav = self.brain.nav
        return helper.atDestinationGoalie(self.brain.my, nav.dest)

    def atDestinationCloser(self):
        nav = self.brain.nav
        return helper.atDestinationCloser(self.brain.my, nav.dest)

    def atHeading(self):
        nav = self.brain.nav
        return helper.atHeading(self.brain.my, nav.dest.h)

##### Direct Motion Calls
    def gainsOff(self):
        """
        Turn off the gains
        """
        freeze = motion.FreezeCommand()
        self.brain.motion.sendFreezeCommand(freeze)

    def gainsOn(self):
        """
        Turn on the gains
        """
        unFreeze = motion.UnfreezeCommand(0.85)
        self.brain.motion.sendFreezeCommand(unFreeze)

##### HEAD-TRACKING Methods
    def penalizeHeads(self):
        """
        Put head into penalized position, stop tracker
        """
        self.brain.tracker.performHeadMove(HeadMoves.PENALIZED_HEADS)

    def zeroHeads(self):
        """
        Put heads into neutral position
        """
        self.brain.tracker.performHeadMove(HeadMoves.ZERO_HEADS)

    def kickScan(self):
        self.brain.tracker.performHeadMove(HeadMoves.KICK_SCAN)

##### Gait switching methods
    def setRobotGait(self):
        """
        Sets the robot's regular gait
        """
        newGait = self.brain.CoA.gait
        self.setGait(newGait)

    def setRobotDribbleGait(self):
        """
        Sets the robot's dribbling gait
        """
        newGait = self.brain.CoA.dribble_gait
        self.setGait(newGait)

    def setRobotSlowGait(self):
        """
        Sets robot's slow moving gait.
        """
        newGait = self.brain.CoA.slow_gait
        self.setGait(newGait)

    def setGait(self, newGait):
        """
        Sets the robots gait to the one given to it
        """
        CoA = self.brain.CoA
        if newGait is not None and \
                CoA.current_gait is not newGait:
            CoA.current_gait = newGait
            self.brain.motion.setGait(newGait)
