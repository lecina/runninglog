class ConfigParams:
    output_dir = "output_dir"
    raw_output_dir = "raw_output_dir"
    processed_output_dir = "processed_output_dir"

    input_dir = "input_dir"

    df_name = "df_name"
    df_struct_name = "df_struct_name"

class FileParams:
    type = "type"
    date = "date"
    time = "time"
    distance = "distance"
    climb = "climb"
    structure = "structure"
    pace = "pace"
    vspeed = "vspeed"
    trail = "trail"
    feeling = "feeling"
    where = "where"
    route = "route"
    notes = "notes"
    bpm = "bpm"
    rep = "rep"
    rep_alt = "repetition"
    list = "list"

class Colnames:
    type = "type"
    date = "date"
    time = "time"
    distance = "distance"
    avg_pace = "avg_pace"
    climb = "climb"
    vspeed = "vspeed"
    trail = "trail"
    feeling = "feeling"
    where = "where"
    route = "route"
    notes = "notes"
    distE = "distE"
    distM = "distM"
    distT = "distT"
    distI = "distI"
    distR = "distR"
    distX = "distX"
    distXB = "distXB"
    timeE = "timeE"
    timeM = "timeM"
    timeT = "timeT"
    timeI = "timeI"
    timeR = "timeR"
    timeX = "timeX"
    timeXB = "timeXB"
    paceE = "paceE"
    paceM = "paceM"
    paceT = "paceT"
    paceI = "paceI"
    paceR = "paceR"
    paceX = "paceX"
    paceXB = "paceXB"
    bpm = "bpm"
    repetition = "#"

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
    XB = "XB" 

RUN_TYPES_LONG_NAME_DICTIONARY = {
    RunTypes.E : "Easy pace",
    RunTypes.M : "Marathon pace",
    RunTypes.T : "Threshold",
    RunTypes.I : "Intervals",
    RunTypes.R : "Reps",
    RunTypes.C : "Race",
    RunTypes.X : "XT(Mountaineering)",
    RunTypes.XB : "XT(Bike)"
}
