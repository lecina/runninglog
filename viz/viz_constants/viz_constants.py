from constants import blockNames

def get_runType_colors():
    runType_colors = {  
                blockNames.RunTypes.E:'#1f77b4', # muted blue
                blockNames.RunTypes.M:'#ff7f0e', # safety orange
                blockNames.RunTypes.T:'#2ca02c', # cooked asparagus green
                blockNames.RunTypes.I:'#d62728', # brick red
                blockNames.RunTypes.R:'#9467bd', # muted purple
                blockNames.RunTypes.C:'#17becf', # blue-teal
                blockNames.RunTypes.X:'#8c564b', # chestnut brown
                blockNames.RunTypes.XB:'#bb6600'}
    return runType_colors
