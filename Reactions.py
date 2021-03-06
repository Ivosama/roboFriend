import PyGame

class Reactions:
    import collections
    memlen = 3  # robot's memory length for mouth and brow lists, first in first out unless specified otherwise (deque)
    ma = collections.deque(maxlen=memlen)  # Mouth memory
    ba = collections.deque(maxlen=memlen)  # brow memory
    ml = ['smile', 'neutral', 'frown']  # list of mouths
    bl = ['b1', 'b2', 'b3']  # list of brows, can add more, but then have to add below too
    acting = False  # Whether or not the robot is performing an action
    # If we have time, maybe use face memory to create reactions based on change
    # eg, if ma is [frown, frown, neutral, smile, frown, neutral, smile, smile, smile, neutral]
    # read it as a shift from frown to smile, and maybe react with a "yay i cheered you up"
    # b1 = -  -
    # b2 = /  \
    # b3 = \  /
    def getReaction(self):
        m = self.getMouth()
        print("getReaction return: ")
        if m == 'smile':
            print('HappyFace')
            PyGame.happyFace()
            return  # Replace each of these returns with separate functions, or more ifs with robot feelings
        else:
            b = self.getBrow()
            if m == 'neutral':
                if b == 'b1':
                    print('NeutralFace')
                    PyGame.neutralFace()
                    return  # Replace each of these returns with separate functions, or more ifs with robot feelings
                elif b == 'b2':
                    print('neutralFace')
                    PyGame.neutralFace()
                    return
                elif b == 'b3':
                    print('AngryFace')
                    PyGame.angryFace()
                    return
            elif m == 'frown':
                if b == 'b1':
                    print('SadFace')
                    PyGame.sadFace()
                    return  # Replace each of these returns with separate functions, or more ifs with robot feelings
                elif b == 'b2':
                    print('SadFace')
                    PyGame.sadFace()
                    return
                elif b == 'b3':
                    print('AngryFace')
                    PyGame.angryFace()
                    return
            else:
                print('error finding reaction')

    def getMouth(self):  # Gets most common mouth entry from memory, can be changed later to list from most common to least.
        if self.ma.count('smile') >= self.ma.count('neutral') and self.ma.count('smile') >= self.ma.count('frown'):  # Priority for positive reactions over negative
            #print('smile')
            return 'smile'
        elif self.ma.count('neutral') >= self.ma.count('frown') and self.ma.count('neutral') >= self.ma.count('smile'):
            #print('neutral')
            return 'neutral'
        elif self.ma.count('frown') >= self.ma.count('neutral') and self.ma.count('frown') >= self.ma.count('smile'):
            #print('frown')
            return 'frown'
        else:
            #print('neutral')
            return 'neutral'

    def getBrow(self):  # 3 states of brow, /  \   -  -   \  /
        if self.ba.count('b1') >= self.ba.count('b2') and self.ba.count('b1') >= self.ba.count('b3'):
            #print('b1')
            return 'b1'
        elif self.ba.count('b2') >= self.ba.count('b3') and self.ba.count('b2') >= self.ba.count('b1'):
            #print('b2')
            return 'b2'
        elif self.ba.count('b3') >= self.ba.count('b2') and self.ba.count('b3') >= self.ba.count('b1'):
            #print('b3')
            return 'b3'
        else:
            #print('b2')
            return 'b2'

    def updateFace(self, m, b):  # use this to update expressions, m = mouth b = brow
        self.updateMouth(m)
        self.updateBrow(b)

    def updateMouthString(self, m):  # update mouth using string
        if m == 'smile' or 'neutral' or 'frown':
            self.ma.append(m)

    def updateMouth(self, mi):  # update mouth using integer
        if mi == 1:
            self.ma.append('smile')
        if mi == 0:
            self.ma.append('neutral')
        if mi == 2:
            self.ma.append('frown')
        print("Mouth append: " + str(mi))

    def updateBrowString(self, b):  # update brow using string
        if b == 'b1' or 'b2' or 'b3':
            self.ba.append(b)

    def updateBrow(self, bi):  # update mouth using integer
        if bi == 0:
            self.ba.append('b1')  # This is neutral brow
        if bi == 1:
            self.ba.append('b2')  # This is happy brow
        if bi == 2:
            self.ba.append('b3')  # This is angry brows
        print("Brow append: " + str(bi))

    def debugRandFace(self):  # adds a random mouth and brow to memory
        import random
        self.ma.append(random.choice(self.ml))
        self.ba.append(random.choice(self.bl))

    def initMem(self):  # Fills memory with some face for initialization
        for x in range(self.memlen):
            self.updateMouth(0)
            self.updateBrow(0)

    def cheerUp(self):  # Triggers to try and cheer the user up with a little dance when they're sad
        print('wiggle')
        print('silly face')


"""
print('avg mouth:')
r.getMouth()
print('avg brow:')
r.getBrow()
print('all vals')
for i in range(r.memlen):
    print(r.ma[i])
    print(r.ba[i])
"""


