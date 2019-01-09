class FileParams:
    type = "type"
    date = "date"
    time = "time"
    distance = "distance"
    climb = "climb"
    structure = "structure"
    pace = "pace"
    where = "where"
    notes = "notes"
    list = "list"

class Colnames:
    type = "type"
    date = "date"
    time = "time"
    distance = "distance"
    avg_pace = "avg_pace"
    climb = "climb"
    where = "where"
    notes = "notes"
    distE = "distE"
    distM = "distM"
    distT = "distT"
    distI = "distI"
    distR = "distR"
    distX = "distX"
    paceE = "paceE"
    paceM = "paceM"
    paceT = "paceT"
    paceI = "paceI"
    paceR = "paceR"
    paceX = "paceX"

class RunTypes:
    type = "type"
    E = "E"
    M = "M"
    T = "T" 
    I = "I"
    H = "H"
    R = "R"
    C = "C"
    X = "X" 
    WU = "WU"
    CD = "CD"

RUN_TYPES_LONG_NAME_DICTIONARY = {
    RunTypes.E : "Easy pace",
    RunTypes.M : "Marathon pace",
    RunTypes.T : "Threshold",
    RunTypes.I : "Intervals",
    RunTypes.R : "Repetitions",
    RunTypes.C : "Race",
    RunTypes.X : "Cross-training(Mountaineering)"
}
