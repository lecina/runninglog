from constants import blockNames

class BASIC_RUN_TYPES:
    E, M, T, I, R, WU, CD, X, XB = range(9)

BASIC_RUN_TYPES_DICTIONARY = {
    BASIC_RUN_TYPES.E : blockNames.RunTypes.E, 
    BASIC_RUN_TYPES.M : blockNames.RunTypes.M, 
    BASIC_RUN_TYPES.T : blockNames.RunTypes.T, 
    BASIC_RUN_TYPES.I : blockNames.RunTypes.I, 
    BASIC_RUN_TYPES.R : blockNames.RunTypes.R,
    BASIC_RUN_TYPES.WU : blockNames.RunTypes.WU,
    BASIC_RUN_TYPES.CD : blockNames.RunTypes.CD,
    BASIC_RUN_TYPES.X : blockNames.RunTypes.X,
    BASIC_RUN_TYPES.XB : blockNames.RunTypes.XB
}

class RUN_TYPES:
    E, LE, M, T, I, H, R, C, X, XB = range(10)

RUN_TYPES_DICTIONARY = {
    RUN_TYPES.E : blockNames.RunTypes.E, 
    RUN_TYPES.M : blockNames.RunTypes.M, 
    RUN_TYPES.T : blockNames.RunTypes.T, 
    RUN_TYPES.I : blockNames.RunTypes.I, 
    RUN_TYPES.R : blockNames.RunTypes.R, 
    RUN_TYPES.C : blockNames.RunTypes.C, 
    RUN_TYPES.X : blockNames.RunTypes.X,
    RUN_TYPES.XB : blockNames.RunTypes.XB
}

