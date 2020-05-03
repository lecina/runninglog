from runninglog.constants import blockNames

"""
    RunTypes can be divided in 5 running types + cross training 
    Basic running types are: easy, marathon pace, threshold, interval and repetition (hard)

    Activities may have an emphasis in one of the previous or may be a race (C)
"""

class BASIC_RUN_TYPES_ENUM:
    E, M, T, I, R, X, XB = range(7)

#Basic run types + cross-training (X as a generic type, XB as biking)
BASIC_RUN_TYPES_DICTIONARY = {
    BASIC_RUN_TYPES_ENUM.E : blockNames.RunTypes.E,
    BASIC_RUN_TYPES_ENUM.M : blockNames.RunTypes.M,
    BASIC_RUN_TYPES_ENUM.T : blockNames.RunTypes.T,
    BASIC_RUN_TYPES_ENUM.I : blockNames.RunTypes.I,
    BASIC_RUN_TYPES_ENUM.R : blockNames.RunTypes.R,
    BASIC_RUN_TYPES_ENUM.X : blockNames.RunTypes.X,
    BASIC_RUN_TYPES_ENUM.XB: blockNames.RunTypes.XB
}

class RUN_TYPES_ENUM:
    E, LE, M, T, I, H, R, C, X, XB = range(10)

#ACTIVITY_TYPES_DICTIONARY
RUN_TYPES_DICTIONARY = {
    RUN_TYPES_ENUM.E : blockNames.RunTypes.E, 
    RUN_TYPES_ENUM.M : blockNames.RunTypes.M, 
    RUN_TYPES_ENUM.T : blockNames.RunTypes.T, 
    RUN_TYPES_ENUM.I : blockNames.RunTypes.I, 
    RUN_TYPES_ENUM.R : blockNames.RunTypes.R, 
    RUN_TYPES_ENUM.C : blockNames.RunTypes.C, 
    RUN_TYPES_ENUM.X : blockNames.RunTypes.X,
    RUN_TYPES_ENUM.XB :blockNames.RunTypes.XB
}



BASIC_RUN_TYPES = [ blockNames.RunTypes.E,
                    blockNames.RunTypes.M,
                    blockNames.RunTypes.T,
                    blockNames.RunTypes.I,
                    blockNames.RunTypes.R ]


ALL_ACTIVITIES = [  blockNames.RunTypes.E,
                    blockNames.RunTypes.M,
                    blockNames.RunTypes.T,
                    blockNames.RunTypes.I,
                    blockNames.RunTypes.R,
                    blockNames.RunTypes.C,
                    blockNames.RunTypes.X,
                    blockNames.RunTypes.XB ]


RUNNING_ACTIVITIES = [  blockNames.RunTypes.E,
                        blockNames.RunTypes.M,
                        blockNames.RunTypes.T,
                        blockNames.RunTypes.I,
                        blockNames.RunTypes.R,
                        blockNames.RunTypes.C 
                    ]


NON_RUNNING_ACTIVITIES = [  blockNames.RunTypes.X, 
                            blockNames.RunTypes.XB]
