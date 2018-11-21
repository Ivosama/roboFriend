class Reactions:
    import cv2
    import numpy as np
    import collections
    import random
    memlen = 10 # robot's memory length for mouth and brow lists, first in first out
    ma = collections.deque(maxlen=memlen)   # Mouth memory
    ba = collections.deque(maxlen=memlen)   # brow memory
    ml = ['smile', 'neutral', 'frown']  # list of mouths
    bl = ['b1', 'b2', 'b3'] # list of brows


    def getReaction(self):
        m = Reactions.getMouth
        b = Reactions.getBrow
        if m == 'smile':
            if b == 'b1':
                print('smile, b1')
                return      # Replace each of these returns with separate functions, or more ifs with robot feelings
            elif b == 'b2':
                print('smile, b2')
                return
            elif b == 'b3':
                print('smile, b3')
                return
        elif m == 'neutral':
            if b == 'b1':
                return      # Replace each of these returns with separate functions, or more ifs with robot feelings
            elif b == 'b2':
                return
            elif b == 'b3':
                return
        elif m == 'frown':
            if b == 'b1':
                return      # Replace each of these returns with separate functions, or more ifs with robot feelings
            elif b == 'b2':
                return
            elif b == 'b3':
                return

    def getMouth(self):     # Gets most common mouth entry from memory
        if Reactions.ma.count('smile') >= Reactions.ma.count('neutral') & Reactions.ma.count('smile') >= Reactions.ma.count('frown'):  # Priority for positive reactions over negative
            return 'smile'
        elif Reactions.ma.count('neutral') >= Reactions.ma.count('frown') & Reactions.ma.count('neutral') >= Reactions.ma.count('smile'):
            return 'neutral'
        elif Reactions.ma.count('frown') >= Reactions.ma.count('neutral') & Reactions.ma.count('frown') >= Reactions.ma.count('smile'):
            return 'frown'

    def getBrow(self):  # 3 states of brow, /  \   -  -   \  /
        if Reactions.ma.count('b1') >= Reactions.ma.count('b2') & Reactions.ma.count('b1') >= Reactions.ma.count('b3'):
            return 'b1'
        elif Reactions.ma.count('b2') >= Reactions.ma.count('b3') & Reactions.ma.count('b2') >= Reactions.ma.count('b1'):
            return 'b2'
        elif Reactions.ma.count('b3') >= Reactions.ma.count('b2') & Reactions.ma.count('b3') >= Reactions.ma.count('b1'):
            return 'b3'

    def updateFace(self, m, b):  # use this to update expressions, m = mouth b = brow
        Reactions.ma.append(m)
        Reactions.ba.append(b)

    def debugRandFace(self):    # adds a random mouth and brow to memory
        import random
        m = random.choice(Reactions.ml)
        b = random.choice(Reactions.bl)
        Reactions.ma.append(m)
        Reactions.ba.append(b)