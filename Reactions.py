def getReaction():
    m = getMouth
    b = getBrow
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
            print('neutral, b1')
            return      # Replace each of these returns with separate functions, or more ifs with robot feelings
        elif b == 'b2':
            print('neutral, b2')
            return
        elif b == 'b3':
            print('neutral, b3')
            return
    elif m == 'frown':
        if b == 'b1':
            print('frown, b1')
            return      # Replace each of these returns with separate functions, or more ifs with robot feelings
        elif b == 'b2':
            print('frown, b2')
            return
        elif b == 'b3':
            print('frown, b3')
            return


def getMouth():     # Gets most common mouth entry from memory
    if Reactions.ma.count('smile') >= Reactions.ma.count('neutral') & Reactions.ma.count('smile') >= Reactions.ma.count('frown'):  # Priority for positive reactions over negative
        return 'smile'
    elif Reactions.ma.count('neutral') >= Reactions.ma.count('frown') & Reactions.ma.count('neutral') >= Reactions.ma.count('smile'):
        return 'neutral'
    elif Reactions.ma.count('frown') >= Reactions.ma.count('neutral') & Reactions.ma.count('frown') >= Reactions.ma.count('smile'):
        return 'frown'


def getBrow():  # 3 states of brow, /  \   -  -   \  /
    if Reactions.ma.count('b1') >= Reactions.ma.count('b2') & Reactions.ma.count('b1') >= Reactions.ma.count('b3'):
        return 'b1'
    elif Reactions.ma.count('b2') >= Reactions.ma.count('b3') & Reactions.ma.count('b2') >= Reactions.ma.count('b1'):
        return 'b2'
    elif Reactions.ma.count('b3') >= Reactions.ma.count('b2') & Reactions.ma.count('b3') >= Reactions.ma.count('b1'):
        return 'b3'


def updateFace(m, b):  # use this to update expressions, m = mouth b = brow
    Reactions.ma.append(m)
    Reactions.ba.append(b)


def updateMouth(m):  # update mouth only
    Reactions.ma.append(m)


def updateBrow(b):  # update brow only
    Reactions.ba.append(b)


def debugRandFace():    # adds a random mouth and brow to memory
    import random
    Reactions.ma.append(random.choice(Reactions.ml))
    Reactions.ba.append(random.choice(Reactions.bl))


class Reactions:
    import collections
    memlen = 10 # robot's memory length for mouth and brow lists, first in first out unless specified otherwise (deque)
    ma = collections.deque(maxlen=memlen)   # Mouth memory
    ba = collections.deque(maxlen=memlen)   # brow memory
    ml = ['smile', 'neutral', 'frown']  # list of mouths
    bl = ['b1', 'b2', 'b3']  # list of brows, can add more, but then have to add below too
    # If we have time, maybe use face memory to create reactions based on change
    # eg, if ma is [frown, frown, neutral, smile, frown, neutral, smile, smile, smile, neutral]
    # read it as a shift from frown to smile, and maybe react with a "yay i cheered you up"

