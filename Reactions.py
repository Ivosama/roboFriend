class Reactions:
    import cv2
    import numpy as np
    import collections
    memlen = 10 #robot's memory length for mouth and brow lists, first in first out
    ma = collections.deque(maxlen=memlen)   #Mouth memory
    ba = collections.deque(maxlen=memlen)   #brow memory
    MOUTH = 'smile'
    BROW = 'neutral'
    ma.append(MOUTH)    #Put these where the mouth / brow are being detected
    ba.append(BROW)

    def getReaction(self):
        m = Reactions.getMouth
        b = Reactions.getBrow
        if m == 'smile':
            if b == 'smile':
                return      #Replace each of these returns with separate functions, or just more if with robot feelings
            elif b == 'neutral':
                return
            elif b == 'frown':
                return
        elif m == 'neutral':
            if b == 'smile':
                return
            elif b == 'neutral':
                return
            elif b == 'frown':
                return
        elif m == 'frown':
            if b == 'smile':
                return
            elif b == 'neutral':
                return
            elif b == 'frown':
                return


    def getMouth(self):
        if Reactions.ma.count('smile') >= Reactions.ma.count('neutral') & Reactions.ma.count('smile') >= Reactions.ma.count('frown'):
            return 'smile'
        if Reactions.ma.count('neutral') >= Reactions.ma.count('frown') & Reactions.ma.count('neutral') >= Reactions.ma.count('smile'):
            return 'neutral'
        if Reactions.ma.count('frown') >= Reactions.ma.count('neutral') & Reactions.ma.count('frown') >= Reactions.ma.count('smile'):
            return 'frown'

    def getBrow(self):  ##OBVIOUSLY NEEDS TO GET CHANGED TO WHATEVER WORDS WE USE FOR BROWS
        if Reactions.ma.count('smile') >= Reactions.ma.count('neutral') & Reactions.ma.count('smile') >= Reactions.ma.count('frown'):
            return 'smile'
        if Reactions.ma.count('neutral') >= Reactions.ma.count('frown') & Reactions.ma.count('neutral') >= Reactions.ma.count('smile'):
            return 'neutral'
        if Reactions.ma.count('frown') >= Reactions.ma.count('neutral') & Reactions.ma.count('frown') >= Reactions.ma.count('smile'):
            return 'frown'

#Mouth states: laugh, smile, neutral, frown, speaking?
#Brow states:
