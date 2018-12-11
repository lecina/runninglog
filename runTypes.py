import blockNames

class BASIC_RUN_TYPES:
    E, M, T, I, R, WU, CD = range(7) #WU and CD are equivalent to E

BASIC_RUN_TYPES_DICTIONARY = {
    BASIC_RUN_TYPES.E : blockNames.RunTypes.E, 
    BASIC_RUN_TYPES.M : blockNames.RunTypes.M, 
    BASIC_RUN_TYPES.T : blockNames.RunTypes.T, 
    BASIC_RUN_TYPES.I : blockNames.RunTypes.I, 
    BASIC_RUN_TYPES.R : blockNames.RunTypes.R, 
    BASIC_RUN_TYPES.WU : blockNames.RunTypes.WU,
    BASIC_RUN_TYPES.CD : blockNames.RunTypes.CD 
}

class RUN_TYPES:
    E, LE, M, T, I, H, R, C, X = range(9)

RUN_TYPES_DICTIONARY = {
    RUN_TYPES.E : blockNames.RunTypes.E, 
    RUN_TYPES.LE : blockNames.RunTypes.LE, 
    RUN_TYPES.M : blockNames.RunTypes.M, 
    RUN_TYPES.T : blockNames.RunTypes.T, 
    RUN_TYPES.I : blockNames.RunTypes.I, 
    RUN_TYPES.H : blockNames.RunTypes.H, 
    RUN_TYPES.R : blockNames.RunTypes.R, 
    RUN_TYPES.C : blockNames.RunTypes.C, 
    RUN_TYPES.X : blockNames.RunTypes.X 
}
