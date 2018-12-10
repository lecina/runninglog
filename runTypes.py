import blockNames

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
