import cv2

# Motivators below
Excitement = 0  # Opposite of boredom, scale of -10 to 10
Hunger = 0   # doesn't require negative, simple indication of battery power, linked to behaviors here
Hype = 0  # opposite of fatigue. Rapid, sustained activity leads to Hype going down into fatigue, so robot gets "tired"
Worried = 0     # maybe different name needed. Motivates the robot to as the user what's wrong, or act compassionate.
Anger = 0   # Increase when user ignores robot, if it loses games, or fails to perform tasks. Drops quickly.
Happiness = 0   # Opposite of sadness. Should tend to decay towards a small positive number (3) to promote happiness.
userFace = 0    # The user's detected emotion, based on smile or frown. 10 is super happy, -10 is super sad.

# When picking behaviors, modify relevant values by a small random number so that the responses are not always
# predictable, mimicking the unpredictable nature of real animals. General behavior should be positive and friendly
# rather than negative or aggressive. Hence, resting points for motivators should be slightly positive.

# Tree structure for behavior picking. At each node, use motivators to pick which way to go. Early nodes are generalist,
# later nodes are more specific, maybe picking between very similar behaviors.

