class Reactions:
    import cv2
    import numpy as np
    import collections
    memlen = 10 #robot's memory length for mouth and brow lists, first in first out
    ma = collections.deque(maxlen=memlen)   #Mouth memory
    ba = collections.deque(maxlen=memlen)   #brow memory
    MOUTH = 'smile'
    BROW = 'neutral'
    def getReaction(self):
        Reactions.ma.append(Reactions.MOUTH)
        Reactions.ba.append(Reactions.BROW)
        # get user brows
        if Reactions.MOUTH == 'smile':
            if Reactions.BROW == 'neutral':
                #neutral-smile reactions below based on robot state
        elif Reactions.MOUTH == 'neutral':
            if Reactions.BROW == 'neutral':
                return

    def getFace(self):



#Mouth states: laugh, smile, neutral, frown, speaking?
#Brow states:
