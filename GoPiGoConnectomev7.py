# GoPiGo Connectome
# Written by Timothy Busbice, (c) 2014, in Python 2.7
# The GoPiGo Connectome uses a Postsynaptic dictionary based on the C Elegans Connectome Model
# This application can be ran on the Raspberry Pi GoPiGo robot with a Sonar that represents Nose Touch when activated
# To run standalone without a GoPiGo robot, simply comment out the sections with Start and End comments 
## Start Comment
from gopigo import *
## End Comment
import time
import copy

# The postsynaptic dictionary contains the accumulated weighted values as the
# connectome is executed
global postsynaptic = {}
global thisState = 0 
global nextState = 1

# The Threshold is the maximum sccumulated value that must be exceeded before
# the Neurite will fire
threshold = 30

# Accumulators are used to decide the value to send to the Left and Right motors
# of the GoPiGo robot
accumleft = 0
accumright = 0

# Used to remove from Axon firing since muscles cannot fire.
muscles = ['MVU', 'MVL', 'MDL', 'MVR', 'MDR']

# Used to accumulate muscle weighted values in body muscles 07-23 = worm locomotion
musDleft = ['MDL07', 'MDL08', 'MDL09', 'MDL10', 'MDL11', 'MDL12', 'MDL13', 'MDL14', 'MDL15', 'MDL16', 'MDL17', 'MDL18', 'MDL19', 'MDL20', 'MDL21', 'MDL22', 'MDL23']
musVleft = ['MVL07', 'MVL08', 'MVL09', 'MVL10', 'MVL11', 'MVL12', 'MVL13', 'MVL14', 'MVL15', 'MVL16', 'MVL17', 'MVL18', 'MVL19', 'MVL20', 'MVL21', 'MVL22', 'MVL23']
musDright = ['MDR07', 'MDR08', 'MDR09', 'MDR10', 'MDR11', 'MDR12', 'MDR13', 'MDR14', 'MDR15', 'MDR16', 'MDR17', 'MDR18', 'MDR19', 'MDR20', 'MDL21', 'MDR22', 'MDR23']
musVright = ['MVR07', 'MVR08', 'MVR09', 'MVR10', 'MVR11', 'MVR12', 'MVR13', 'MVR14', 'MVR15', 'MVR16', 'MVR17', 'MVR18', 'MVR19', 'MVR20', 'MVL21', 'MVR22', 'MVR23']

# This is the full C Elegans Connectome as expresed in the form of the Presynatptic
# neurite and the postsynaptic neurites
# postsynaptic['ADAR'][nextState] = (2 + postsynaptic['ADAR'][thisState])
# arr=postsynaptic['AIBR']

def ADAL():
        postsynaptic['ADAR'][nextState] = 2 + postsynaptic['ADAR'][thisState] 
        postsynaptic['ADFL'][nextState] = 1 + postsynaptic['ADFL'][thisState]
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 2 + postsynaptic['AIBR'][thisState]
        postsynaptic['ASHL'][nextState] = 1 + postsynaptic['ASHL'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 4 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 7 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVJR'][nextState] = 5 + postsynaptic['AVJR'][thisState]
        postsynaptic['FLPR'][nextState] = 1 + postsynaptic['FLPR'][thisState]
        postsynaptic['PVQL'][nextState] = 1 + postsynaptic['PVQL'][thisState]
        postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
        postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
        postsynaptic['RIML'][nextState] = 3 + postsynaptic['RIML'][thisState]
        postsynaptic['RIPL'][nextState] = 1 + postsynaptic['RIPL'][thisState]
        postsynaptic['SMDVR'][nextState] = 2 + postsynaptic['SMDVR'][thisState]

def ADAR():
        postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
        postsynaptic['ADFR'][nextState] = 1 + postsynaptic['ADFR'][thisState]
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['ASHR'][nextState] = 1 + postsynaptic['ASHR'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 5 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 2 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVJL'][nextState] = 3 + postsynaptic['AVJL'][thisState]
        postsynaptic['PVQR'][nextState] = 1 + postsynaptic['PVQR'][thisState]
        postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
        postsynaptic['RIMR'][nextState] = 5 + postsynaptic['RIMR'][thisState]
        postsynaptic['RIPR'][nextState] = 1 + postsynaptic['RIPR'][thisState]
        postsynaptic['RIVR'][nextState] = 1 + postsynaptic['RIVR'][thisState]
        postsynaptic['SMDVL'][nextState] = 2 + postsynaptic['SMDVL'][thisState]

def ADEL():
        postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
        postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
        postsynaptic['AINL'][nextState] = 1 + postsynaptic['AINL'][thisState]
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 3 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVKR'][nextState] = 1 + postsynaptic['AVKR'][thisState]
        postsynaptic['AVL'][nextState] = 1 + postsynaptic['AVL'][thisState]
        postsynaptic['BDUL'][nextState] = 1 + postsynaptic['BDUL'][thisState]
        postsynaptic['CEPDL'][nextState] = 1 + postsynaptic['CEPDL'][thisState]
        postsynaptic['FLPL'][nextState] = 1 + postsynaptic['FLPL'][thisState]
        postsynaptic['IL1L'][nextState] = 1 + postsynaptic['IL1L'][thisState]
        postsynaptic['IL2L'][nextState] = 1 + postsynaptic['IL2L'][thisState]
        postsynaptic['MDL05'][nextState] = 1 + postsynaptic['MDL05'][thisState]
        postsynaptic['OLLL'][nextState] = 1 + postsynaptic['OLLL'][thisState]
        postsynaptic['RIAL'][nextState] = 1 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIFL'][nextState] = 1 + postsynaptic['RIFL'][thisState]
        postsynaptic['RIGL'][nextState] = 5 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIGR'][nextState] = 3 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIH'][nextState] = 2 + postsynaptic['RIH'][thisState]
        postsynaptic['RIVL'][nextState] = 1 + postsynaptic['RIVL'][thisState]
        postsynaptic['RIVR'][nextState] = 1 + postsynaptic['RIVR'][thisState]
        postsynaptic['RMDL'][nextState] = 2 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]
        postsynaptic['RMHL'][nextState] = 1 + postsynaptic['RMHL'][thisState]
        postsynaptic['SIADR'][nextState] = 1 + postsynaptic['SIADR'][thisState]
        postsynaptic['SIBDR'][nextState] = 1 + postsynaptic['SIBDR'][thisState]
        postsynaptic['SMBDR'][nextState] = 1 + postsynaptic['SMBDR'][thisState]
        postsynaptic['URBL'][nextState] = 1 + postsynaptic['URBL'][thisState]

def ADER():
        postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]
        postsynaptic['ADEL'][nextState] = 2 + postsynaptic['ADEL'][thisState]
        postsynaptic['ALA'][nextState] = 1 + postsynaptic['ALA'][thisState]
        postsynaptic['AVAL'][nextState] = 5 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['AVJR'][nextState] = 1 + postsynaptic['AVJR'][thisState]
        postsynaptic['AVKL'][nextState] = 2 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 1 + postsynaptic['AVKR'][thisState]
        postsynaptic['CEPDR'][nextState] = 1 + postsynaptic['CEPDR'][thisState]
        postsynaptic['FLPL'][nextState] = 1 + postsynaptic['FLPL'][thisState]
        postsynaptic['FLPR'][nextState] = 1 + postsynaptic['FLPR'][thisState]
        postsynaptic['OLLR'][nextState] = 2 + postsynaptic['OLLR'][thisState]
        postsynaptic['PVR'][nextState] = 1 + postsynaptic['PVR'][thisState]
        postsynaptic['RIGL'][nextState] = 7 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIGR'][nextState] = 4 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]
        postsynaptic['RMDR'][nextState] = 2 + postsynaptic['RMDR'][thisState]
        postsynaptic['SAAVR'][nextState] = 1 + postsynaptic['SAAVR'][thisState]

def ADFL():
        postsynaptic['ADAL'][nextState] = 2 + postsynaptic['ADAL'][thisState]
        postsynaptic['AIZL'][nextState] = 12 + postsynaptic['AIZL'][thisState]
        postsynaptic['AUAL'][nextState] = 5 + postsynaptic['AUAL'][thisState]
        postsynaptic['OLQVL'][nextState] = 1 + postsynaptic['OLQVL'][thisState]
        postsynaptic['RIAL'][nextState] = 15 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIR'][nextState] = 2 + postsynaptic['RIR'][thisState]
        postsynaptic['SMBVL'][nextState] = 2 + postsynaptic['SMBVL'][thisState]

def ADFR():
        postsynaptic['ADAR'][nextState] = 2 + postsynaptic['ADAR'][thisState]
        postsynaptic['AIAR'][nextState] = 1 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIYR'][nextState] = 1 + postsynaptic['AIYR'][thisState]
        postsynaptic['AIZR'][nextState] = 8 + postsynaptic['AIZR'][thisState]
        postsynaptic['ASHR'][nextState] = 1 + postsynaptic['ASHR'][thisState]
        postsynaptic['AUAR'][nextState] = 4 + postsynaptic['AUAR'][thisState]
        postsynaptic['AWBR'][nextState] = 1 + postsynaptic['AWBR'][thisState]
        postsynaptic['PVPR'][nextState] = 1 + postsynaptic['PVPR'][thisState]
        postsynaptic['RIAR'][nextState] = 16 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIGR'][nextState] = 3 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIR'][nextState] = 3 + postsynaptic['RIR'][thisState]
        postsynaptic['SMBDR'][nextState] = 1 + postsynaptic['SMBDR'][thisState]
        postsynaptic['SMBVR'][nextState] = 2 + postsynaptic['SMBVR'][thisState]
        postsynaptic['URXR'][nextState] = 1 + postsynaptic['URXR'][thisState]

def ADLL():
        postsynaptic['ADLR'][nextState] = 1 + postsynaptic['ADLR'][thisState]
        postsynaptic['AIAL'][nextState] = 6 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIBL'][nextState] = 7 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['ALA'][nextState] = 2 + postsynaptic['ALA'][thisState]
        postsynaptic['ASER'][nextState] = 3 + postsynaptic['ASER'][thisState]
        postsynaptic['ASHL'][nextState] = 2 + postsynaptic['ASHL'][thisState]
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 3 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 4 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVJR'][nextState] = 3 + postsynaptic['AVJR'][thisState]
        postsynaptic['AWBL'][nextState] = 2 + postsynaptic['AWBL'][thisState]
        postsynaptic['OLQVL'][nextState] = 2 + postsynaptic['OLQVL'][thisState]
        postsynaptic['RIPL'][nextState] = 1 + postsynaptic['RIPL'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]

def ADLR():
        postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]
        postsynaptic['AIAR'][nextState] = 10 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIBR'][nextState] = 10 + postsynaptic['AIBR'][thisState]
        postsynaptic['ASER'][nextState] = 1 + postsynaptic['ASER'][thisState]
        postsynaptic['ASHR'][nextState] = 3 + postsynaptic['ASHR'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 5 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVJR'][nextState] = 1 + postsynaptic['AVJR'][thisState]
        postsynaptic['AWCR'][nextState] = 3 + postsynaptic['AWCR'][thisState]
        postsynaptic['OLLR'][nextState] = 1 + postsynaptic['OLLR'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
        postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]

def AFDL():
        postsynaptic['AFDR'][nextState] = 1 + postsynaptic['AFDR'][thisState]
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['AINR'][nextState] = 1 + postsynaptic['AINR'][thisState]
        postsynaptic['AIYL'][nextState] = 7 + postsynaptic['AIYL'][thisState]

def AFDR():
        postsynaptic['AFDL'][nextState] = 1 + postsynaptic['AFDL'][thisState]
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIYR'][nextState] = 13 + postsynaptic['AIYR'][thisState]
        postsynaptic['ASER'][nextState] = 1 + postsynaptic['ASER'][thisState]
                   
def AIAL():
        postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
        postsynaptic['AIAR'][nextState] = 1 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIBL'][nextState] = 10 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIML'][nextState] = 2 + postsynaptic['AIML'][thisState]
        postsynaptic['AIZL'][nextState] = 1 + postsynaptic['AIZL'][thisState]
        postsynaptic['ASER'][nextState] = 3 + postsynaptic['ASER'][thisState]
        postsynaptic['ASGL'][nextState] = 1 + postsynaptic['ASGL'][thisState]
        postsynaptic['ASHL'][nextState] = 1 + postsynaptic['ASHL'][thisState]
        postsynaptic['ASIL'][nextState] = 2 + postsynaptic['ASIL'][thisState]
        postsynaptic['ASKL'][nextState] = 3 + postsynaptic['ASKL'][thisState]
        postsynaptic['AWAL'][nextState] = 1 + postsynaptic['AWAL'][thisState]
        postsynaptic['AWCR'][nextState] = 1 + postsynaptic['AWCR'][thisState]
        postsynaptic['HSNL'][nextState] = 1 + postsynaptic['HSNL'][thisState]
        postsynaptic['RIFL'][nextState] = 1 + postsynaptic['RIFL'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]

def AIAR():
        postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]
        postsynaptic['ADFR'][nextState] = 1 + postsynaptic['ADFR'][thisState]
        postsynaptic['ADLR'][nextState] = 2 + postsynaptic['ADLR'][thisState]
        postsynaptic['AIAL'][nextState] = 1 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIBR'][nextState] = 14 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIZR'][nextState] = 1 + postsynaptic['AIZR'][thisState]
        postsynaptic['ASER'][nextState] = 1 + postsynaptic['ASER'][thisState]
        postsynaptic['ASGR'][nextState] = 1 + postsynaptic['ASGR'][thisState]
        postsynaptic['ASIR'][nextState] = 2 + postsynaptic['ASIR'][thisState]
        postsynaptic['AWAR'][nextState] = 2 + postsynaptic['AWAR'][thisState]
        postsynaptic['AWCL'][nextState] = 1 + postsynaptic['AWCL'][thisState]
        postsynaptic['AWCR'][nextState] = 3 + postsynaptic['AWCR'][thisState]
        postsynaptic['RIFR'][nextState] = 2 + postsynaptic['RIFR'][thisState]

def AIBL():
        postsynaptic['AFDL'][nextState] = 1 + postsynaptic['AFDL'][thisState]
        postsynaptic['AIYL'][nextState] = 1 + postsynaptic['AIYL'][thisState]
        postsynaptic['ASER'][nextState] = 1 + postsynaptic['ASER'][thisState]
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVBL'][nextState] = 5 + postsynaptic['AVBL'][thisState]
        postsynaptic['DVC'][nextState] = 1 + postsynaptic['DVC'][thisState]
        postsynaptic['FLPL'][nextState] = 1 + postsynaptic['FLPL'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['RIBR'][nextState] = 4 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIFL'][nextState] = 1 + postsynaptic['RIFL'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIGR'][nextState] = 3 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIML'][nextState] = 2 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 13 + postsynaptic['RIMR'][thisState]
        postsynaptic['RIMR'][nextState] = 1 + postsynaptic['RIMR'][thisState]
        postsynaptic['RIVL'][nextState] = 1 + postsynaptic['RIVL'][thisState]
        postsynaptic['SAADL'][nextState] = 2 + postsynaptic['SAADL'][thisState]
        postsynaptic['SAADR'][nextState] = 2 + postsynaptic['SAADR'][thisState]
        postsynaptic['SMDDR'][nextState] = 4 + postsynaptic['SMDDR'][thisState]

def AIBR():
        postsynaptic['AFDR'][nextState] = 1 + postsynaptic['AFDR'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBR'][nextState] = 3 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['DB1'][nextState] = 1 + postsynaptic['DB1'][thisState]
        postsynaptic['DVC'][nextState] = 2 + postsynaptic['DVC'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['RIAL'][nextState] = 1 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIBL'][nextState] = 4 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIGL'][nextState] = 3 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIML'][nextState] = 16 + postsynaptic['RIML'][thisState]
        postsynaptic['RIML'][nextState] = 1 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 1 + postsynaptic['RIMR'][thisState]
        postsynaptic['RIS'][nextState] = 1 + postsynaptic['RIS'][thisState]
        postsynaptic['RIVR'][nextState] = 1 + postsynaptic['RIVR'][thisState]
        postsynaptic['SAADL'][nextState] = 1 + postsynaptic['SAADL'][thisState]
        postsynaptic['SMDDL'][nextState] = 3 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDVL'][nextState] = 1 + postsynaptic['SMDVL'][thisState]
        postsynaptic['VB1'][nextState] = 3 + postsynaptic['VB1'][thisState]

def AIML():
        postsynaptic['AIAL'][nextState] = 5 + postsynaptic['AIAL'][thisState]
        postsynaptic['ALML'][nextState] = 1 + postsynaptic['ALML'][thisState]
        postsynaptic['ASGL'][nextState] = 2 + postsynaptic['ASGL'][thisState]
        postsynaptic['ASKL'][nextState] = 2 + postsynaptic['ASKL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['AVFL'][nextState] = 4 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVFR'][nextState] = 1 + postsynaptic['AVFR'][thisState]
        postsynaptic['AVHL'][nextState] = 2 + postsynaptic['AVHL'][thisState]
        postsynaptic['AVHR'][nextState] = 1 + postsynaptic['AVHR'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['PVQL'][nextState] = 1 + postsynaptic['PVQL'][thisState]
        postsynaptic['RIFL'][nextState] = 1 + postsynaptic['RIFL'][thisState]
        postsynaptic['SIBDR'][nextState] = 1 + postsynaptic['SIBDR'][thisState]
        postsynaptic['SMBVL'][nextState] = 1 + postsynaptic['SMBVL'][thisState]

def AIMR():
        postsynaptic['AIAR'][nextState] = 5 + postsynaptic['AIAR'][thisState]
        postsynaptic['ASGR'][nextState] = 2 + postsynaptic['ASGR'][thisState]
        postsynaptic['ASJR'][nextState] = 2 + postsynaptic['ASJR'][thisState]
        postsynaptic['ASKR'][nextState] = 3 + postsynaptic['ASKR'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVFL'][nextState] = 1 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVFR'][nextState] = 1 + postsynaptic['AVFR'][thisState]
        postsynaptic['HSNL'][nextState] = 1 + postsynaptic['HSNL'][thisState]
        postsynaptic['HSNR'][nextState] = 2 + postsynaptic['HSNR'][thisState]
        postsynaptic['OLQDR'][nextState] = 1 + postsynaptic['OLQDR'][thisState]
        postsynaptic['PVNR'][nextState] = 1 + postsynaptic['PVNR'][thisState]
        postsynaptic['RIFR'][nextState] = 1 + postsynaptic['RIFR'][thisState]
        postsynaptic['RMGR'][nextState] = 1 + postsynaptic['RMGR'][thisState]

def AINL():
        postsynaptic['ADEL'][nextState] = 1 + postsynaptic['ADEL'][thisState]
        postsynaptic['AFDR'][nextState] = 5 + postsynaptic['AFDR'][thisState]
        postsynaptic['AINR'][nextState] = 2 + postsynaptic['AINR'][thisState]
        postsynaptic['ASEL'][nextState] = 3 + postsynaptic['ASEL'][thisState]
        postsynaptic['ASGR'][nextState] = 2 + postsynaptic['ASGR'][thisState]
        postsynaptic['AUAR'][nextState] = 2 + postsynaptic['AUAR'][thisState]
        postsynaptic['BAGL'][nextState] = 3 + postsynaptic['BAGL'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 2 + postsynaptic['RIBR'][thisState]

def AINR():
        postsynaptic['AFDL'][nextState] = 4 + postsynaptic['AFDL'][thisState]
        postsynaptic['AFDR'][nextState] = 1 + postsynaptic['AFDR'][thisState]
        postsynaptic['AIAL'][nextState] = 2 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIBL'][nextState] = 2 + postsynaptic['AIBL'][thisState]
        postsynaptic['AINL'][nextState] = 2 + postsynaptic['AINL'][thisState]
        postsynaptic['ASEL'][nextState] = 1 + postsynaptic['ASEL'][thisState]
        postsynaptic['ASER'][nextState] = 1 + postsynaptic['ASER'][thisState]
        postsynaptic['ASGL'][nextState] = 1 + postsynaptic['ASGL'][thisState]
        postsynaptic['AUAL'][nextState] = 1 + postsynaptic['AUAL'][thisState]
        postsynaptic['AUAR'][nextState] = 1 + postsynaptic['AUAR'][thisState]
        postsynaptic['BAGR'][nextState] = 3 + postsynaptic['BAGR'][thisState]
        postsynaptic['RIBL'][nextState] = 2 + postsynaptic['RIBL'][thisState]
        postsynaptic['RID'][nextState] = 1 + postsynaptic['RID'][thisState]

def AIYL():
        postsynaptic['AIYR'][nextState] = 1 + postsynaptic['AIYR'][thisState]
        postsynaptic['AIZL'][nextState] = 13 + postsynaptic['AIZL'][thisState]
        postsynaptic['AWAL'][nextState] = 3 + postsynaptic['AWAL'][thisState]
        postsynaptic['AWCL'][nextState] = 1 + postsynaptic['AWCL'][thisState]
        postsynaptic['AWCR'][nextState] = 1 + postsynaptic['AWCR'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['RIAL'][nextState] = 7 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIBL'][nextState] = 4 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIML'][nextState] = 1 + postsynaptic['RIML'][thisState]

def AIYR():
        postsynaptic['ADFR'][nextState] = 1 + postsynaptic['ADFR'][thisState]
        postsynaptic['AIYL'][nextState] = 1 + postsynaptic['AIYL'][thisState]
        postsynaptic['AIZR'][nextState] = 8 + postsynaptic['AIZR'][thisState]
        postsynaptic['AWAR'][nextState] = 1 + postsynaptic['AWAR'][thisState]
        postsynaptic['HSNL'][nextState] = 1 + postsynaptic['HSNL'][thisState]
        postsynaptic['RIAR'][nextState] = 6 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIBR'][nextState] = 2 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIMR'][nextState] = 1 + postsynaptic['RIMR'][thisState]

def AIZL():
        postsynaptic['AIAL'][nextState] = 3 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIBL'][nextState] = 2 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 8 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIZR'][nextState] = 2 + postsynaptic['AIZR'][thisState]
        postsynaptic['ASEL'][nextState] = 1 + postsynaptic['ASEL'][thisState]
        postsynaptic['ASGL'][nextState] = 1 + postsynaptic['ASGL'][thisState]
        postsynaptic['ASHL'][nextState] = 1 + postsynaptic['ASHL'][thisState]
        postsynaptic['AVER'][nextState] = 5 + postsynaptic['AVER'][thisState]
        postsynaptic['DVA'][nextState] = 1 + postsynaptic['DVA'][thisState]
        postsynaptic['RIAL'][nextState] = 8 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIML'][nextState] = 4 + postsynaptic['RIML'][thisState]
        postsynaptic['SMBDL'][nextState] = 9 + postsynaptic['SMBDL'][thisState]
        postsynaptic['SMBVL'][nextState] = 7 + postsynaptic['SMBVL'][thisState]
        postsynaptic['VB2'][nextState] = 1 + postsynaptic['VB2'][thisState]

def AIZR():
        postsynaptic['AIAR'][nextState] = 1 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIBL'][nextState] = 8 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIZL'][nextState] = 2 + postsynaptic['AIZL'][thisState]
        postsynaptic['ASGR'][nextState] = 1 + postsynaptic['ASGR'][thisState]
        postsynaptic['ASHR'][nextState] = 1 + postsynaptic['ASHR'][thisState]
        postsynaptic['AVEL'][nextState] = 4 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['AWAR'][nextState] = 1 + postsynaptic['AWAR'][thisState]
        postsynaptic['DVA'][nextState] = 1 + postsynaptic['DVA'][thisState]
        postsynaptic['RIAR'][nextState] = 7 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIMR'][nextState] = 4 + postsynaptic['RIMR'][thisState]
        postsynaptic['SMBDR'][nextState] = 5 + postsynaptic['SMBDR'][thisState]
        postsynaptic['SMBVR'][nextState] = 3 + postsynaptic['SMBVR'][thisState]
        postsynaptic['SMDDR'][nextState] = 1 + postsynaptic['SMDDR'][thisState]

def ALA():
        postsynaptic['ADEL'][nextState] = 1 + postsynaptic['ADEL'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVEL'][nextState] = 2 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['RID'][nextState] = 1 + postsynaptic['RID'][thisState]
        postsynaptic['RMDR'][nextState] = 1 + postsynaptic['RMDR'][thisState]

def ALML():
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVM'][nextState] = 1 + postsynaptic['AVM'][thisState]
        postsynaptic['BDUL'][nextState] = 6 + postsynaptic['BDUL'][thisState]
        postsynaptic['CEPDL'][nextState] = 3 + postsynaptic['CEPDL'][thisState]
        postsynaptic['CEPVL'][nextState] = 2 + postsynaptic['CEPVL'][thisState]
        postsynaptic['PVCL'][nextState] = 2 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVR'][nextState] = 1 + postsynaptic['PVR'][thisState]
        postsynaptic['RMDDR'][nextState] = 1 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]
        postsynaptic['SDQL'][nextState] = 1 + postsynaptic['SDQL'][thisState]

def ALMR():
        postsynaptic['AVM'][nextState] = 1 + postsynaptic['AVM'][thisState]
        postsynaptic['BDUR'][nextState] = 5 + postsynaptic['BDUR'][thisState]
        postsynaptic['CEPDR'][nextState] = 1 + postsynaptic['CEPDR'][thisState]
        postsynaptic['CEPVR'][nextState] = 1 + postsynaptic['CEPVR'][thisState]
        postsynaptic['PVCR'][nextState] = 3 + postsynaptic['PVCR'][thisState]
        postsynaptic['RMDDL'][nextState] = 1 + postsynaptic['RMDDL'][thisState]
        postsynaptic['SIADL'][nextState] = 1 + postsynaptic['SIADL'][thisState]

def ALNL():
        postsynaptic['SAAVL'][nextState] = 3 + postsynaptic['SAAVL'][thisState]
        postsynaptic['SMBDR'][nextState] = 2 + postsynaptic['SMBDR'][thisState]
        postsynaptic['SMBDR'][nextState] = 1 + postsynaptic['SMBDR'][thisState]
        postsynaptic['SMDVL'][nextState] = 1 + postsynaptic['SMDVL'][thisState]

def ALNR():
        postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
        postsynaptic['RMHR'][nextState] = 1 + postsynaptic['RMHR'][thisState]
        postsynaptic['SAAVR'][nextState] = 2 + postsynaptic['SAAVR'][thisState]
        postsynaptic['SMBDL'][nextState] = 2 + postsynaptic['SMBDL'][thisState]
        postsynaptic['SMDDR'][nextState] = 1 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVL'][nextState] = 1 + postsynaptic['SMDVL'][thisState]

def AQR():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 3 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 3 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 4 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVKL'][nextState] = 2 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 1 + postsynaptic['AVKR'][thisState]
        postsynaptic['BAGL'][nextState] = 2 + postsynaptic['BAGL'][thisState]
        postsynaptic['BAGR'][nextState] = 2 + postsynaptic['BAGR'][thisState]
        postsynaptic['PVCR'][nextState] = 2 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVPL'][nextState] = 1 + postsynaptic['PVPL'][thisState]
        postsynaptic['PVPL'][nextState] = 7 + postsynaptic['PVPL'][thisState]
        postsynaptic['PVPR'][nextState] = 9 + postsynaptic['PVPR'][thisState]
        postsynaptic['RIAL'][nextState] = 3 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 1 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIGL'][nextState] = 2 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['URXL'][nextState] = 1 + postsynaptic['URXL'][thisState]

def AS1():
        postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['DA1'][nextState] = 2 + postsynaptic['DA1'][thisState]
        postsynaptic['MDL05'][nextState] = 3 + postsynaptic['MDL05'][thisState]
        postsynaptic['MDL08'][nextState] = 3 + postsynaptic['MDL08'][thisState]
        postsynaptic['MDR05'][nextState] = 3 + postsynaptic['MDR05'][thisState]
        postsynaptic['MDR08'][nextState] = 4 + postsynaptic['MDR08'][thisState]
        postsynaptic['VA3'][nextState] = 1 + postsynaptic['VA3'][thisState]
        postsynaptic['VD1'][nextState] = 5 + postsynaptic['VD1'][thisState]
        postsynaptic['VD2'][nextState] = 1 + postsynaptic['VD2'][thisState]

def AS2():
        postsynaptic['DA2'][nextState] = 1 + postsynaptic['DA2'][thisState]
        postsynaptic['DB1'][nextState] = 1 + postsynaptic['DB1'][thisState]
        postsynaptic['DD1'][nextState] = 1 + postsynaptic['DD1'][thisState]
        postsynaptic['MDL07'][nextState] = 3 + postsynaptic['MDL07'][thisState]
        postsynaptic['MDL08'][nextState] = 2 + postsynaptic['MDL08'][thisState]
        postsynaptic['MDR07'][nextState] = 3 + postsynaptic['MDR07'][thisState]
        postsynaptic['MDR08'][nextState] = 3 + postsynaptic['MDR08'][thisState]
        postsynaptic['VA4'][nextState] = 2 + postsynaptic['VA4'][thisState]
        postsynaptic['VD2'][nextState] = 10 + postsynaptic['VD2'][thisState]

def AS3():
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['DA2'][nextState] = 1 + postsynaptic['DA2'][thisState]
        postsynaptic['DA3'][nextState] = 1 + postsynaptic['DA3'][thisState]
        postsynaptic['DD1'][nextState] = 1 + postsynaptic['DD1'][thisState]
        postsynaptic['MDL09'][nextState] = 3 + postsynaptic['MDL09'][thisState]
        postsynaptic['MDL10'][nextState] = 3 + postsynaptic['MDL10'][thisState]
        postsynaptic['MDR09'][nextState] = 3 + postsynaptic['MDR09'][thisState]
        postsynaptic['MDR10'][nextState] = 3 + postsynaptic['MDR10'][thisState]
        postsynaptic['VA5'][nextState] = 2 + postsynaptic['VA5'][thisState]
        postsynaptic['VD2'][nextState] = 1 + postsynaptic['VD2'][thisState]
        postsynaptic['VD3'][nextState] = 15 + postsynaptic['VD3'][thisState]

def AS4():
        postsynaptic['AS5'][nextState] = 1 + postsynaptic['AS5'][thisState]
        postsynaptic['DA3'][nextState] = 1 + postsynaptic['DA3'][thisState]
        postsynaptic['MDL11'][nextState] = 2 + postsynaptic['MDL11'][thisState]
        postsynaptic['MDL12'][nextState] = 2 + postsynaptic['MDL12'][thisState]
        postsynaptic['MDR11'][nextState] = 3 + postsynaptic['MDR11'][thisState]
        postsynaptic['MDR12'][nextState] = 2 + postsynaptic['MDR12'][thisState]
        postsynaptic['VD4'][nextState] = 11 + postsynaptic['VD4'][thisState]

def AS5():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['DD2'][nextState] = 1 + postsynaptic['DD2'][thisState]
        postsynaptic['MDL11'][nextState] = 2 + postsynaptic['MDL11'][thisState]
        postsynaptic['MDL14'][nextState] = 3 + postsynaptic['MDL14'][thisState]
        postsynaptic['MDR11'][nextState] = 2 + postsynaptic['MDR11'][thisState]
        postsynaptic['MDR14'][nextState] = 3 + postsynaptic['MDR14'][thisState]
        postsynaptic['VA7'][nextState] = 1 + postsynaptic['VA7'][thisState]
        postsynaptic['VD5'][nextState] = 9 + postsynaptic['VD5'][thisState]

def AS6():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DA5'][nextState] = 2 + postsynaptic['DA5'][thisState]
        postsynaptic['MDL13'][nextState] = 3 + postsynaptic['MDL13'][thisState]
        postsynaptic['MDL14'][nextState] = 2 + postsynaptic['MDL14'][thisState]
        postsynaptic['MDR13'][nextState] = 3 + postsynaptic['MDR13'][thisState]
        postsynaptic['MDR14'][nextState] = 2 + postsynaptic['MDR14'][thisState]
        postsynaptic['VA8'][nextState] = 1 + postsynaptic['VA8'][thisState]
        postsynaptic['VD6'][nextState] = 13 + postsynaptic['VD6'][thisState]

def AS7():
        postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 5 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['MDL13'][nextState] = 2 + postsynaptic['MDL13'][thisState]
        postsynaptic['MDL16'][nextState] = 3 + postsynaptic['MDL16'][thisState]
        postsynaptic['MDR13'][nextState] = 2 + postsynaptic['MDR13'][thisState]
        postsynaptic['MDR16'][nextState] = 3 + postsynaptic['MDR16'][thisState]

def AS8():
        postsynaptic['AVAL'][nextState] = 4 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 3 + postsynaptic['AVAR'][thisState]
        postsynaptic['MDL15'][nextState] = 2 + postsynaptic['MDL15'][thisState]
        postsynaptic['MDL18'][nextState] = 3 + postsynaptic['MDL18'][thisState]
        postsynaptic['MDR15'][nextState] = 2 + postsynaptic['MDR15'][thisState]
        postsynaptic['MDR18'][nextState] = 3 + postsynaptic['MDR18'][thisState]

def AS9():
        postsynaptic['AVAL'][nextState] = 4 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['DVB'][nextState] = 7 + postsynaptic['DVB'][thisState]
        postsynaptic['MDL17'][nextState] = 2 + postsynaptic['MDL17'][thisState]
        postsynaptic['MDL20'][nextState] = 3 + postsynaptic['MDL20'][thisState]
        postsynaptic['MDR17'][nextState] = 2 + postsynaptic['MDR17'][thisState]
        postsynaptic['MDR20'][nextState] = 3 + postsynaptic['MDR20'][thisState]

def AS10():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['MDL19'][nextState] = 3 + postsynaptic['MDL19'][thisState]
        postsynaptic['MDL20'][nextState] = 2 + postsynaptic['MDL20'][thisState]
        postsynaptic['MDR19'][nextState] = 3 + postsynaptic['MDR19'][thisState]
        postsynaptic['MDR20'][nextState] = 2 + postsynaptic['MDR20'][thisState]

def AS11():
        postsynaptic['MDL21'][nextState] = 1 + postsynaptic['MDL21'][thisState]
        postsynaptic['MDL22'][nextState] = 1 + postsynaptic['MDL22'][thisState]
        postsynaptic['MDL23'][nextState] = 1 + postsynaptic['MDL23'][thisState]
        postsynaptic['MDL24'][nextState] = 1 + postsynaptic['MDL24'][thisState]
        postsynaptic['MDR21'][nextState] = 1 + postsynaptic['MDR21'][thisState]
        postsynaptic['MDR22'][nextState] = 1 + postsynaptic['MDR22'][thisState]
        postsynaptic['MDR23'][nextState] = 1 + postsynaptic['MDR23'][thisState]
        postsynaptic['MDR24'][nextState] = 1 + postsynaptic['MDR24'][thisState]
        postsynaptic['PDA'][nextState] = 1 + postsynaptic['PDA'][thisState]
        postsynaptic['PDB'][nextState] = 1 + postsynaptic['PDB'][thisState]
        postsynaptic['PDB'][nextState] = 2 + postsynaptic['PDB'][thisState]
        postsynaptic['VD13'][nextState] = 2 + postsynaptic['VD13'][thisState]

def ASEL():
        postsynaptic['ADFR'][nextState] = 1 + postsynaptic['ADFR'][thisState]
        postsynaptic['AIAL'][nextState] = 3 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIBL'][nextState] = 7 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 2 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIYL'][nextState] = 13 + postsynaptic['AIYL'][thisState]
        postsynaptic['AIYR'][nextState] = 6 + postsynaptic['AIYR'][thisState]
        postsynaptic['AWCL'][nextState] = 4 + postsynaptic['AWCL'][thisState]
        postsynaptic['AWCR'][nextState] = 1 + postsynaptic['AWCR'][thisState]
        postsynaptic['RIAR'][nextState] = 1 + postsynaptic['RIAR'][thisState]

def ASER():
        postsynaptic['AFDL'][nextState] = 1 + postsynaptic['AFDL'][thisState]
        postsynaptic['AFDR'][nextState] = 2 + postsynaptic['AFDR'][thisState]
        postsynaptic['AIAL'][nextState] = 1 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIAR'][nextState] = 3 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIBL'][nextState] = 2 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 10 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIYL'][nextState] = 2 + postsynaptic['AIYL'][thisState]
        postsynaptic['AIYR'][nextState] = 14 + postsynaptic['AIYR'][thisState]
        postsynaptic['AWAR'][nextState] = 1 + postsynaptic['AWAR'][thisState]
        postsynaptic['AWCL'][nextState] = 1 + postsynaptic['AWCL'][thisState]
        postsynaptic['AWCR'][nextState] = 1 + postsynaptic['AWCR'][thisState]

def ASGL():
        postsynaptic['AIAL'][nextState] = 9 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIBL'][nextState] = 3 + postsynaptic['AIBL'][thisState]
        postsynaptic['AINR'][nextState] = 2 + postsynaptic['AINR'][thisState]
        postsynaptic['AIZL'][nextState] = 1 + postsynaptic['AIZL'][thisState]
        postsynaptic['ASKL'][nextState] = 1 + postsynaptic['ASKL'][thisState]

def ASGR():
        postsynaptic['AIAR'][nextState] = 10 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIBR'][nextState] = 2 + postsynaptic['AIBR'][thisState]
        postsynaptic['AINL'][nextState] = 1 + postsynaptic['AINL'][thisState]
        postsynaptic['AIYR'][nextState] = 1 + postsynaptic['AIYR'][thisState]
        postsynaptic['AIZR'][nextState] = 1 + postsynaptic['AIZR'][thisState]

def ASHL():
        postsynaptic['ADAL'][nextState] = 2 + postsynaptic['ADAL'][thisState]
        postsynaptic['ADFL'][nextState] = 3 + postsynaptic['ADFL'][thisState]
        postsynaptic['AIAL'][nextState] = 7 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIBL'][nextState] = 5 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIZL'][nextState] = 1 + postsynaptic['AIZL'][thisState]
        postsynaptic['ASHR'][nextState] = 1 + postsynaptic['ASHR'][thisState]
        postsynaptic['ASKL'][nextState] = 1 + postsynaptic['ASKL'][thisState]
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVBL'][nextState] = 6 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVDL'][nextState] = 2 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['RIAL'][nextState] = 4 + postsynaptic['RIAL'][thisState]
        postsynaptic['RICL'][nextState] = 2 + postsynaptic['RICL'][thisState]
        postsynaptic['RIML'][nextState] = 1 + postsynaptic['RIML'][thisState]
        postsynaptic['RIPL'][nextState] = 1 + postsynaptic['RIPL'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]

def ASHR():
        postsynaptic['ADAR'][nextState] = 3 + postsynaptic['ADAR'][thisState]
        postsynaptic['ADFR'][nextState] = 2 + postsynaptic['ADFR'][thisState]
        postsynaptic['AIAR'][nextState] = 10 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIBR'][nextState] = 3 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIZR'][nextState] = 1 + postsynaptic['AIZR'][thisState]
        postsynaptic['ASHL'][nextState] = 1 + postsynaptic['ASHL'][thisState]
        postsynaptic['ASKR'][nextState] = 1 + postsynaptic['ASKR'][thisState]
        postsynaptic['AVAR'][nextState] = 5 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBR'][nextState] = 3 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 5 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVER'][nextState] = 3 + postsynaptic['AVER'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['PVPR'][nextState] = 1 + postsynaptic['PVPR'][thisState]
        postsynaptic['RIAR'][nextState] = 2 + postsynaptic['RIAR'][thisState]
        postsynaptic['RICR'][nextState] = 2 + postsynaptic['RICR'][thisState]
        postsynaptic['RMGR'][nextState] = 2 + postsynaptic['RMGR'][thisState]
        postsynaptic['RMGR'][nextState] = 1 + postsynaptic['RMGR'][thisState]

def ASIL():
        postsynaptic['AIAL'][nextState] = 2 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIYL'][nextState] = 2 + postsynaptic['AIYL'][thisState]
        postsynaptic['AIZL'][nextState] = 1 + postsynaptic['AIZL'][thisState]
        postsynaptic['ASER'][nextState] = 1 + postsynaptic['ASER'][thisState]
        postsynaptic['ASIR'][nextState] = 1 + postsynaptic['ASIR'][thisState]
        postsynaptic['ASKL'][nextState] = 2 + postsynaptic['ASKL'][thisState]
        postsynaptic['AWCL'][nextState] = 1 + postsynaptic['AWCL'][thisState]
        postsynaptic['AWCR'][nextState] = 1 + postsynaptic['AWCR'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]

def ASIR():
        postsynaptic['AIAL'][nextState] = 1 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIAR'][nextState] = 3 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIAR'][nextState] = 2 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['ASEL'][nextState] = 2 + postsynaptic['ASEL'][thisState]
        postsynaptic['ASHR'][nextState] = 1 + postsynaptic['ASHR'][thisState]
        postsynaptic['ASIL'][nextState] = 1 + postsynaptic['ASIL'][thisState]
        postsynaptic['AWCL'][nextState] = 1 + postsynaptic['AWCL'][thisState]
        postsynaptic['AWCR'][nextState] = 1 + postsynaptic['AWCR'][thisState]

def ASJL():
        postsynaptic['ASJR'][nextState] = 1 + postsynaptic['ASJR'][thisState]
        postsynaptic['ASKL'][nextState] = 4 + postsynaptic['ASKL'][thisState]
        postsynaptic['HSNL'][nextState] = 1 + postsynaptic['HSNL'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['PVQL'][nextState] = 14 + postsynaptic['PVQL'][thisState]

def ASJR():
        postsynaptic['ASJL'][nextState] = 1 + postsynaptic['ASJL'][thisState]
        postsynaptic['ASKR'][nextState] = 4 + postsynaptic['ASKR'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['PVQR'][nextState] = 13 + postsynaptic['PVQR'][thisState]

def ASKL():
        postsynaptic['AIAL'][nextState] = 11 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIBL'][nextState] = 2 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIML'][nextState] = 2 + postsynaptic['AIML'][thisState]
        postsynaptic['ASKR'][nextState] = 1 + postsynaptic['ASKR'][thisState]
        postsynaptic['PVQL'][nextState] = 5 + postsynaptic['PVQL'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]

def ASKR():
        postsynaptic['AIAR'][nextState] = 11 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIMR'][nextState] = 1 + postsynaptic['AIMR'][thisState]
        postsynaptic['ASHR'][nextState] = 1 + postsynaptic['ASHR'][thisState]
        postsynaptic['ASKL'][nextState] = 1 + postsynaptic['ASKL'][thisState]
        postsynaptic['AWAR'][nextState] = 1 + postsynaptic['AWAR'][thisState]
        postsynaptic['CEPVR'][nextState] = 1 + postsynaptic['CEPVR'][thisState]
        postsynaptic['PVQR'][nextState] = 4 + postsynaptic['PVQR'][thisState]
        postsynaptic['RIFR'][nextState] = 1 + postsynaptic['RIFR'][thisState]
        postsynaptic['RMGR'][nextState] = 1 + postsynaptic['RMGR'][thisState]

def AUAL():
        postsynaptic['AINR'][nextState] = 1 + postsynaptic['AINR'][thisState]
        postsynaptic['AUAR'][nextState] = 1 + postsynaptic['AUAR'][thisState]
        postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 3 + postsynaptic['AVEL'][thisState]
        postsynaptic['AWBL'][nextState] = 1 + postsynaptic['AWBL'][thisState]
        postsynaptic['RIAL'][nextState] = 5 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIBL'][nextState] = 9 + postsynaptic['RIBL'][thisState]

def AUAR():
        postsynaptic['AINL'][nextState] = 1 + postsynaptic['AINL'][thisState]
        postsynaptic['AIYR'][nextState] = 1 + postsynaptic['AIYR'][thisState]
        postsynaptic['AUAL'][nextState] = 1 + postsynaptic['AUAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVER'][nextState] = 4 + postsynaptic['AVER'][thisState]
        postsynaptic['AWBR'][nextState] = 1 + postsynaptic['AWBR'][thisState]
        postsynaptic['RIAR'][nextState] = 6 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIBR'][nextState] = 13 + postsynaptic['RIBR'][thisState]
        postsynaptic['URXR'][nextState] = 1 + postsynaptic['URXR'][thisState]

def AVAL():
        postsynaptic['AS1'][nextState] = 3 + postsynaptic['AS1'][thisState]
        postsynaptic['AS10'][nextState] = 3 + postsynaptic['AS10'][thisState]
        postsynaptic['AS11'][nextState] = 4 + postsynaptic['AS11'][thisState]
        postsynaptic['AS2'][nextState] = 1 + postsynaptic['AS2'][thisState]
        postsynaptic['AS3'][nextState] = 3 + postsynaptic['AS3'][thisState]
        postsynaptic['AS4'][nextState] = 1 + postsynaptic['AS4'][thisState]
        postsynaptic['AS5'][nextState] = 4 + postsynaptic['AS5'][thisState]
        postsynaptic['AS6'][nextState] = 1 + postsynaptic['AS6'][thisState]
        postsynaptic['AS7'][nextState] = 14 + postsynaptic['AS7'][thisState]
        postsynaptic['AS8'][nextState] = 9 + postsynaptic['AS8'][thisState]
        postsynaptic['AS9'][nextState] = 12 + postsynaptic['AS9'][thisState]
        postsynaptic['AVAR'][nextState] = 7 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVHL'][nextState] = 1 + postsynaptic['AVHL'][thisState]
        postsynaptic['AVJL'][nextState] = 2 + postsynaptic['AVJL'][thisState]
        postsynaptic['DA1'][nextState] = 4 + postsynaptic['DA1'][thisState]
        postsynaptic['DA2'][nextState] = 4 + postsynaptic['DA2'][thisState]
        postsynaptic['DA3'][nextState] = 6 + postsynaptic['DA3'][thisState]
        postsynaptic['DA4'][nextState] = 10 + postsynaptic['DA4'][thisState]
        postsynaptic['DA5'][nextState] = 8 + postsynaptic['DA5'][thisState]
        postsynaptic['DA6'][nextState] = 21 + postsynaptic['DA6'][thisState]
        postsynaptic['DA7'][nextState] = 4 + postsynaptic['DA7'][thisState]
        postsynaptic['DA8'][nextState] = 4 + postsynaptic['DA8'][thisState]
        postsynaptic['DA9'][nextState] = 3 + postsynaptic['DA9'][thisState]
        postsynaptic['DB5'][nextState] = 2 + postsynaptic['DB5'][thisState]
        postsynaptic['DB6'][nextState] = 4 + postsynaptic['DB6'][thisState]
        postsynaptic['FLPL'][nextState] = 1 + postsynaptic['FLPL'][thisState]
        postsynaptic['LUAL'][nextState] = 2 + postsynaptic['LUAL'][thisState]
        postsynaptic['PVCL'][nextState] = 12 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 11 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVPL'][nextState] = 1 + postsynaptic['PVPL'][thisState]
        postsynaptic['RIMR'][nextState] = 3 + postsynaptic['RIMR'][thisState]
        postsynaptic['SABD'][nextState] = 4 + postsynaptic['SABD'][thisState]
        postsynaptic['SABVR'][nextState] = 1 + postsynaptic['SABVR'][thisState]
        postsynaptic['SDQR'][nextState] = 1 + postsynaptic['SDQR'][thisState]
        postsynaptic['URYDL'][nextState] = 1 + postsynaptic['URYDL'][thisState]
        postsynaptic['URYVR'][nextState] = 1 + postsynaptic['URYVR'][thisState]
        postsynaptic['VA1'][nextState] = 3 + postsynaptic['VA1'][thisState]
        postsynaptic['VA10'][nextState] = 6 + postsynaptic['VA10'][thisState]
        postsynaptic['VA11'][nextState] = 7 + postsynaptic['VA11'][thisState]
        postsynaptic['VA12'][nextState] = 2 + postsynaptic['VA12'][thisState]
        postsynaptic['VA2'][nextState] = 5 + postsynaptic['VA2'][thisState]
        postsynaptic['VA3'][nextState] = 3 + postsynaptic['VA3'][thisState]
        postsynaptic['VA4'][nextState] = 3 + postsynaptic['VA4'][thisState]
        postsynaptic['VA5'][nextState] = 8 + postsynaptic['VA5'][thisState]
        postsynaptic['VA6'][nextState] = 10 + postsynaptic['VA6'][thisState]
        postsynaptic['VA7'][nextState] = 2 + postsynaptic['VA7'][thisState]
        postsynaptic['VA8'][nextState] = 19 + postsynaptic['VA8'][thisState]
        postsynaptic['VA9'][nextState] = 8 + postsynaptic['VA9'][thisState]
        postsynaptic['VB9'][nextState] = 5 + postsynaptic['VB9'][thisState]

def AVAR():
        postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
        postsynaptic['AS1'][nextState] = 3 + postsynaptic['AS1'][thisState]
        postsynaptic['AS10'][nextState] = 2 + postsynaptic['AS10'][thisState]
        postsynaptic['AS11'][nextState] = 6 + postsynaptic['AS11'][thisState]
        postsynaptic['AS2'][nextState] = 2 + postsynaptic['AS2'][thisState]
        postsynaptic['AS3'][nextState] = 2 + postsynaptic['AS3'][thisState]
        postsynaptic['AS4'][nextState] = 1 + postsynaptic['AS4'][thisState]
        postsynaptic['AS5'][nextState] = 2 + postsynaptic['AS5'][thisState]
        postsynaptic['AS6'][nextState] = 3 + postsynaptic['AS6'][thisState]
        postsynaptic['AS7'][nextState] = 8 + postsynaptic['AS7'][thisState]
        postsynaptic['AS8'][nextState] = 9 + postsynaptic['AS8'][thisState]
        postsynaptic['AS9'][nextState] = 6 + postsynaptic['AS9'][thisState]
        postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 2 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 2 + postsynaptic['AVER'][thisState]
        postsynaptic['DA1'][nextState] = 8 + postsynaptic['DA1'][thisState]
        postsynaptic['DA2'][nextState] = 4 + postsynaptic['DA2'][thisState]
        postsynaptic['DA3'][nextState] = 5 + postsynaptic['DA3'][thisState]
        postsynaptic['DA4'][nextState] = 8 + postsynaptic['DA4'][thisState]
        postsynaptic['DA5'][nextState] = 7 + postsynaptic['DA5'][thisState]
        postsynaptic['DA6'][nextState] = 13 + postsynaptic['DA6'][thisState]
        postsynaptic['DA7'][nextState] = 3 + postsynaptic['DA7'][thisState]
        postsynaptic['DA8'][nextState] = 9 + postsynaptic['DA8'][thisState]
        postsynaptic['DA9'][nextState] = 2 + postsynaptic['DA9'][thisState]
        postsynaptic['DB3'][nextState] = 1 + postsynaptic['DB3'][thisState]
        postsynaptic['DB5'][nextState] = 3 + postsynaptic['DB5'][thisState]
        postsynaptic['DB6'][nextState] = 5 + postsynaptic['DB6'][thisState]
        postsynaptic['LUAL'][nextState] = 1 + postsynaptic['LUAL'][thisState]
        postsynaptic['LUAR'][nextState] = 3 + postsynaptic['LUAR'][thisState]
        postsynaptic['PDEL'][nextState] = 1 + postsynaptic['PDEL'][thisState]
        postsynaptic['PDER'][nextState] = 1 + postsynaptic['PDER'][thisState]
        postsynaptic['PVCL'][nextState] = 7 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 8 + postsynaptic['PVCR'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIML'][nextState] = 2 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 1 + postsynaptic['RIMR'][thisState]
        postsynaptic['SABD'][nextState] = 1 + postsynaptic['SABD'][thisState]
        postsynaptic['SABVL'][nextState] = 6 + postsynaptic['SABVL'][thisState]
        postsynaptic['SABVR'][nextState] = 1 + postsynaptic['SABVR'][thisState]
        postsynaptic['URYDR'][nextState] = 1 + postsynaptic['URYDR'][thisState]
        postsynaptic['URYVL'][nextState] = 1 + postsynaptic['URYVL'][thisState]
        postsynaptic['VA10'][nextState] = 5 + postsynaptic['VA10'][thisState]
        postsynaptic['VA11'][nextState] = 15 + postsynaptic['VA11'][thisState]
        postsynaptic['VA12'][nextState] = 1 + postsynaptic['VA12'][thisState]
        postsynaptic['VA2'][nextState] = 2 + postsynaptic['VA2'][thisState]
        postsynaptic['VA3'][nextState] = 7 + postsynaptic['VA3'][thisState]
        postsynaptic['VA4'][nextState] = 5 + postsynaptic['VA4'][thisState]
        postsynaptic['VA5'][nextState] = 4 + postsynaptic['VA5'][thisState]
        postsynaptic['VA6'][nextState] = 5 + postsynaptic['VA6'][thisState]
        postsynaptic['VA7'][nextState] = 4 + postsynaptic['VA7'][thisState]
        postsynaptic['VA8'][nextState] = 16 + postsynaptic['VA8'][thisState]
        postsynaptic['VB9'][nextState] = 10 + postsynaptic['VB9'][thisState]
        postsynaptic['VD13'][nextState] = 2 + postsynaptic['VD13'][thisState]

def AVBL():
        postsynaptic['AQR'][nextState] = 1 + postsynaptic['AQR'][thisState]
        postsynaptic['AS10'][nextState] = 1 + postsynaptic['AS10'][thisState]
        postsynaptic['AS3'][nextState] = 1 + postsynaptic['AS3'][thisState]
        postsynaptic['AS4'][nextState] = 1 + postsynaptic['AS4'][thisState]
        postsynaptic['AS5'][nextState] = 1 + postsynaptic['AS5'][thisState]
        postsynaptic['AS6'][nextState] = 1 + postsynaptic['AS6'][thisState]
        postsynaptic['AS7'][nextState] = 2 + postsynaptic['AS7'][thisState]
        postsynaptic['AS9'][nextState] = 1 + postsynaptic['AS9'][thisState]
        postsynaptic['AVAL'][nextState] = 7 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 7 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBR'][nextState] = 4 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 2 + postsynaptic['AVER'][thisState]
        postsynaptic['AVL'][nextState] = 1 + postsynaptic['AVL'][thisState]
        postsynaptic['DB3'][nextState] = 1 + postsynaptic['DB3'][thisState]
        postsynaptic['DB4'][nextState] = 1 + postsynaptic['DB4'][thisState]
        postsynaptic['DB5'][nextState] = 1 + postsynaptic['DB5'][thisState]
        postsynaptic['DB6'][nextState] = 2 + postsynaptic['DB6'][thisState]
        postsynaptic['DB7'][nextState] = 2 + postsynaptic['DB7'][thisState]
        postsynaptic['DVA'][nextState] = 1 + postsynaptic['DVA'][thisState]
        postsynaptic['PVNR'][nextState] = 1 + postsynaptic['PVNR'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RID'][nextState] = 1 + postsynaptic['RID'][thisState]
        postsynaptic['SDQR'][nextState] = 1 + postsynaptic['SDQR'][thisState]
        postsynaptic['SIBVL'][nextState] = 1 + postsynaptic['SIBVL'][thisState]
        postsynaptic['VA10'][nextState] = 1 + postsynaptic['VA10'][thisState]
        postsynaptic['VA2'][nextState] = 1 + postsynaptic['VA2'][thisState]
        postsynaptic['VA7'][nextState] = 1 + postsynaptic['VA7'][thisState]
        postsynaptic['VB1'][nextState] = 1 + postsynaptic['VB1'][thisState]
        postsynaptic['VB10'][nextState] = 2 + postsynaptic['VB10'][thisState]
        postsynaptic['VB11'][nextState] = 2 + postsynaptic['VB11'][thisState]
        postsynaptic['VB2'][nextState] = 4 + postsynaptic['VB2'][thisState]
        postsynaptic['VB4'][nextState] = 1 + postsynaptic['VB4'][thisState]
        postsynaptic['VB5'][nextState] = 1 + postsynaptic['VB5'][thisState]
        postsynaptic['VB6'][nextState] = 1 + postsynaptic['VB6'][thisState]
        postsynaptic['VB7'][nextState] = 2 + postsynaptic['VB7'][thisState]
        postsynaptic['VB8'][nextState] = 7 + postsynaptic['VB8'][thisState]
        postsynaptic['VB9'][nextState] = 1 + postsynaptic['VB9'][thisState]
        postsynaptic['VC3'][nextState] = 1 + postsynaptic['VC3'][thisState]

def AVBR():
        postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]
        postsynaptic['AS10'][nextState] = 1 + postsynaptic['AS10'][thisState]
        postsynaptic['AS3'][nextState] = 1 + postsynaptic['AS3'][thisState]
        postsynaptic['AS4'][nextState] = 1 + postsynaptic['AS4'][thisState]
        postsynaptic['AS5'][nextState] = 1 + postsynaptic['AS5'][thisState]
        postsynaptic['AS6'][nextState] = 2 + postsynaptic['AS6'][thisState]
        postsynaptic['AS7'][nextState] = 3 + postsynaptic['AS7'][thisState]
        postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 7 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 4 + postsynaptic['AVBL'][thisState]
        postsynaptic['DA5'][nextState] = 1 + postsynaptic['DA5'][thisState]
        postsynaptic['DB1'][nextState] = 3 + postsynaptic['DB1'][thisState]
        postsynaptic['DB2'][nextState] = 1 + postsynaptic['DB2'][thisState]
        postsynaptic['DB3'][nextState] = 1 + postsynaptic['DB3'][thisState]
        postsynaptic['DB4'][nextState] = 1 + postsynaptic['DB4'][thisState]
        postsynaptic['DB5'][nextState] = 1 + postsynaptic['DB5'][thisState]
        postsynaptic['DB6'][nextState] = 1 + postsynaptic['DB6'][thisState]
        postsynaptic['DB7'][nextState] = 1 + postsynaptic['DB7'][thisState]
        postsynaptic['DD1'][nextState] = 1 + postsynaptic['DD1'][thisState]
        postsynaptic['DVA'][nextState] = 1 + postsynaptic['DVA'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['PVNL'][nextState] = 2 + postsynaptic['PVNL'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RID'][nextState] = 2 + postsynaptic['RID'][thisState]
        postsynaptic['SIBVL'][nextState] = 1 + postsynaptic['SIBVL'][thisState]
        postsynaptic['VA4'][nextState] = 1 + postsynaptic['VA4'][thisState]
        postsynaptic['VA8'][nextState] = 1 + postsynaptic['VA8'][thisState]
        postsynaptic['VA9'][nextState] = 2 + postsynaptic['VA9'][thisState]
        postsynaptic['VB10'][nextState] = 1 + postsynaptic['VB10'][thisState]
        postsynaptic['VB11'][nextState] = 1 + postsynaptic['VB11'][thisState]
        postsynaptic['VB2'][nextState] = 1 + postsynaptic['VB2'][thisState]
        postsynaptic['VB3'][nextState] = 1 + postsynaptic['VB3'][thisState]
        postsynaptic['VB4'][nextState] = 1 + postsynaptic['VB4'][thisState]
        postsynaptic['VB6'][nextState] = 2 + postsynaptic['VB6'][thisState]
        postsynaptic['VB7'][nextState] = 2 + postsynaptic['VB7'][thisState]
        postsynaptic['VB8'][nextState] = 3 + postsynaptic['VB8'][thisState]
        postsynaptic['VB9'][nextState] = 6 + postsynaptic['VB9'][thisState]
        postsynaptic['VD10'][nextState] = 1 + postsynaptic['VD10'][thisState]
        postsynaptic['VD3'][nextState] = 1 + postsynaptic['VD3'][thisState]

def AVDL():
        postsynaptic['ADAR'][nextState] = 2 + postsynaptic['ADAR'][thisState]
        postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]
        postsynaptic['AS10'][nextState] = 1 + postsynaptic['AS10'][thisState]
        postsynaptic['AS11'][nextState] = 2 + postsynaptic['AS11'][thisState]
        postsynaptic['AS4'][nextState] = 1 + postsynaptic['AS4'][thisState]
        postsynaptic['AS5'][nextState] = 1 + postsynaptic['AS5'][thisState]
        postsynaptic['AVAL'][nextState] = 13 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 19 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVM'][nextState] = 2 + postsynaptic['AVM'][thisState]
        postsynaptic['DA1'][nextState] = 1 + postsynaptic['DA1'][thisState]
        postsynaptic['DA2'][nextState] = 1 + postsynaptic['DA2'][thisState]
        postsynaptic['DA3'][nextState] = 4 + postsynaptic['DA3'][thisState]
        postsynaptic['DA4'][nextState] = 1 + postsynaptic['DA4'][thisState]
        postsynaptic['DA5'][nextState] = 1 + postsynaptic['DA5'][thisState]
        postsynaptic['DA8'][nextState] = 1 + postsynaptic['DA8'][thisState]
        postsynaptic['FLPL'][nextState] = 1 + postsynaptic['FLPL'][thisState]
        postsynaptic['FLPR'][nextState] = 1 + postsynaptic['FLPR'][thisState]
        postsynaptic['LUAL'][nextState] = 1 + postsynaptic['LUAL'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['SABD'][nextState] = 1 + postsynaptic['SABD'][thisState]
        postsynaptic['SABVL'][nextState] = 1 + postsynaptic['SABVL'][thisState]
        postsynaptic['SABVR'][nextState] = 1 + postsynaptic['SABVR'][thisState]
        postsynaptic['VA5'][nextState] = 1 + postsynaptic['VA5'][thisState]

def AVDR():
        postsynaptic['ADAL'][nextState] = 2 + postsynaptic['ADAL'][thisState]
        postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]
        postsynaptic['AS10'][nextState] = 1 + postsynaptic['AS10'][thisState]
        postsynaptic['AS5'][nextState] = 1 + postsynaptic['AS5'][thisState]
        postsynaptic['AVAL'][nextState] = 16 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 15 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVDL'][nextState] = 2 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVJL'][nextState] = 2 + postsynaptic['AVJL'][thisState]
        postsynaptic['DA1'][nextState] = 2 + postsynaptic['DA1'][thisState]
        postsynaptic['DA2'][nextState] = 1 + postsynaptic['DA2'][thisState]
        postsynaptic['DA3'][nextState] = 1 + postsynaptic['DA3'][thisState]
        postsynaptic['DA4'][nextState] = 1 + postsynaptic['DA4'][thisState]
        postsynaptic['DA5'][nextState] = 2 + postsynaptic['DA5'][thisState]
        postsynaptic['DA8'][nextState] = 1 + postsynaptic['DA8'][thisState]
        postsynaptic['DA9'][nextState] = 1 + postsynaptic['DA9'][thisState]
        postsynaptic['DB4'][nextState] = 1 + postsynaptic['DB4'][thisState]
        postsynaptic['DVC'][nextState] = 1 + postsynaptic['DVC'][thisState]
        postsynaptic['FLPR'][nextState] = 1 + postsynaptic['FLPR'][thisState]
        postsynaptic['LUAL'][nextState] = 2 + postsynaptic['LUAL'][thisState]
        postsynaptic['PQR'][nextState] = 1 + postsynaptic['PQR'][thisState]
        postsynaptic['SABD'][nextState] = 1 + postsynaptic['SABD'][thisState]
        postsynaptic['SABVL'][nextState] = 3 + postsynaptic['SABVL'][thisState]
        postsynaptic['SABVR'][nextState] = 1 + postsynaptic['SABVR'][thisState]
        postsynaptic['VA11'][nextState] = 1 + postsynaptic['VA11'][thisState]
        postsynaptic['VA2'][nextState] = 1 + postsynaptic['VA2'][thisState]
        postsynaptic['VA3'][nextState] = 2 + postsynaptic['VA3'][thisState]
        postsynaptic['VA6'][nextState] = 1 + postsynaptic['VA6'][thisState]

def AVEL():
        postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]
        postsynaptic['AVAL'][nextState] = 12 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 7 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['DA1'][nextState] = 5 + postsynaptic['DA1'][thisState]
        postsynaptic['DA2'][nextState] = 1 + postsynaptic['DA2'][thisState]
        postsynaptic['DA3'][nextState] = 3 + postsynaptic['DA3'][thisState]
        postsynaptic['DA4'][nextState] = 1 + postsynaptic['DA4'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['RIML'][nextState] = 2 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 3 + postsynaptic['RIMR'][thisState]
        postsynaptic['RMDVR'][nextState] = 1 + postsynaptic['RMDVR'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]
        postsynaptic['SABD'][nextState] = 6 + postsynaptic['SABD'][thisState]
        postsynaptic['SABVL'][nextState] = 7 + postsynaptic['SABVL'][thisState]
        postsynaptic['SABVR'][nextState] = 3 + postsynaptic['SABVR'][thisState]
        postsynaptic['VA1'][nextState] = 5 + postsynaptic['VA1'][thisState]
        postsynaptic['VA3'][nextState] = 3 + postsynaptic['VA3'][thisState]
        postsynaptic['VD2'][nextState] = 1 + postsynaptic['VD2'][thisState]
        postsynaptic['VD3'][nextState] = 1 + postsynaptic['VD3'][thisState]

def AVER():
        postsynaptic['AS1'][nextState] = 3 + postsynaptic['AS1'][thisState]
        postsynaptic['AS2'][nextState] = 2 + postsynaptic['AS2'][thisState]
        postsynaptic['AS3'][nextState] = 1 + postsynaptic['AS3'][thisState]
        postsynaptic['AVAL'][nextState] = 7 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 16 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['DA1'][nextState] = 5 + postsynaptic['DA1'][thisState]
        postsynaptic['DA2'][nextState] = 3 + postsynaptic['DA2'][thisState]
        postsynaptic['DA3'][nextState] = 1 + postsynaptic['DA3'][thisState]
        postsynaptic['DB3'][nextState] = 1 + postsynaptic['DB3'][thisState]
        postsynaptic['RIML'][nextState] = 3 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 2 + postsynaptic['RIMR'][thisState]
        postsynaptic['RMDVL'][nextState] = 1 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMDVR'][nextState] = 1 + postsynaptic['RMDVR'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]
        postsynaptic['SABD'][nextState] = 2 + postsynaptic['SABD'][thisState]
        postsynaptic['SABVL'][nextState] = 3 + postsynaptic['SABVL'][thisState]
        postsynaptic['SABVR'][nextState] = 3 + postsynaptic['SABVR'][thisState]
        postsynaptic['VA1'][nextState] = 1 + postsynaptic['VA1'][thisState]
        postsynaptic['VA2'][nextState] = 1 + postsynaptic['VA2'][thisState]
        postsynaptic['VA3'][nextState] = 2 + postsynaptic['VA3'][thisState]
        postsynaptic['VA4'][nextState] = 1 + postsynaptic['VA4'][thisState]
        postsynaptic['VA5'][nextState] = 1 + postsynaptic['VA5'][thisState]

def AVFL():
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVFR'][nextState] = 30 + postsynaptic['AVFR'][thisState]
        postsynaptic['AVG'][nextState] = 1 + postsynaptic['AVG'][thisState]
        postsynaptic['AVHL'][nextState] = 4 + postsynaptic['AVHL'][thisState]
        postsynaptic['AVHR'][nextState] = 7 + postsynaptic['AVHR'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVJR'][nextState] = 1 + postsynaptic['AVJR'][thisState]
        postsynaptic['AVL'][nextState] = 1 + postsynaptic['AVL'][thisState]
        postsynaptic['HSNL'][nextState] = 1 + postsynaptic['HSNL'][thisState]
        postsynaptic['MVL11'][nextState] = 1 + postsynaptic['MVL11'][thisState]
        postsynaptic['MVL12'][nextState] = 1 + postsynaptic['MVL12'][thisState]
        postsynaptic['PDER'][nextState] = 1 + postsynaptic['PDER'][thisState]
        postsynaptic['PVNL'][nextState] = 2 + postsynaptic['PVNL'][thisState]
        postsynaptic['PVQL'][nextState] = 1 + postsynaptic['PVQL'][thisState]
        postsynaptic['PVQR'][nextState] = 2 + postsynaptic['PVQR'][thisState]
        postsynaptic['VB1'][nextState] = 1 + postsynaptic['VB1'][thisState]

def AVFR():
        postsynaptic['ASJL'][nextState] = 1 + postsynaptic['ASJL'][thisState]
        postsynaptic['ASKL'][nextState] = 1 + postsynaptic['ASKL'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 5 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVFL'][nextState] = 24 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVHL'][nextState] = 4 + postsynaptic['AVHL'][thisState]
        postsynaptic['AVHR'][nextState] = 2 + postsynaptic['AVHR'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVJR'][nextState] = 1 + postsynaptic['AVJR'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['MVL14'][nextState] = 2 + postsynaptic['MVL14'][thisState]
        postsynaptic['MVR14'][nextState] = 2 + postsynaptic['MVR14'][thisState]
        postsynaptic['PVQL'][nextState] = 1 + postsynaptic['PVQL'][thisState]
        postsynaptic['VC4'][nextState] = 1 + postsynaptic['VC4'][thisState]
        postsynaptic['VD11'][nextState] = 1 + postsynaptic['VD11'][thisState]

def AVG():
        postsynaptic['AVAR'][nextState] = 3 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['AVFL'][nextState] = 1 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVL'][nextState] = 1 + postsynaptic['AVL'][thisState]
        postsynaptic['DA8'][nextState] = 1 + postsynaptic['DA8'][thisState]
        postsynaptic['PHAL'][nextState] = 2 + postsynaptic['PHAL'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVNR'][nextState] = 1 + postsynaptic['PVNR'][thisState]
        postsynaptic['PVPR'][nextState] = 1 + postsynaptic['PVPR'][thisState]
        postsynaptic['PVQR'][nextState] = 1 + postsynaptic['PVQR'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['RIFL'][nextState] = 1 + postsynaptic['RIFL'][thisState]
        postsynaptic['RIFR'][nextState] = 1 + postsynaptic['RIFR'][thisState]
        postsynaptic['VA11'][nextState] = 1 + postsynaptic['VA11'][thisState]

def AVHL():
        postsynaptic['ADFR'][nextState] = 3 + postsynaptic['ADFR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVFL'][nextState] = 1 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVFL'][nextState] = 2 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVFR'][nextState] = 5 + postsynaptic['AVFR'][thisState]
        postsynaptic['AVHR'][nextState] = 2 + postsynaptic['AVHR'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AWBR'][nextState] = 1 + postsynaptic['AWBR'][thisState]
        postsynaptic['PHBR'][nextState] = 1 + postsynaptic['PHBR'][thisState]
        postsynaptic['PVPR'][nextState] = 2 + postsynaptic['PVPR'][thisState]
        postsynaptic['PVQL'][nextState] = 1 + postsynaptic['PVQL'][thisState]
        postsynaptic['PVQR'][nextState] = 2 + postsynaptic['PVQR'][thisState]
        postsynaptic['RIMR'][nextState] = 1 + postsynaptic['RIMR'][thisState]
        postsynaptic['RIR'][nextState] = 3 + postsynaptic['RIR'][thisState]
        postsynaptic['SMBDR'][nextState] = 1 + postsynaptic['SMBDR'][thisState]
        postsynaptic['SMBVR'][nextState] = 1 + postsynaptic['SMBVR'][thisState]
        postsynaptic['VD1'][nextState] = 1 + postsynaptic['VD1'][thisState]

def AVHR():
        postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]
        postsynaptic['ADLR'][nextState] = 2 + postsynaptic['ADLR'][thisState]
        postsynaptic['AQR'][nextState] = 2 + postsynaptic['AQR'][thisState]
        postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVFL'][nextState] = 1 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVFR'][nextState] = 2 + postsynaptic['AVFR'][thisState]
        postsynaptic['AVHL'][nextState] = 2 + postsynaptic['AVHL'][thisState]
        postsynaptic['AVJR'][nextState] = 4 + postsynaptic['AVJR'][thisState]
        postsynaptic['PVNL'][nextState] = 1 + postsynaptic['PVNL'][thisState]
        postsynaptic['PVPL'][nextState] = 3 + postsynaptic['PVPL'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIR'][nextState] = 4 + postsynaptic['RIR'][thisState]
        postsynaptic['SMBDL'][nextState] = 1 + postsynaptic['SMBDL'][thisState]
        postsynaptic['SMBVL'][nextState] = 1 + postsynaptic['SMBVL'][thisState]

def AVJL():
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 4 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVFR'][nextState] = 1 + postsynaptic['AVFR'][thisState]
        postsynaptic['AVHL'][nextState] = 2 + postsynaptic['AVHL'][thisState]
        postsynaptic['AVJR'][nextState] = 4 + postsynaptic['AVJR'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['PLMR'][nextState] = 2 + postsynaptic['PLMR'][thisState]
        postsynaptic['PVCL'][nextState] = 2 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 5 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVNR'][nextState] = 1 + postsynaptic['PVNR'][thisState]
        postsynaptic['RIFR'][nextState] = 1 + postsynaptic['RIFR'][thisState]
        postsynaptic['RIS'][nextState] = 2 + postsynaptic['RIS'][thisState]

def AVJR():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 3 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 3 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVER'][nextState] = 3 + postsynaptic['AVER'][thisState]
        postsynaptic['AVJL'][nextState] = 5 + postsynaptic['AVJL'][thisState]
        postsynaptic['PVCL'][nextState] = 3 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 4 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVQR'][nextState] = 1 + postsynaptic['PVQR'][thisState]
        postsynaptic['SABVL'][nextState] = 1 + postsynaptic['SABVL'][thisState]

def AVKL():
        postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
        postsynaptic['AQR'][nextState] = 2 + postsynaptic['AQR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVEL'][nextState] = 2 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['AVKR'][nextState] = 2 + postsynaptic['AVKR'][thisState]
        postsynaptic['AVM'][nextState] = 1 + postsynaptic['AVM'][thisState]
        postsynaptic['DVA'][nextState] = 1 + postsynaptic['DVA'][thisState]
        postsynaptic['PDEL'][nextState] = 3 + postsynaptic['PDEL'][thisState]
        postsynaptic['PDER'][nextState] = 1 + postsynaptic['PDER'][thisState]
        postsynaptic['PVM'][nextState] = 1 + postsynaptic['PVM'][thisState]
        postsynaptic['PVPL'][nextState] = 1 + postsynaptic['PVPL'][thisState]
        postsynaptic['PVPR'][nextState] = 1 + postsynaptic['PVPR'][thisState]
        postsynaptic['PVT'][nextState] = 2 + postsynaptic['PVT'][thisState]
        postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
        postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIML'][nextState] = 2 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 1 + postsynaptic['RIMR'][thisState]
        postsynaptic['RMFR'][nextState] = 1 + postsynaptic['RMFR'][thisState]
        postsynaptic['SAADR'][nextState] = 1 + postsynaptic['SAADR'][thisState]
        postsynaptic['SIAVR'][nextState] = 1 + postsynaptic['SIAVR'][thisState]
        postsynaptic['SMBDL'][nextState] = 1 + postsynaptic['SMBDL'][thisState]
        postsynaptic['SMBDR'][nextState] = 1 + postsynaptic['SMBDR'][thisState]
        postsynaptic['SMBVR'][nextState] = 1 + postsynaptic['SMBVR'][thisState]
        postsynaptic['SMDDR'][nextState] = 1 + postsynaptic['SMDDR'][thisState]
        postsynaptic['VB1'][nextState] = 4 + postsynaptic['VB1'][thisState]
        postsynaptic['VB10'][nextState] = 1 + postsynaptic['VB10'][thisState]

def AVKR():
        postsynaptic['ADEL'][nextState] = 1 + postsynaptic['ADEL'][thisState]
        postsynaptic['AQR'][nextState] = 1 + postsynaptic['AQR'][thisState]
        postsynaptic['AVKL'][nextState] = 2 + postsynaptic['AVKL'][thisState]
        postsynaptic['BDUL'][nextState] = 1 + postsynaptic['BDUL'][thisState]
        postsynaptic['MVL10'][nextState] = 1 + postsynaptic['MVL10'][thisState]
        postsynaptic['PVPL'][nextState] = 6 + postsynaptic['PVPL'][thisState]
        postsynaptic['PVQL'][nextState] = 1 + postsynaptic['PVQL'][thisState]
        postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIML'][nextState] = 2 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 2 + postsynaptic['RIMR'][thisState]
        postsynaptic['RMDR'][nextState] = 1 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMFL'][nextState] = 1 + postsynaptic['RMFL'][thisState]
        postsynaptic['SAADL'][nextState] = 1 + postsynaptic['SAADL'][thisState]
        postsynaptic['SMBDL'][nextState] = 2 + postsynaptic['SMBDL'][thisState]
        postsynaptic['SMBDR'][nextState] = 2 + postsynaptic['SMBDR'][thisState]
        postsynaptic['SMBVR'][nextState] = 1 + postsynaptic['SMBVR'][thisState]
        postsynaptic['SMDDL'][nextState] = 1 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDDR'][nextState] = 2 + postsynaptic['SMDDR'][thisState]

def AVL():
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVFR'][nextState] = 1 + postsynaptic['AVFR'][thisState]
        postsynaptic['DA2'][nextState] = 1 + postsynaptic['DA2'][thisState]
        postsynaptic['DD1'][nextState] = 1 + postsynaptic['DD1'][thisState]
        postsynaptic['DD6'][nextState] = 2 + postsynaptic['DD6'][thisState]
        postsynaptic['DVB'][nextState] = 1 + postsynaptic['DVB'][thisState]
        postsynaptic['DVC'][nextState] = 9 + postsynaptic['DVC'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['MVL10'][nextState] = -5 + postsynaptic['MVL10'][thisState]
        postsynaptic['MVR10'][nextState] = -5 + postsynaptic['MVR10'][thisState]
        postsynaptic['PVM'][nextState] = 1 + postsynaptic['PVM'][thisState]
        postsynaptic['PVPR'][nextState] = 1 + postsynaptic['PVPR'][thisState]
        postsynaptic['PVWL'][nextState] = 1 + postsynaptic['PVWL'][thisState]
        postsynaptic['SABD'][nextState] = 5 + postsynaptic['SABD'][thisState]
        postsynaptic['SABVL'][nextState] = 4 + postsynaptic['SABVL'][thisState]
        postsynaptic['SABVR'][nextState] = 3 + postsynaptic['SABVR'][thisState]
        postsynaptic['VD12'][nextState] = 4 + postsynaptic['VD12'][thisState]

def AVM():
        postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
        postsynaptic['ALML'][nextState] = 1 + postsynaptic['ALML'][thisState]
        postsynaptic['ALMR'][nextState] = 1 + postsynaptic['ALMR'][thisState]
        postsynaptic['AVBL'][nextState] = 6 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 6 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 2 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVJR'][nextState] = 1 + postsynaptic['AVJR'][thisState]
        postsynaptic['BDUL'][nextState] = 3 + postsynaptic['BDUL'][thisState]
        postsynaptic['BDUR'][nextState] = 2 + postsynaptic['BDUR'][thisState]
        postsynaptic['DA1'][nextState] = 1 + postsynaptic['DA1'][thisState]
        postsynaptic['PVCL'][nextState] = 4 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 5 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVNL'][nextState] = 1 + postsynaptic['PVNL'][thisState]
        postsynaptic['PVR'][nextState] = 3 + postsynaptic['PVR'][thisState]
        postsynaptic['RID'][nextState] = 1 + postsynaptic['RID'][thisState]
        postsynaptic['SIBVL'][nextState] = 1 + postsynaptic['SIBVL'][thisState]
        postsynaptic['VA1'][nextState] = 2 + postsynaptic['VA1'][thisState]

def AWAL():
        postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
        postsynaptic['AFDL'][nextState] = 5 + postsynaptic['AFDL'][thisState]
        postsynaptic['AIAL'][nextState] = 1 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIYL'][nextState] = 1 + postsynaptic['AIYL'][thisState]
        postsynaptic['AIZL'][nextState] = 10 + postsynaptic['AIZL'][thisState]
        postsynaptic['ASEL'][nextState] = 4 + postsynaptic['ASEL'][thisState]
        postsynaptic['ASGL'][nextState] = 1 + postsynaptic['ASGL'][thisState]
        postsynaptic['AWAR'][nextState] = 1 + postsynaptic['AWAR'][thisState]
        postsynaptic['AWBL'][nextState] = 1 + postsynaptic['AWBL'][thisState]

def AWAR():
        postsynaptic['ADFR'][nextState] = 3 + postsynaptic['ADFR'][thisState]
        postsynaptic['AFDR'][nextState] = 7 + postsynaptic['AFDR'][thisState]
        postsynaptic['AIAR'][nextState] = 1 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIYR'][nextState] = 2 + postsynaptic['AIYR'][thisState]
        postsynaptic['AIZR'][nextState] = 7 + postsynaptic['AIZR'][thisState]
        postsynaptic['AIZR'][nextState] = 1 + postsynaptic['AIZR'][thisState]
        postsynaptic['ASEL'][nextState] = 1 + postsynaptic['ASEL'][thisState]
        postsynaptic['ASER'][nextState] = 2 + postsynaptic['ASER'][thisState]
        postsynaptic['AUAR'][nextState] = 1 + postsynaptic['AUAR'][thisState]
        postsynaptic['AWAL'][nextState] = 1 + postsynaptic['AWAL'][thisState]
        postsynaptic['AWBR'][nextState] = 1 + postsynaptic['AWBR'][thisState]
        postsynaptic['RIFR'][nextState] = 2 + postsynaptic['RIFR'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIR'][nextState] = 2 + postsynaptic['RIR'][thisState]

def AWBL():
        postsynaptic['ADFL'][nextState] = 9 + postsynaptic['ADFL'][thisState]
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIZL'][nextState] = 9 + postsynaptic['AIZL'][thisState]
        postsynaptic['AUAL'][nextState] = 1 + postsynaptic['AUAL'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AWBR'][nextState] = 1 + postsynaptic['AWBR'][thisState]
        postsynaptic['RIAL'][nextState] = 3 + postsynaptic['RIAL'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]
        postsynaptic['SMBDL'][nextState] = 1 + postsynaptic['SMBDL'][thisState]

def AWBR():
        postsynaptic['ADFR'][nextState] = 4 + postsynaptic['ADFR'][thisState]
        postsynaptic['AIZR'][nextState] = 4 + postsynaptic['AIZR'][thisState]
        postsynaptic['ASGR'][nextState] = 1 + postsynaptic['ASGR'][thisState]
        postsynaptic['ASHR'][nextState] = 2 + postsynaptic['ASHR'][thisState]
        postsynaptic['AUAR'][nextState] = 1 + postsynaptic['AUAR'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['AWBL'][nextState] = 1 + postsynaptic['AWBL'][thisState]
        postsynaptic['RIAR'][nextState] = 1 + postsynaptic['RIAR'][thisState]
        postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
        postsynaptic['RIR'][nextState] = 2 + postsynaptic['RIR'][thisState]
        postsynaptic['RMGR'][nextState] = 1 + postsynaptic['RMGR'][thisState]
        postsynaptic['SMBVR'][nextState] = 1 + postsynaptic['SMBVR'][thisState]

def AWCL():
        postsynaptic['AIAL'][nextState] = 2 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIAR'][nextState] = 4 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIYL'][nextState] = 10 + postsynaptic['AIYL'][thisState]
        postsynaptic['ASEL'][nextState] = 1 + postsynaptic['ASEL'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AWCR'][nextState] = 1 + postsynaptic['AWCR'][thisState]
        postsynaptic['RIAL'][nextState] = 3 + postsynaptic['RIAL'][thisState]

def AWCR():
        postsynaptic['AIAR'][nextState] = 1 + postsynaptic['AIAR'][thisState]
        postsynaptic['AIBR'][nextState] = 4 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIYL'][nextState] = 4 + postsynaptic['AIYL'][thisState]
        postsynaptic['AIYR'][nextState] = 9 + postsynaptic['AIYR'][thisState]
        postsynaptic['ASEL'][nextState] = 1 + postsynaptic['ASEL'][thisState]
        postsynaptic['ASGR'][nextState] = 1 + postsynaptic['ASGR'][thisState]
        postsynaptic['AWCL'][nextState] = 5 + postsynaptic['AWCL'][thisState]

def BAGL():
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 4 + postsynaptic['AVER'][thisState]
        postsynaptic['BAGR'][nextState] = 2 + postsynaptic['BAGR'][thisState]
        postsynaptic['RIAR'][nextState] = 5 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 7 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIGR'][nextState] = 4 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIR'][nextState] = 1 + postsynaptic['RIR'][thisState]

def BAGR():
        postsynaptic['AIYL'][nextState] = 1 + postsynaptic['AIYL'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVEL'][nextState] = 2 + postsynaptic['AVEL'][thisState]
        postsynaptic['BAGL'][nextState] = 1 + postsynaptic['BAGL'][thisState]
        postsynaptic['RIAL'][nextState] = 5 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIBL'][nextState] = 4 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIGL'][nextState] = 5 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIR'][nextState] = 1 + postsynaptic['RIR'][thisState]

def BDUL():
        postsynaptic['ADEL'][nextState] = 3 + postsynaptic['ADEL'][thisState]
        postsynaptic['AVHL'][nextState] = 1 + postsynaptic['AVHL'][thisState]
        postsynaptic['AVJR'][nextState] = 1 + postsynaptic['AVJR'][thisState]
        postsynaptic['HSNL'][nextState] = 1 + postsynaptic['HSNL'][thisState]
        postsynaptic['PVNL'][nextState] = 2 + postsynaptic['PVNL'][thisState]
        postsynaptic['PVNR'][nextState] = 2 + postsynaptic['PVNR'][thisState]
        postsynaptic['SAADL'][nextState] = 1 + postsynaptic['SAADL'][thisState]
        postsynaptic['URADL'][nextState] = 1 + postsynaptic['URADL'][thisState]

def BDUR():
        postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
        postsynaptic['ALMR'][nextState] = 1 + postsynaptic['ALMR'][thisState]
        postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVHL'][nextState] = 1 + postsynaptic['AVHL'][thisState]
        postsynaptic['AVJL'][nextState] = 2 + postsynaptic['AVJL'][thisState]
        postsynaptic['HSNR'][nextState] = 4 + postsynaptic['HSNR'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVNL'][nextState] = 2 + postsynaptic['PVNL'][thisState]
        postsynaptic['PVNR'][nextState] = 1 + postsynaptic['PVNR'][thisState]
        postsynaptic['SDQL'][nextState] = 1 + postsynaptic['SDQL'][thisState]
        postsynaptic['URADR'][nextState] = 1 + postsynaptic['URADR'][thisState]

def CEPDL():
        postsynaptic['AVER'][nextState] = 5 + postsynaptic['AVER'][thisState]
        postsynaptic['IL1DL'][nextState] = 4 + postsynaptic['IL1DL'][thisState]
        postsynaptic['OLLL'][nextState] = 2 + postsynaptic['OLLL'][thisState]
        postsynaptic['OLQDL'][nextState] = 6 + postsynaptic['OLQDL'][thisState]
        postsynaptic['OLQDL'][nextState] = 1 + postsynaptic['OLQDL'][thisState]
        postsynaptic['RIBL'][nextState] = 2 + postsynaptic['RIBL'][thisState]
        postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
        postsynaptic['RICR'][nextState] = 2 + postsynaptic['RICR'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]
        postsynaptic['RIPL'][nextState] = 2 + postsynaptic['RIPL'][thisState]
        postsynaptic['RIS'][nextState] = 1 + postsynaptic['RIS'][thisState]
        postsynaptic['RMDVL'][nextState] = 3 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMGL'][nextState] = 4 + postsynaptic['RMGL'][thisState]
        postsynaptic['RMHR'][nextState] = 4 + postsynaptic['RMHR'][thisState]
        postsynaptic['SIADR'][nextState] = 1 + postsynaptic['SIADR'][thisState]
        postsynaptic['SMBDR'][nextState] = 1 + postsynaptic['SMBDR'][thisState]
        postsynaptic['URADL'][nextState] = 2 + postsynaptic['URADL'][thisState]
        postsynaptic['URBL'][nextState] = 4 + postsynaptic['URBL'][thisState]
        postsynaptic['URYDL'][nextState] = 2 + postsynaptic['URYDL'][thisState]

def CEPDR():
        postsynaptic['AVEL'][nextState] = 6 + postsynaptic['AVEL'][thisState]
        postsynaptic['BDUR'][nextState] = 1 + postsynaptic['BDUR'][thisState]
        postsynaptic['IL1DR'][nextState] = 5 + postsynaptic['IL1DR'][thisState]
        postsynaptic['IL1R'][nextState] = 1 + postsynaptic['IL1R'][thisState]
        postsynaptic['OLLR'][nextState] = 8 + postsynaptic['OLLR'][thisState]
        postsynaptic['OLQDR'][nextState] = 5 + postsynaptic['OLQDR'][thisState]
        postsynaptic['OLQDR'][nextState] = 2 + postsynaptic['OLQDR'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RICL'][nextState] = 4 + postsynaptic['RICL'][thisState]
        postsynaptic['RICR'][nextState] = 3 + postsynaptic['RICR'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]
        postsynaptic['RIS'][nextState] = 1 + postsynaptic['RIS'][thisState]
        postsynaptic['RMDDL'][nextState] = 1 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDVR'][nextState] = 2 + postsynaptic['RMDVR'][thisState]
        postsynaptic['RMGR'][nextState] = 1 + postsynaptic['RMGR'][thisState]
        postsynaptic['RMHL'][nextState] = 4 + postsynaptic['RMHL'][thisState]
        postsynaptic['RMHR'][nextState] = 1 + postsynaptic['RMHR'][thisState]
        postsynaptic['SIADL'][nextState] = 1 + postsynaptic['SIADL'][thisState]
        postsynaptic['SMBDR'][nextState] = 1 + postsynaptic['SMBDR'][thisState]
        postsynaptic['URADR'][nextState] = 1 + postsynaptic['URADR'][thisState]
        postsynaptic['URBR'][nextState] = 2 + postsynaptic['URBR'][thisState]
        postsynaptic['URYDR'][nextState] = 1 + postsynaptic['URYDR'][thisState]

def CEPVL():
        postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]
        postsynaptic['AVER'][nextState] = 3 + postsynaptic['AVER'][thisState]
        postsynaptic['IL1VL'][nextState] = 2 + postsynaptic['IL1VL'][thisState]
        postsynaptic['MVL03'][nextState] = 1 + postsynaptic['MVL03'][thisState]
        postsynaptic['OLLL'][nextState] = 4 + postsynaptic['OLLL'][thisState]
        postsynaptic['OLQVL'][nextState] = 6 + postsynaptic['OLQVL'][thisState]
        postsynaptic['OLQVL'][nextState] = 1 + postsynaptic['OLQVL'][thisState]
        postsynaptic['RICL'][nextState] = 7 + postsynaptic['RICL'][thisState]
        postsynaptic['RICR'][nextState] = 4 + postsynaptic['RICR'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]
        postsynaptic['RIPL'][nextState] = 1 + postsynaptic['RIPL'][thisState]
        postsynaptic['RMDDL'][nextState] = 4 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMHL'][nextState] = 1 + postsynaptic['RMHL'][thisState]
        postsynaptic['SIAVL'][nextState] = 1 + postsynaptic['SIAVL'][thisState]
        postsynaptic['URAVL'][nextState] = 2 + postsynaptic['URAVL'][thisState]

def CEPVR():
        postsynaptic['ASGR'][nextState] = 1 + postsynaptic['ASGR'][thisState]
        postsynaptic['AVEL'][nextState] = 5 + postsynaptic['AVEL'][thisState]
        postsynaptic['IL1VR'][nextState] = 1 + postsynaptic['IL1VR'][thisState]
        postsynaptic['IL2VR'][nextState] = 2 + postsynaptic['IL2VR'][thisState]
        postsynaptic['MVR04'][nextState] = 1 + postsynaptic['MVR04'][thisState]
        postsynaptic['OLLR'][nextState] = 7 + postsynaptic['OLLR'][thisState]
        postsynaptic['OLQVR'][nextState] = 3 + postsynaptic['OLQVR'][thisState]
        postsynaptic['OLQVR'][nextState] = 1 + postsynaptic['OLQVR'][thisState]
        postsynaptic['RICL'][nextState] = 2 + postsynaptic['RICL'][thisState]
        postsynaptic['RICR'][nextState] = 2 + postsynaptic['RICR'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]
        postsynaptic['RIPR'][nextState] = 1 + postsynaptic['RIPR'][thisState]
        postsynaptic['RIVL'][nextState] = 1 + postsynaptic['RIVL'][thisState]
        postsynaptic['RMDDR'][nextState] = 2 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMHR'][nextState] = 2 + postsynaptic['RMHR'][thisState]
        postsynaptic['SIAVR'][nextState] = 2 + postsynaptic['SIAVR'][thisState]
        postsynaptic['URAVR'][nextState] = 1 + postsynaptic['URAVR'][thisState]

def DA1():
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 6 + postsynaptic['AVAR'][thisState]
        postsynaptic['DA4'][nextState] = 1 + postsynaptic['DA4'][thisState]
        postsynaptic['DD1'][nextState] = 4 + postsynaptic['DD1'][thisState]
        postsynaptic['MDL08'][nextState] = 8 + postsynaptic['MDL08'][thisState]
        postsynaptic['MDR08'][nextState] = 8 + postsynaptic['MDR08'][thisState]
        postsynaptic['SABVL'][nextState] = 2 + postsynaptic['SABVL'][thisState]
        postsynaptic['SABVR'][nextState] = 3 + postsynaptic['SABVR'][thisState]
        postsynaptic['VD1'][nextState] = 17 + postsynaptic['VD1'][thisState]
        postsynaptic['VD2'][nextState] = 1 + postsynaptic['VD2'][thisState]

def DA2():
        postsynaptic['AS2'][nextState] = 2 + postsynaptic['AS2'][thisState]
        postsynaptic['AS3'][nextState] = 1 + postsynaptic['AS3'][thisState]
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['DD1'][nextState] = 1 + postsynaptic['DD1'][thisState]
        postsynaptic['MDL07'][nextState] = 2 + postsynaptic['MDL07'][thisState]
        postsynaptic['MDL08'][nextState] = 1 + postsynaptic['MDL08'][thisState]
        postsynaptic['MDL09'][nextState] = 2 + postsynaptic['MDL09'][thisState]
        postsynaptic['MDL10'][nextState] = 2 + postsynaptic['MDL10'][thisState]
        postsynaptic['MDR07'][nextState] = 2 + postsynaptic['MDR07'][thisState]
        postsynaptic['MDR08'][nextState] = 2 + postsynaptic['MDR08'][thisState]
        postsynaptic['MDR09'][nextState] = 2 + postsynaptic['MDR09'][thisState]
        postsynaptic['MDR10'][nextState] = 2 + postsynaptic['MDR10'][thisState]
        postsynaptic['SABVL'][nextState] = 1 + postsynaptic['SABVL'][thisState]
        postsynaptic['VA1'][nextState] = 2 + postsynaptic['VA1'][thisState]
        postsynaptic['VD1'][nextState] = 2 + postsynaptic['VD1'][thisState]
        postsynaptic['VD2'][nextState] = 11 + postsynaptic['VD2'][thisState]
        postsynaptic['VD3'][nextState] = 5 + postsynaptic['VD3'][thisState]

def DA3():
        postsynaptic['AS4'][nextState] = 2 + postsynaptic['AS4'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['DA4'][nextState] = 2 + postsynaptic['DA4'][thisState]
        postsynaptic['DB3'][nextState] = 1 + postsynaptic['DB3'][thisState]
        postsynaptic['DD2'][nextState] = 1 + postsynaptic['DD2'][thisState]
        postsynaptic['MDL09'][nextState] = 5 + postsynaptic['MDL09'][thisState]
        postsynaptic['MDL10'][nextState] = 5 + postsynaptic['MDL10'][thisState]
        postsynaptic['MDL12'][nextState] = 5 + postsynaptic['MDL12'][thisState]
        postsynaptic['MDR09'][nextState] = 5 + postsynaptic['MDR09'][thisState]
        postsynaptic['MDR10'][nextState] = 5 + postsynaptic['MDR10'][thisState]
        postsynaptic['MDR12'][nextState] = 5 + postsynaptic['MDR12'][thisState]
        postsynaptic['VD3'][nextState] = 25 + postsynaptic['VD3'][thisState]
        postsynaptic['VD4'][nextState] = 6 + postsynaptic['VD4'][thisState]

def DA4():
        postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['DA1'][nextState] = 1 + postsynaptic['DA1'][thisState]
        postsynaptic['DA3'][nextState] = 1 + postsynaptic['DA3'][thisState]
        postsynaptic['DB3'][nextState] = 2 + postsynaptic['DB3'][thisState]
        postsynaptic['DD2'][nextState] = 1 + postsynaptic['DD2'][thisState]
        postsynaptic['MDL11'][nextState] = 4 + postsynaptic['MDL11'][thisState]
        postsynaptic['MDL12'][nextState] = 4 + postsynaptic['MDL12'][thisState]
        postsynaptic['MDL14'][nextState] = 5 + postsynaptic['MDL14'][thisState]
        postsynaptic['MDR11'][nextState] = 4 + postsynaptic['MDR11'][thisState]
        postsynaptic['MDR12'][nextState] = 4 + postsynaptic['MDR12'][thisState]
        postsynaptic['MDR14'][nextState] = 5 + postsynaptic['MDR14'][thisState]
        postsynaptic['VB6'][nextState] = 1 + postsynaptic['VB6'][thisState]
        postsynaptic['VD4'][nextState] = 12 + postsynaptic['VD4'][thisState]
        postsynaptic['VD5'][nextState] = 15 + postsynaptic['VD5'][thisState]

def DA5():
        postsynaptic['AS6'][nextState] = 2 + postsynaptic['AS6'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 5 + postsynaptic['AVAR'][thisState]
        postsynaptic['DB4'][nextState] = 1 + postsynaptic['DB4'][thisState]
        postsynaptic['MDL13'][nextState] = 5 + postsynaptic['MDL13'][thisState]
        postsynaptic['MDL14'][nextState] = 4 + postsynaptic['MDL14'][thisState]
        postsynaptic['MDR13'][nextState] = 5 + postsynaptic['MDR13'][thisState]
        postsynaptic['MDR14'][nextState] = 4 + postsynaptic['MDR14'][thisState]
        postsynaptic['VA4'][nextState] = 1 + postsynaptic['VA4'][thisState]
        postsynaptic['VA5'][nextState] = 2 + postsynaptic['VA5'][thisState]
        postsynaptic['VD5'][nextState] = 1 + postsynaptic['VD5'][thisState]
        postsynaptic['VD6'][nextState] = 16 + postsynaptic['VD6'][thisState]

def DA6():
        postsynaptic['AVAL'][nextState] = 10 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['MDL11'][nextState] = 6 + postsynaptic['MDL11'][thisState]
        postsynaptic['MDL12'][nextState] = 4 + postsynaptic['MDL12'][thisState]
        postsynaptic['MDL13'][nextState] = 4 + postsynaptic['MDL13'][thisState]
        postsynaptic['MDL14'][nextState] = 4 + postsynaptic['MDL14'][thisState]
        postsynaptic['MDL16'][nextState] = 4 + postsynaptic['MDL16'][thisState]
        postsynaptic['MDR11'][nextState] = 4 + postsynaptic['MDR11'][thisState]
        postsynaptic['MDR12'][nextState] = 4 + postsynaptic['MDR12'][thisState]
        postsynaptic['MDR13'][nextState] = 4 + postsynaptic['MDR13'][thisState]
        postsynaptic['MDR14'][nextState] = 4 + postsynaptic['MDR14'][thisState]
        postsynaptic['MDR16'][nextState] = 4 + postsynaptic['MDR16'][thisState]
        postsynaptic['VD4'][nextState] = 4 + postsynaptic['VD4'][thisState]
        postsynaptic['VD5'][nextState] = 3 + postsynaptic['VD5'][thisState]
        postsynaptic['VD6'][nextState] = 3 + postsynaptic['VD6'][thisState]

def DA7():
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['MDL15'][nextState] = 4 + postsynaptic['MDL15'][thisState]
        postsynaptic['MDL17'][nextState] = 4 + postsynaptic['MDL17'][thisState]
        postsynaptic['MDL18'][nextState] = 4 + postsynaptic['MDL18'][thisState]
        postsynaptic['MDR15'][nextState] = 4 + postsynaptic['MDR15'][thisState]
        postsynaptic['MDR17'][nextState] = 4 + postsynaptic['MDR17'][thisState]
        postsynaptic['MDR18'][nextState] = 4 + postsynaptic['MDR18'][thisState]

def DA8():
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['DA9'][nextState] = 1 + postsynaptic['DA9'][thisState]
        postsynaptic['MDL17'][nextState] = 4 + postsynaptic['MDL17'][thisState]
        postsynaptic['MDL19'][nextState] = 4 + postsynaptic['MDL19'][thisState]
        postsynaptic['MDL20'][nextState] = 4 + postsynaptic['MDL20'][thisState]
        postsynaptic['MDR17'][nextState] = 4 + postsynaptic['MDR17'][thisState]
        postsynaptic['MDR19'][nextState] = 4 + postsynaptic['MDR19'][thisState]
        postsynaptic['MDR20'][nextState] = 4 + postsynaptic['MDR20'][thisState]

def DA9():
        postsynaptic['DA8'][nextState] = 1 + postsynaptic['DA8'][thisState]
        postsynaptic['DD6'][nextState] = 1 + postsynaptic['DD6'][thisState]
        postsynaptic['MDL19'][nextState] = 4 + postsynaptic['MDL19'][thisState]
        postsynaptic['MDL21'][nextState] = 4 + postsynaptic['MDL21'][thisState]
        postsynaptic['MDL22'][nextState] = 4 + postsynaptic['MDL22'][thisState]
        postsynaptic['MDL23'][nextState] = 4 + postsynaptic['MDL23'][thisState]
        postsynaptic['MDL24'][nextState] = 4 + postsynaptic['MDL24'][thisState]
        postsynaptic['MDR19'][nextState] = 4 + postsynaptic['MDR19'][thisState]
        postsynaptic['MDR21'][nextState] = 4 + postsynaptic['MDR21'][thisState]
        postsynaptic['MDR22'][nextState] = 4 + postsynaptic['MDR22'][thisState]
        postsynaptic['MDR23'][nextState] = 4 + postsynaptic['MDR23'][thisState]
        postsynaptic['MDR24'][nextState] = 4 + postsynaptic['MDR24'][thisState]
        postsynaptic['PDA'][nextState] = 1 + postsynaptic['PDA'][thisState]
        postsynaptic['PHCL'][nextState] = 1 + postsynaptic['PHCL'][thisState]
        postsynaptic['RID'][nextState] = 1 + postsynaptic['RID'][thisState]
        postsynaptic['VD13'][nextState] = 1 + postsynaptic['VD13'][thisState]

def DB1():
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]
        postsynaptic['AS2'][nextState] = 1 + postsynaptic['AS2'][thisState]
        postsynaptic['AS3'][nextState] = 1 + postsynaptic['AS3'][thisState]
        postsynaptic['AVBR'][nextState] = 3 + postsynaptic['AVBR'][thisState]
        postsynaptic['DB2'][nextState] = 1 + postsynaptic['DB2'][thisState]
        postsynaptic['DB4'][nextState] = 1 + postsynaptic['DB4'][thisState]
        postsynaptic['DD1'][nextState] = 10 + postsynaptic['DD1'][thisState]
        postsynaptic['DVA'][nextState] = 1 + postsynaptic['DVA'][thisState]
        postsynaptic['MDL07'][nextState] = 1 + postsynaptic['MDL07'][thisState]
        postsynaptic['MDL08'][nextState] = 1 + postsynaptic['MDL08'][thisState]
        postsynaptic['MDR07'][nextState] = 1 + postsynaptic['MDR07'][thisState]
        postsynaptic['MDR08'][nextState] = 1 + postsynaptic['MDR08'][thisState]
        postsynaptic['RID'][nextState] = 1 + postsynaptic['RID'][thisState]
        postsynaptic['RIS'][nextState] = 1 + postsynaptic['RIS'][thisState]
        postsynaptic['VB3'][nextState] = 1 + postsynaptic['VB3'][thisState]
        postsynaptic['VB4'][nextState] = 1 + postsynaptic['VB4'][thisState]
        postsynaptic['VD1'][nextState] = 21 + postsynaptic['VD1'][thisState]
        postsynaptic['VD2'][nextState] = 15 + postsynaptic['VD2'][thisState]
        postsynaptic['VD3'][nextState] = 1 + postsynaptic['VD3'][thisState]

def DB2():
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DA3'][nextState] = 5 + postsynaptic['DA3'][thisState]
        postsynaptic['DB1'][nextState] = 1 + postsynaptic['DB1'][thisState]
        postsynaptic['DB3'][nextState] = 6 + postsynaptic['DB3'][thisState]
        postsynaptic['DD2'][nextState] = 3 + postsynaptic['DD2'][thisState]
        postsynaptic['MDL09'][nextState] = 3 + postsynaptic['MDL09'][thisState]
        postsynaptic['MDL10'][nextState] = 3 + postsynaptic['MDL10'][thisState]
        postsynaptic['MDL11'][nextState] = 3 + postsynaptic['MDL11'][thisState]
        postsynaptic['MDL12'][nextState] = 3 + postsynaptic['MDL12'][thisState]
        postsynaptic['MDR09'][nextState] = 3 + postsynaptic['MDR09'][thisState]
        postsynaptic['MDR10'][nextState] = 3 + postsynaptic['MDR10'][thisState]
        postsynaptic['MDR11'][nextState] = 3 + postsynaptic['MDR11'][thisState]
        postsynaptic['MDR12'][nextState] = 3 + postsynaptic['MDR12'][thisState]
        postsynaptic['VB1'][nextState] = 2 + postsynaptic['VB1'][thisState]
        postsynaptic['VD3'][nextState] = 23 + postsynaptic['VD3'][thisState]
        postsynaptic['VD4'][nextState] = 14 + postsynaptic['VD4'][thisState]
        postsynaptic['VD5'][nextState] = 1 + postsynaptic['VD5'][thisState]

def DB3():
        postsynaptic['AS4'][nextState] = 1 + postsynaptic['AS4'][thisState]
        postsynaptic['AS5'][nextState] = 1 + postsynaptic['AS5'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DA4'][nextState] = 1 + postsynaptic['DA4'][thisState]
        postsynaptic['DB2'][nextState] = 6 + postsynaptic['DB2'][thisState]
        postsynaptic['DB4'][nextState] = 1 + postsynaptic['DB4'][thisState]
        postsynaptic['DD2'][nextState] = 4 + postsynaptic['DD2'][thisState]
        postsynaptic['DD3'][nextState] = 10 + postsynaptic['DD3'][thisState]
        postsynaptic['MDL11'][nextState] = 3 + postsynaptic['MDL11'][thisState]
        postsynaptic['MDL12'][nextState] = 3 + postsynaptic['MDL12'][thisState]
        postsynaptic['MDL13'][nextState] = 4 + postsynaptic['MDL13'][thisState]
        postsynaptic['MDL14'][nextState] = 3 + postsynaptic['MDL14'][thisState]
        postsynaptic['MDR11'][nextState] = 3 + postsynaptic['MDR11'][thisState]
        postsynaptic['MDR12'][nextState] = 3 + postsynaptic['MDR12'][thisState]
        postsynaptic['MDR13'][nextState] = 4 + postsynaptic['MDR13'][thisState]
        postsynaptic['MDR14'][nextState] = 3 + postsynaptic['MDR14'][thisState]
        postsynaptic['VD4'][nextState] = 9 + postsynaptic['VD4'][thisState]
        postsynaptic['VD5'][nextState] = 26 + postsynaptic['VD5'][thisState]
        postsynaptic['VD6'][nextState] = 7 + postsynaptic['VD6'][thisState]

def DB4():
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DB1'][nextState] = 1 + postsynaptic['DB1'][thisState]
        postsynaptic['DB3'][nextState] = 1 + postsynaptic['DB3'][thisState]
        postsynaptic['DD3'][nextState] = 3 + postsynaptic['DD3'][thisState]
        postsynaptic['MDL13'][nextState] = 2 + postsynaptic['MDL13'][thisState]
        postsynaptic['MDL14'][nextState] = 2 + postsynaptic['MDL14'][thisState]
        postsynaptic['MDL16'][nextState] = 2 + postsynaptic['MDL16'][thisState]
        postsynaptic['MDR13'][nextState] = 2 + postsynaptic['MDR13'][thisState]
        postsynaptic['MDR14'][nextState] = 2 + postsynaptic['MDR14'][thisState]
        postsynaptic['MDR16'][nextState] = 2 + postsynaptic['MDR16'][thisState]
        postsynaptic['VB2'][nextState] = 1 + postsynaptic['VB2'][thisState]
        postsynaptic['VB4'][nextState] = 1 + postsynaptic['VB4'][thisState]
        postsynaptic['VD6'][nextState] = 13 + postsynaptic['VD6'][thisState]

def DB5():
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['MDL15'][nextState] = 2 + postsynaptic['MDL15'][thisState]
        postsynaptic['MDL17'][nextState] = 2 + postsynaptic['MDL17'][thisState]
        postsynaptic['MDL18'][nextState] = 2 + postsynaptic['MDL18'][thisState]
        postsynaptic['MDR15'][nextState] = 2 + postsynaptic['MDR15'][thisState]
        postsynaptic['MDR17'][nextState] = 2 + postsynaptic['MDR17'][thisState]
        postsynaptic['MDR18'][nextState] = 2 + postsynaptic['MDR18'][thisState]

def DB6():
        postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['MDL17'][nextState] = 2 + postsynaptic['MDL17'][thisState]
        postsynaptic['MDL19'][nextState] = 2 + postsynaptic['MDL19'][thisState]
        postsynaptic['MDL20'][nextState] = 2 + postsynaptic['MDL20'][thisState]
        postsynaptic['MDR17'][nextState] = 2 + postsynaptic['MDR17'][thisState]
        postsynaptic['MDR19'][nextState] = 2 + postsynaptic['MDR19'][thisState]
        postsynaptic['MDR20'][nextState] = 2 + postsynaptic['MDR20'][thisState]

def DB7():
        postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['MDL19'][nextState] = 2 + postsynaptic['MDL19'][thisState]
        postsynaptic['MDL21'][nextState] = 2 + postsynaptic['MDL21'][thisState]
        postsynaptic['MDL22'][nextState] = 2 + postsynaptic['MDL22'][thisState]
        postsynaptic['MDL23'][nextState] = 2 + postsynaptic['MDL23'][thisState]
        postsynaptic['MDL24'][nextState] = 2 + postsynaptic['MDL24'][thisState]
        postsynaptic['MDR19'][nextState] = 2 + postsynaptic['MDR19'][thisState]
        postsynaptic['MDR21'][nextState] = 2 + postsynaptic['MDR21'][thisState]
        postsynaptic['MDR22'][nextState] = 2 + postsynaptic['MDR22'][thisState]
        postsynaptic['MDR23'][nextState] = 2 + postsynaptic['MDR23'][thisState]
        postsynaptic['MDR24'][nextState] = 2 + postsynaptic['MDR24'][thisState]
        postsynaptic['VD13'][nextState] = 2 + postsynaptic['VD13'][thisState]

def DD1():
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DD2'][nextState] = 3 + postsynaptic['DD2'][thisState]
        postsynaptic['MDL07'][nextState] = -6 + postsynaptic['MDL07'][thisState]
        postsynaptic['MDL08'][nextState] = -6 + postsynaptic['MDL08'][thisState]
        postsynaptic['MDL09'][nextState] = -7 + postsynaptic['MDL09'][thisState]
        postsynaptic['MDL10'][nextState] = -6 + postsynaptic['MDL10'][thisState]
        postsynaptic['MDR07'][nextState] = -6 + postsynaptic['MDR07'][thisState]
        postsynaptic['MDR08'][nextState] = -6 + postsynaptic['MDR08'][thisState]
        postsynaptic['MDR09'][nextState] = -7 + postsynaptic['MDR09'][thisState]
        postsynaptic['MDR10'][nextState] = -6 + postsynaptic['MDR10'][thisState]
        postsynaptic['VD1'][nextState] = 4 + postsynaptic['VD1'][thisState]
        postsynaptic['VD2'][nextState] = 1 + postsynaptic['VD2'][thisState]
        postsynaptic['VD2'][nextState] = 2 + postsynaptic['VD2'][thisState]

def DD2():
        postsynaptic['DA3'][nextState] = 1 + postsynaptic['DA3'][thisState]
        postsynaptic['DD1'][nextState] = 1 + postsynaptic['DD1'][thisState]
        postsynaptic['DD3'][nextState] = 2 + postsynaptic['DD3'][thisState]
        postsynaptic['MDL09'][nextState] = -6 + postsynaptic['MDL09'][thisState]
        postsynaptic['MDL11'][nextState] = -7 + postsynaptic['MDL11'][thisState]
        postsynaptic['MDL12'][nextState] = -6 + postsynaptic['MDL12'][thisState]
        postsynaptic['MDR09'][nextState] = -6 + postsynaptic['MDR09'][thisState]
        postsynaptic['MDR11'][nextState] = -7 + postsynaptic['MDR11'][thisState]
        postsynaptic['MDR12'][nextState] = -6 + postsynaptic['MDR12'][thisState]
        postsynaptic['VD3'][nextState] = 1 + postsynaptic['VD3'][thisState]
        postsynaptic['VD4'][nextState] = 3 + postsynaptic['VD4'][thisState]

def DD3():
        postsynaptic['DD2'][nextState] = 2 + postsynaptic['DD2'][thisState]
        postsynaptic['DD4'][nextState] = 1 + postsynaptic['DD4'][thisState]
        postsynaptic['MDL11'][nextState] = -7 + postsynaptic['MDL11'][thisState]
        postsynaptic['MDL13'][nextState] = -9 + postsynaptic['MDL13'][thisState]
        postsynaptic['MDL14'][nextState] = -7 + postsynaptic['MDL14'][thisState]
        postsynaptic['MDR11'][nextState] = -7 + postsynaptic['MDR11'][thisState]
        postsynaptic['MDR13'][nextState] = -9 + postsynaptic['MDR13'][thisState]
        postsynaptic['MDR14'][nextState] = -7 + postsynaptic['MDR14'][thisState]

def DD4():
        postsynaptic['DD3'][nextState] = 1 + postsynaptic['DD3'][thisState]
        postsynaptic['MDL13'][nextState] = -7 + postsynaptic['MDL13'][thisState]
        postsynaptic['MDL15'][nextState] = -7 + postsynaptic['MDL15'][thisState]
        postsynaptic['MDL16'][nextState] = -7 + postsynaptic['MDL16'][thisState]
        postsynaptic['MDR13'][nextState] = -7 + postsynaptic['MDR13'][thisState]
        postsynaptic['MDR15'][nextState] = -7 + postsynaptic['MDR15'][thisState]
        postsynaptic['MDR16'][nextState] = -7 + postsynaptic['MDR16'][thisState]
        postsynaptic['VC3'][nextState] = 1 + postsynaptic['VC3'][thisState]
        postsynaptic['VD8'][nextState] = 1 + postsynaptic['VD8'][thisState]

def DD5():
        postsynaptic['MDL17'][nextState] = -7 + postsynaptic['MDL17'][thisState]
        postsynaptic['MDL18'][nextState] = -7 + postsynaptic['MDL18'][thisState]
        postsynaptic['MDL20'][nextState] = -7 + postsynaptic['MDL20'][thisState]
        postsynaptic['MDR17'][nextState] = -7 + postsynaptic['MDR17'][thisState]
        postsynaptic['MDR18'][nextState] = -7 + postsynaptic['MDR18'][thisState]
        postsynaptic['MDR20'][nextState] = -7 + postsynaptic['MDR20'][thisState]
        postsynaptic['VB8'][nextState] = 1 + postsynaptic['VB8'][thisState]
        postsynaptic['VD10'][nextState] = 1 + postsynaptic['VD10'][thisState]
        postsynaptic['VD9'][nextState] = 1 + postsynaptic['VD9'][thisState]

def DD6():
        postsynaptic['MDL19'][nextState] = -7 + postsynaptic['MDL19'][thisState]
        postsynaptic['MDL21'][nextState] = -7 + postsynaptic['MDL21'][thisState]
        postsynaptic['MDL22'][nextState] = -7 + postsynaptic['MDL22'][thisState]
        postsynaptic['MDL23'][nextState] = -7 + postsynaptic['MDL23'][thisState]
        postsynaptic['MDL24'][nextState] = -7 + postsynaptic['MDL24'][thisState]
        postsynaptic['MDR19'][nextState] = -7 + postsynaptic['MDR19'][thisState]
        postsynaptic['MDR21'][nextState] = -7 + postsynaptic['MDR21'][thisState]
        postsynaptic['MDR22'][nextState] = -7 + postsynaptic['MDR22'][thisState]
        postsynaptic['MDR23'][nextState] = -7 + postsynaptic['MDR23'][thisState]
        postsynaptic['MDR24'][nextState] = -7 + postsynaptic['MDR24'][thisState]

def DVA():
        postsynaptic['AIZL'][nextState] = 3 + postsynaptic['AIZL'][thisState]
        postsynaptic['AQR'][nextState] = 4 + postsynaptic['AQR'][thisState]
        postsynaptic['AUAL'][nextState] = 1 + postsynaptic['AUAL'][thisState]
        postsynaptic['AUAR'][nextState] = 1 + postsynaptic['AUAR'][thisState]
        postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVEL'][nextState] = 9 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 5 + postsynaptic['AVER'][thisState]
        postsynaptic['DB1'][nextState] = 1 + postsynaptic['DB1'][thisState]
        postsynaptic['DB2'][nextState] = 1 + postsynaptic['DB2'][thisState]
        postsynaptic['DB3'][nextState] = 2 + postsynaptic['DB3'][thisState]
        postsynaptic['DB4'][nextState] = 1 + postsynaptic['DB4'][thisState]
        postsynaptic['DB5'][nextState] = 1 + postsynaptic['DB5'][thisState]
        postsynaptic['DB6'][nextState] = 2 + postsynaptic['DB6'][thisState]
        postsynaptic['DB7'][nextState] = 1 + postsynaptic['DB7'][thisState]
        postsynaptic['PDEL'][nextState] = 3 + postsynaptic['PDEL'][thisState]
        postsynaptic['PVCL'][nextState] = 3 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVR'][nextState] = 3 + postsynaptic['PVR'][thisState]
        postsynaptic['PVR'][nextState] = 2 + postsynaptic['PVR'][thisState]
        postsynaptic['RIAL'][nextState] = 1 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 1 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIMR'][nextState] = 1 + postsynaptic['RIMR'][thisState]
        postsynaptic['RIR'][nextState] = 3 + postsynaptic['RIR'][thisState]
        postsynaptic['SAADR'][nextState] = 1 + postsynaptic['SAADR'][thisState]
        postsynaptic['SAAVL'][nextState] = 1 + postsynaptic['SAAVL'][thisState]
        postsynaptic['SAAVR'][nextState] = 1 + postsynaptic['SAAVR'][thisState]
        postsynaptic['SABD'][nextState] = 1 + postsynaptic['SABD'][thisState]
        postsynaptic['SMBDL'][nextState] = 3 + postsynaptic['SMBDL'][thisState]
        postsynaptic['SMBDR'][nextState] = 2 + postsynaptic['SMBDR'][thisState]
        postsynaptic['SMBVL'][nextState] = 3 + postsynaptic['SMBVL'][thisState]
        postsynaptic['SMBVR'][nextState] = 2 + postsynaptic['SMBVR'][thisState]
        postsynaptic['VA12'][nextState] = 1 + postsynaptic['VA12'][thisState]
        postsynaptic['VA2'][nextState] = 1 + postsynaptic['VA2'][thisState]
        postsynaptic['VB1'][nextState] = 1 + postsynaptic['VB1'][thisState]
        postsynaptic['VB11'][nextState] = 2 + postsynaptic['VB11'][thisState]

def DVB():
        postsynaptic['AS9'][nextState] = 7 + postsynaptic['AS9'][thisState]
        postsynaptic['AVL'][nextState] = 5 + postsynaptic['AVL'][thisState]
        postsynaptic['AVL'][nextState] = 1 + postsynaptic['AVL'][thisState]
        postsynaptic['DA8'][nextState] = 2 + postsynaptic['DA8'][thisState]
        postsynaptic['DD6'][nextState] = 3 + postsynaptic['DD6'][thisState]
        postsynaptic['DVC'][nextState] = 3 + postsynaptic['DVC'][thisState]
        # postsynaptic['MANAL'][nextState] = -5 + postsynaptic['MANAL'][thisState] - just not needed or used
        postsynaptic['PDA'][nextState] = 1 + postsynaptic['PDA'][thisState]
        postsynaptic['PHCL'][nextState] = 1 + postsynaptic['PHCL'][thisState]
        postsynaptic['PVPL'][nextState] = 1 + postsynaptic['PVPL'][thisState]
        postsynaptic['VA9'][nextState] = 1 + postsynaptic['VA9'][thisState]
        postsynaptic['VB9'][nextState] = 1 + postsynaptic['VB9'][thisState]

def DVC():
        postsynaptic['AIBL'][nextState] = 2 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 5 + postsynaptic['AIBR'][thisState]
        postsynaptic['AVAL'][nextState] = 5 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 7 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVKL'][nextState] = 2 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 1 + postsynaptic['AVKR'][thisState]
        postsynaptic['AVL'][nextState] = 9 + postsynaptic['AVL'][thisState]
        postsynaptic['PVPL'][nextState] = 2 + postsynaptic['PVPL'][thisState]
        postsynaptic['PVPR'][nextState] = 13 + postsynaptic['PVPR'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIGL'][nextState] = 5 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIGR'][nextState] = 5 + postsynaptic['RIGR'][thisState]
        postsynaptic['RMFL'][nextState] = 2 + postsynaptic['RMFL'][thisState]
        postsynaptic['RMFR'][nextState] = 4 + postsynaptic['RMFR'][thisState]
        postsynaptic['VA9'][nextState] = 1 + postsynaptic['VA9'][thisState]
        postsynaptic['VD1'][nextState] = 5 + postsynaptic['VD1'][thisState]
        postsynaptic['VD10'][nextState] = 4 + postsynaptic['VD10'][thisState]

def FLPL():
        postsynaptic['ADEL'][nextState] = 2 + postsynaptic['ADEL'][thisState]
        postsynaptic['ADER'][nextState] = 2 + postsynaptic['ADER'][thisState]
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 2 + postsynaptic['AIBR'][thisState]
        postsynaptic['AVAL'][nextState] = 15 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 17 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 4 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 5 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 7 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 13 + postsynaptic['AVDR'][thisState]
        postsynaptic['DVA'][nextState] = 1 + postsynaptic['DVA'][thisState]
        postsynaptic['FLPR'][nextState] = 3 + postsynaptic['FLPR'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]

def FLPR():
        postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['AVAL'][nextState] = 12 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 5 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 5 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 10 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 4 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 2 + postsynaptic['AVER'][thisState]
        postsynaptic['AVJR'][nextState] = 1 + postsynaptic['AVJR'][thisState]
        postsynaptic['DVA'][nextState] = 1 + postsynaptic['DVA'][thisState]
        postsynaptic['FLPL'][nextState] = 4 + postsynaptic['FLPL'][thisState]
        postsynaptic['PVCL'][nextState] = 2 + postsynaptic['PVCL'][thisState]
        postsynaptic['VB1'][nextState] = 1 + postsynaptic['VB1'][thisState]

def HSNL():
        postsynaptic['AIAL'][nextState] = 1 + postsynaptic['AIAL'][thisState]
        postsynaptic['AIZL'][nextState] = 2 + postsynaptic['AIZL'][thisState]
        postsynaptic['AIZR'][nextState] = 1 + postsynaptic['AIZR'][thisState]
        postsynaptic['ASHL'][nextState] = 1 + postsynaptic['ASHL'][thisState]
        postsynaptic['ASHR'][nextState] = 2 + postsynaptic['ASHR'][thisState]
        postsynaptic['ASJR'][nextState] = 1 + postsynaptic['ASJR'][thisState]
        postsynaptic['ASKL'][nextState] = 1 + postsynaptic['ASKL'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVFL'][nextState] = 6 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AWBL'][nextState] = 1 + postsynaptic['AWBL'][thisState]
        postsynaptic['AWBR'][nextState] = 2 + postsynaptic['AWBR'][thisState]
        postsynaptic['HSNR'][nextState] = 3 + postsynaptic['HSNR'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['MVULVA'][nextState] = 7 + postsynaptic['MVULVA'][thisState]
        postsynaptic['RIFL'][nextState] = 3 + postsynaptic['RIFL'][thisState]
        postsynaptic['RIML'][nextState] = 2 + postsynaptic['RIML'][thisState]
        postsynaptic['SABVL'][nextState] = 2 + postsynaptic['SABVL'][thisState]
        postsynaptic['VC5'][nextState] = 3 + postsynaptic['VC5'][thisState]

def HSNR():
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIZL'][nextState] = 1 + postsynaptic['AIZL'][thisState]
        postsynaptic['AIZR'][nextState] = 1 + postsynaptic['AIZR'][thisState]
        postsynaptic['AS5'][nextState] = 1 + postsynaptic['AS5'][thisState]
        postsynaptic['ASHL'][nextState] = 2 + postsynaptic['ASHL'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVFL'][nextState] = 1 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVL'][nextState] = 1 + postsynaptic['AVL'][thisState]
        postsynaptic['AWBL'][nextState] = 1 + postsynaptic['AWBL'][thisState]
        postsynaptic['BDUR'][nextState] = 1 + postsynaptic['BDUR'][thisState]
        postsynaptic['DA5'][nextState] = 1 + postsynaptic['DA5'][thisState]
        postsynaptic['DA6'][nextState] = 1 + postsynaptic['DA6'][thisState]
        postsynaptic['HSNL'][nextState] = 2 + postsynaptic['HSNL'][thisState]
        postsynaptic['MVULVA'][nextState] = 6 + postsynaptic['MVULVA'][thisState]
        postsynaptic['PVNR'][nextState] = 2 + postsynaptic['PVNR'][thisState]
        postsynaptic['PVQR'][nextState] = 1 + postsynaptic['PVQR'][thisState]
        postsynaptic['RIFR'][nextState] = 4 + postsynaptic['RIFR'][thisState]
        postsynaptic['RMGR'][nextState] = 1 + postsynaptic['RMGR'][thisState]
        postsynaptic['SABD'][nextState] = 1 + postsynaptic['SABD'][thisState]
        postsynaptic['SABVR'][nextState] = 1 + postsynaptic['SABVR'][thisState]
        postsynaptic['VA6'][nextState] = 1 + postsynaptic['VA6'][thisState]
        postsynaptic['VC2'][nextState] = 3 + postsynaptic['VC2'][thisState]
        postsynaptic['VC3'][nextState] = 1 + postsynaptic['VC3'][thisState]
        postsynaptic['VD4'][nextState] = 2 + postsynaptic['VD4'][thisState]

def I1L():
        postsynaptic['I1R'][nextState] = 1 + postsynaptic['I1R'][thisState]
        postsynaptic['I3'][nextState] = 1 + postsynaptic['I3'][thisState]
        postsynaptic['I5'][nextState] = 1 + postsynaptic['I5'][thisState]
        postsynaptic['RIPL'][nextState] = 1 + postsynaptic['RIPL'][thisState]
        postsynaptic['RIPR'][nextState] = 1 + postsynaptic['RIPR'][thisState]

def I1R():
        postsynaptic['I1L'][nextState] = 1 + postsynaptic['I1L'][thisState]
        postsynaptic['I3'][nextState] = 1 + postsynaptic['I3'][thisState]
        postsynaptic['I5'][nextState] = 1 + postsynaptic['I5'][thisState]
        postsynaptic['RIPL'][nextState] = 1 + postsynaptic['RIPL'][thisState]
        postsynaptic['RIPR'][nextState] = 1 + postsynaptic['RIPR'][thisState]

def I2L():
        postsynaptic['I1L'][nextState] = 1 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 1 + postsynaptic['I1R'][thisState]
        postsynaptic['M1'][nextState] = 4 + postsynaptic['M1'][thisState]

def I2R():
        postsynaptic['I1L'][nextState] = 1 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 1 + postsynaptic['I1R'][thisState]
        postsynaptic['M1'][nextState] = 4 + postsynaptic['M1'][thisState]

def I3():
        postsynaptic['M1'][nextState] = 4 + postsynaptic['M1'][thisState]
        postsynaptic['M2L'][nextState] = 2 + postsynaptic['M2L'][thisState]
        postsynaptic['M2R'][nextState] = 2 + postsynaptic['M2R'][thisState]

def I4():
        postsynaptic['I2L'][nextState] = 5 + postsynaptic['I2L'][thisState]
        postsynaptic['I2R'][nextState] = 5 + postsynaptic['I2R'][thisState]
        postsynaptic['I5'][nextState] = 2 + postsynaptic['I5'][thisState]
        postsynaptic['M1'][nextState] = 4 + postsynaptic['M1'][thisState]

def I5():
        postsynaptic['I1L'][nextState] = 4 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 3 + postsynaptic['I1R'][thisState]
        postsynaptic['M1'][nextState] = 2 + postsynaptic['M1'][thisState]
        postsynaptic['M5'][nextState] = 2 + postsynaptic['M5'][thisState]
        postsynaptic['MI'][nextState] = 4 + postsynaptic['MI'][thisState]

def I6():
        postsynaptic['I2L'][nextState] = 2 + postsynaptic['I2L'][thisState]
        postsynaptic['I2R'][nextState] = 2 + postsynaptic['I2R'][thisState]
        postsynaptic['I3'][nextState] = 1 + postsynaptic['I3'][thisState]
        postsynaptic['M4'][nextState] = 1 + postsynaptic['M4'][thisState]
        postsynaptic['M5'][nextState] = 2 + postsynaptic['M5'][thisState]
        postsynaptic['NSML'][nextState] = 2 + postsynaptic['NSML'][thisState]
        postsynaptic['NSMR'][nextState] = 2 + postsynaptic['NSMR'][thisState]

def IL1DL():
        postsynaptic['IL1DR'][nextState] = 1 + postsynaptic['IL1DR'][thisState]
        postsynaptic['IL1L'][nextState] = 1 + postsynaptic['IL1L'][thisState]
        postsynaptic['MDL01'][nextState] = 1 + postsynaptic['MDL01'][thisState]
        postsynaptic['MDL02'][nextState] = 1 + postsynaptic['MDL02'][thisState]
        postsynaptic['MDL04'][nextState] = 2 + postsynaptic['MDL04'][thisState]
        postsynaptic['OLLL'][nextState] = 1 + postsynaptic['OLLL'][thisState]
        postsynaptic['PVR'][nextState] = 1 + postsynaptic['PVR'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]
        postsynaptic['RIPL'][nextState] = 2 + postsynaptic['RIPL'][thisState]
        postsynaptic['RMDDR'][nextState] = 1 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 4 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]
        postsynaptic['URYDL'][nextState] = 1 + postsynaptic['URYDL'][thisState]

def IL1DR():
        postsynaptic['IL1DL'][nextState] = 1 + postsynaptic['IL1DL'][thisState]
        postsynaptic['IL1R'][nextState] = 1 + postsynaptic['IL1R'][thisState]
        postsynaptic['MDR01'][nextState] = 4 + postsynaptic['MDR01'][thisState]
        postsynaptic['MDR02'][nextState] = 3 + postsynaptic['MDR02'][thisState]
        postsynaptic['OLLR'][nextState] = 1 + postsynaptic['OLLR'][thisState]
        postsynaptic['RIPR'][nextState] = 5 + postsynaptic['RIPR'][thisState]
        postsynaptic['RMDVR'][nextState] = 5 + postsynaptic['RMDVR'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]

def IL1L():
        postsynaptic['AVER'][nextState] = 2 + postsynaptic['AVER'][thisState]
        postsynaptic['IL1DL'][nextState] = 2 + postsynaptic['IL1DL'][thisState]
        postsynaptic['IL1VL'][nextState] = 1 + postsynaptic['IL1VL'][thisState]
        postsynaptic['MDL01'][nextState] = 3 + postsynaptic['MDL01'][thisState]
        postsynaptic['MDL03'][nextState] = 3 + postsynaptic['MDL03'][thisState]
        postsynaptic['MDL05'][nextState] = 4 + postsynaptic['MDL05'][thisState]
        postsynaptic['MVL01'][nextState] = 3 + postsynaptic['MVL01'][thisState]
        postsynaptic['MVL03'][nextState] = 3 + postsynaptic['MVL03'][thisState]
        postsynaptic['RMDDL'][nextState] = 5 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDL'][nextState] = 1 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDR'][nextState] = 3 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 4 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMDVR'][nextState] = 2 + postsynaptic['RMDVR'][thisState]
        postsynaptic['RMER'][nextState] = 1 + postsynaptic['RMER'][thisState]

def IL1R():
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['IL1DR'][nextState] = 2 + postsynaptic['IL1DR'][thisState]
        postsynaptic['IL1VR'][nextState] = 1 + postsynaptic['IL1VR'][thisState]
        postsynaptic['MDR01'][nextState] = 3 + postsynaptic['MDR01'][thisState]
        postsynaptic['MDR03'][nextState] = 3 + postsynaptic['MDR03'][thisState]
        postsynaptic['MVR01'][nextState] = 3 + postsynaptic['MVR01'][thisState]
        postsynaptic['MVR03'][nextState] = 3 + postsynaptic['MVR03'][thisState]
        postsynaptic['RMDDL'][nextState] = 3 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDDR'][nextState] = 2 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDL'][nextState] = 4 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDR'][nextState] = 2 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 1 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMDVR'][nextState] = 4 + postsynaptic['RMDVR'][thisState]
        postsynaptic['RMEL'][nextState] = 2 + postsynaptic['RMEL'][thisState]
        postsynaptic['RMHL'][nextState] = 1 + postsynaptic['RMHL'][thisState]
        postsynaptic['URXR'][nextState] = 2 + postsynaptic['URXR'][thisState]

def IL1VL():
        postsynaptic['IL1L'][nextState] = 2 + postsynaptic['IL1L'][thisState]
        postsynaptic['IL1VR'][nextState] = 1 + postsynaptic['IL1VR'][thisState]
        postsynaptic['MVL01'][nextState] = 5 + postsynaptic['MVL01'][thisState]
        postsynaptic['MVL02'][nextState] = 4 + postsynaptic['MVL02'][thisState]
        postsynaptic['RIPL'][nextState] = 4 + postsynaptic['RIPL'][thisState]
        postsynaptic['RMDDL'][nextState] = 5 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMED'][nextState] = 1 + postsynaptic['RMED'][thisState]
        postsynaptic['URYVL'][nextState] = 1 + postsynaptic['URYVL'][thisState]

def IL1VR():
        postsynaptic['IL1R'][nextState] = 2 + postsynaptic['IL1R'][thisState]
        postsynaptic['IL1VL'][nextState] = 1 + postsynaptic['IL1VL'][thisState]
        postsynaptic['IL2R'][nextState] = 1 + postsynaptic['IL2R'][thisState]
        postsynaptic['IL2VR'][nextState] = 1 + postsynaptic['IL2VR'][thisState]
        postsynaptic['MVR01'][nextState] = 5 + postsynaptic['MVR01'][thisState]
        postsynaptic['MVR02'][nextState] = 5 + postsynaptic['MVR02'][thisState]
        postsynaptic['RIPR'][nextState] = 6 + postsynaptic['RIPR'][thisState]
        postsynaptic['RMDDR'][nextState] = 10 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMER'][nextState] = 1 + postsynaptic['RMER'][thisState]

def IL2DL():
        postsynaptic['AUAL'][nextState] = 1 + postsynaptic['AUAL'][thisState]
        postsynaptic['IL1DL'][nextState] = 7 + postsynaptic['IL1DL'][thisState]
        postsynaptic['OLQDL'][nextState] = 2 + postsynaptic['OLQDL'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIPL'][nextState] = 10 + postsynaptic['RIPL'][thisState]
        postsynaptic['RMEL'][nextState] = 4 + postsynaptic['RMEL'][thisState]
        postsynaptic['RMER'][nextState] = 3 + postsynaptic['RMER'][thisState]
        postsynaptic['URADL'][nextState] = 3 + postsynaptic['URADL'][thisState]

def IL2DR():
        postsynaptic['CEPDR'][nextState] = 1 + postsynaptic['CEPDR'][thisState]
        postsynaptic['IL1DR'][nextState] = 7 + postsynaptic['IL1DR'][thisState]
        postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
        postsynaptic['RIPR'][nextState] = 11 + postsynaptic['RIPR'][thisState]
        postsynaptic['RMED'][nextState] = 1 + postsynaptic['RMED'][thisState]
        postsynaptic['RMEL'][nextState] = 2 + postsynaptic['RMEL'][thisState]
        postsynaptic['RMER'][nextState] = 2 + postsynaptic['RMER'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]
        postsynaptic['URADR'][nextState] = 3 + postsynaptic['URADR'][thisState]

def IL2L():
        postsynaptic['ADEL'][nextState] = 2 + postsynaptic['ADEL'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['IL1L'][nextState] = 1 + postsynaptic['IL1L'][thisState]
        postsynaptic['OLQDL'][nextState] = 5 + postsynaptic['OLQDL'][thisState]
        postsynaptic['OLQVL'][nextState] = 8 + postsynaptic['OLQVL'][thisState]
        postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
        postsynaptic['RIH'][nextState] = 7 + postsynaptic['RIH'][thisState]
        postsynaptic['RMDL'][nextState] = 3 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDR'][nextState] = 1 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMER'][nextState] = 2 + postsynaptic['RMER'][thisState]
        postsynaptic['RMEV'][nextState] = 2 + postsynaptic['RMEV'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]
        postsynaptic['URXL'][nextState] = 2 + postsynaptic['URXL'][thisState]

def IL2R():
        postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
        postsynaptic['IL1R'][nextState] = 1 + postsynaptic['IL1R'][thisState]
        postsynaptic['IL1VR'][nextState] = 1 + postsynaptic['IL1VR'][thisState]
        postsynaptic['OLLR'][nextState] = 1 + postsynaptic['OLLR'][thisState]
        postsynaptic['OLQDR'][nextState] = 2 + postsynaptic['OLQDR'][thisState]
        postsynaptic['OLQVR'][nextState] = 7 + postsynaptic['OLQVR'][thisState]
        postsynaptic['RIH'][nextState] = 6 + postsynaptic['RIH'][thisState]
        postsynaptic['RMDL'][nextState] = 1 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMEL'][nextState] = 2 + postsynaptic['RMEL'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]
        postsynaptic['RMGR'][nextState] = 1 + postsynaptic['RMGR'][thisState]
        postsynaptic['URBR'][nextState] = 1 + postsynaptic['URBR'][thisState]
        postsynaptic['URXR'][nextState] = 1 + postsynaptic['URXR'][thisState]

def IL2VL():
        postsynaptic['BAGR'][nextState] = 1 + postsynaptic['BAGR'][thisState]
        postsynaptic['IL1VL'][nextState] = 7 + postsynaptic['IL1VL'][thisState]
        postsynaptic['IL2L'][nextState] = 1 + postsynaptic['IL2L'][thisState]
        postsynaptic['OLQVL'][nextState] = 1 + postsynaptic['OLQVL'][thisState]
        postsynaptic['RIAL'][nextState] = 1 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIH'][nextState] = 2 + postsynaptic['RIH'][thisState]
        postsynaptic['RIPL'][nextState] = 1 + postsynaptic['RIPL'][thisState]
        postsynaptic['RMEL'][nextState] = 1 + postsynaptic['RMEL'][thisState]
        postsynaptic['RMER'][nextState] = 4 + postsynaptic['RMER'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]
        postsynaptic['URAVL'][nextState] = 3 + postsynaptic['URAVL'][thisState]

def IL2VR():
        postsynaptic['IL1VR'][nextState] = 6 + postsynaptic['IL1VR'][thisState]
        postsynaptic['OLQVR'][nextState] = 1 + postsynaptic['OLQVR'][thisState]
        postsynaptic['RIAR'][nextState] = 2 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIH'][nextState] = 3 + postsynaptic['RIH'][thisState]
        postsynaptic['RIPR'][nextState] = 15 + postsynaptic['RIPR'][thisState]
        postsynaptic['RMEL'][nextState] = 3 + postsynaptic['RMEL'][thisState]
        postsynaptic['RMER'][nextState] = 2 + postsynaptic['RMER'][thisState]
        postsynaptic['RMEV'][nextState] = 3 + postsynaptic['RMEV'][thisState]
        postsynaptic['URAVR'][nextState] = 4 + postsynaptic['URAVR'][thisState]
        postsynaptic['URXR'][nextState] = 1 + postsynaptic['URXR'][thisState]

def LUAL():
        postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 6 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVDL'][nextState] = 4 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['PHBL'][nextState] = 1 + postsynaptic['PHBL'][thisState]
        postsynaptic['PLML'][nextState] = 1 + postsynaptic['PLML'][thisState]
        postsynaptic['PVNL'][nextState] = 1 + postsynaptic['PVNL'][thisState]
        postsynaptic['PVR'][nextState] = 1 + postsynaptic['PVR'][thisState]
        postsynaptic['PVWL'][nextState] = 1 + postsynaptic['PVWL'][thisState]

def LUAR():
        postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 7 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 3 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVJR'][nextState] = 1 + postsynaptic['AVJR'][thisState]
        postsynaptic['PLMR'][nextState] = 1 + postsynaptic['PLMR'][thisState]
        postsynaptic['PQR'][nextState] = 1 + postsynaptic['PQR'][thisState]
        postsynaptic['PVCR'][nextState] = 3 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVR'][nextState] = 2 + postsynaptic['PVR'][thisState]
        postsynaptic['PVWL'][nextState] = 1 + postsynaptic['PVWL'][thisState]

def M1():
        postsynaptic['I2L'][nextState] = 2 + postsynaptic['I2L'][thisState]
        postsynaptic['I2R'][nextState] = 2 + postsynaptic['I2R'][thisState]
        postsynaptic['I3'][nextState] = 1 + postsynaptic['I3'][thisState]
        postsynaptic['I4'][nextState] = 1 + postsynaptic['I4'][thisState]

def M2L():
        postsynaptic['I1L'][nextState] = 3 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 3 + postsynaptic['I1R'][thisState]
        postsynaptic['I3'][nextState] = 3 + postsynaptic['I3'][thisState]
        postsynaptic['M2R'][nextState] = 1 + postsynaptic['M2R'][thisState]
        postsynaptic['M5'][nextState] = 1 + postsynaptic['M5'][thisState]
        postsynaptic['MI'][nextState] = 4 + postsynaptic['MI'][thisState]

def M2R():
        postsynaptic['I1L'][nextState] = 3 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 3 + postsynaptic['I1R'][thisState]
        postsynaptic['I3'][nextState] = 3 + postsynaptic['I3'][thisState]
        postsynaptic['M3L'][nextState] = 1 + postsynaptic['M3L'][thisState]
        postsynaptic['M3R'][nextState] = 1 + postsynaptic['M3R'][thisState]
        postsynaptic['M5'][nextState] = 1 + postsynaptic['M5'][thisState]
        postsynaptic['MI'][nextState] = 4 + postsynaptic['MI'][thisState]

def M3L():
        postsynaptic['I1L'][nextState] = 4 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 4 + postsynaptic['I1R'][thisState]
        postsynaptic['I4'][nextState] = 2 + postsynaptic['I4'][thisState]
        postsynaptic['I5'][nextState] = 3 + postsynaptic['I5'][thisState]
        postsynaptic['I6'][nextState] = 1 + postsynaptic['I6'][thisState]
        postsynaptic['M1'][nextState] = 2 + postsynaptic['M1'][thisState]
        postsynaptic['M3R'][nextState] = 1 + postsynaptic['M3R'][thisState]
        postsynaptic['MCL'][nextState] = 1 + postsynaptic['MCL'][thisState]
        postsynaptic['MCR'][nextState] = 1 + postsynaptic['MCR'][thisState]
        postsynaptic['MI'][nextState] = 2 + postsynaptic['MI'][thisState]
        postsynaptic['NSML'][nextState] = 2 + postsynaptic['NSML'][thisState]
        postsynaptic['NSMR'][nextState] = 3 + postsynaptic['NSMR'][thisState]

def M3R():
        postsynaptic['I1L'][nextState] = 4 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 4 + postsynaptic['I1R'][thisState]
        postsynaptic['I3'][nextState] = 2 + postsynaptic['I3'][thisState]
        postsynaptic['I4'][nextState] = 6 + postsynaptic['I4'][thisState]
        postsynaptic['I5'][nextState] = 3 + postsynaptic['I5'][thisState]
        postsynaptic['I6'][nextState] = 1 + postsynaptic['I6'][thisState]
        postsynaptic['M1'][nextState] = 2 + postsynaptic['M1'][thisState]
        postsynaptic['M3L'][nextState] = 1 + postsynaptic['M3L'][thisState]
        postsynaptic['MCL'][nextState] = 1 + postsynaptic['MCL'][thisState]
        postsynaptic['MCR'][nextState] = 1 + postsynaptic['MCR'][thisState]
        postsynaptic['MI'][nextState] = 2 + postsynaptic['MI'][thisState]
        postsynaptic['NSML'][nextState] = 2 + postsynaptic['NSML'][thisState]
        postsynaptic['NSMR'][nextState] = 3 + postsynaptic['NSMR'][thisState]

def M4():
        postsynaptic['I3'][nextState] = 1 + postsynaptic['I3'][thisState]
        postsynaptic['I5'][nextState] = 13 + postsynaptic['I5'][thisState]
        postsynaptic['I6'][nextState] = 3 + postsynaptic['I6'][thisState]
        postsynaptic['M2L'][nextState] = 1 + postsynaptic['M2L'][thisState]
        postsynaptic['M2R'][nextState] = 1 + postsynaptic['M2R'][thisState]
        postsynaptic['M4'][nextState] = 6 + postsynaptic['M4'][thisState]
        postsynaptic['M5'][nextState] = 1 + postsynaptic['M5'][thisState]
        postsynaptic['NSML'][nextState] = 1 + postsynaptic['NSML'][thisState]
        postsynaptic['NSMR'][nextState] = 1 + postsynaptic['NSMR'][thisState]

def M5():
        postsynaptic['I5'][nextState] = 3 + postsynaptic['I5'][thisState]
        postsynaptic['I5'][nextState] = 1 + postsynaptic['I5'][thisState]
        postsynaptic['I6'][nextState] = 1 + postsynaptic['I6'][thisState]
        postsynaptic['M1'][nextState] = 2 + postsynaptic['M1'][thisState]
        postsynaptic['M2L'][nextState] = 2 + postsynaptic['M2L'][thisState]
        postsynaptic['M2R'][nextState] = 2 + postsynaptic['M2R'][thisState]
        postsynaptic['M5'][nextState] = 4 + postsynaptic['M5'][thisState]

def MCL():
        postsynaptic['I1L'][nextState] = 3 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 3 + postsynaptic['I1R'][thisState]
        postsynaptic['I2L'][nextState] = 1 + postsynaptic['I2L'][thisState]
        postsynaptic['I2R'][nextState] = 1 + postsynaptic['I2R'][thisState]
        postsynaptic['I3'][nextState] = 1 + postsynaptic['I3'][thisState]
        postsynaptic['M1'][nextState] = 2 + postsynaptic['M1'][thisState]
        postsynaptic['M2L'][nextState] = 2 + postsynaptic['M2L'][thisState]
        postsynaptic['M2R'][nextState] = 2 + postsynaptic['M2R'][thisState]

def MCR():
        postsynaptic['I1L'][nextState] = 3 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 3 + postsynaptic['I1R'][thisState]
        postsynaptic['I3'][nextState] = 1 + postsynaptic['I3'][thisState]
        postsynaptic['M1'][nextState] = 2 + postsynaptic['M1'][thisState]
        postsynaptic['M2L'][nextState] = 2 + postsynaptic['M2L'][thisState]
        postsynaptic['M2R'][nextState] = 2 + postsynaptic['M2R'][thisState]

def MI():
        postsynaptic['I1L'][nextState] = 1 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 1 + postsynaptic['I1R'][thisState]
        postsynaptic['I3'][nextState] = 1 + postsynaptic['I3'][thisState]
        postsynaptic['I4'][nextState] = 1 + postsynaptic['I4'][thisState]
        postsynaptic['I5'][nextState] = 2 + postsynaptic['I5'][thisState]
        postsynaptic['M1'][nextState] = 1 + postsynaptic['M1'][thisState]
        postsynaptic['M2L'][nextState] = 2 + postsynaptic['M2L'][thisState]
        postsynaptic['M2R'][nextState] = 2 + postsynaptic['M2R'][thisState]
        postsynaptic['M3L'][nextState] = 1 + postsynaptic['M3L'][thisState]
        postsynaptic['M3R'][nextState] = 1 + postsynaptic['M3R'][thisState]
        postsynaptic['MCL'][nextState] = 2 + postsynaptic['MCL'][thisState]
        postsynaptic['MCR'][nextState] = 2 + postsynaptic['MCR'][thisState]

def NSML():
        postsynaptic['I1L'][nextState] = 1 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 2 + postsynaptic['I1R'][thisState]
        postsynaptic['I2L'][nextState] = 6 + postsynaptic['I2L'][thisState]
        postsynaptic['I2R'][nextState] = 6 + postsynaptic['I2R'][thisState]
        postsynaptic['I3'][nextState] = 2 + postsynaptic['I3'][thisState]
        postsynaptic['I4'][nextState] = 3 + postsynaptic['I4'][thisState]
        postsynaptic['I5'][nextState] = 2 + postsynaptic['I5'][thisState]
        postsynaptic['I6'][nextState] = 2 + postsynaptic['I6'][thisState]
        postsynaptic['M3L'][nextState] = 2 + postsynaptic['M3L'][thisState]
        postsynaptic['M3R'][nextState] = 2 + postsynaptic['M3R'][thisState]

def NSMR():
        postsynaptic['I1L'][nextState] = 2 + postsynaptic['I1L'][thisState]
        postsynaptic['I1R'][nextState] = 2 + postsynaptic['I1R'][thisState]
        postsynaptic['I2L'][nextState] = 6 + postsynaptic['I2L'][thisState]
        postsynaptic['I2R'][nextState] = 6 + postsynaptic['I2R'][thisState]
        postsynaptic['I3'][nextState] = 2 + postsynaptic['I3'][thisState]
        postsynaptic['I4'][nextState] = 3 + postsynaptic['I4'][thisState]
        postsynaptic['I5'][nextState] = 2 + postsynaptic['I5'][thisState]
        postsynaptic['I6'][nextState] = 2 + postsynaptic['I6'][thisState]
        postsynaptic['M3L'][nextState] = 2 + postsynaptic['M3L'][thisState]
        postsynaptic['M3R'][nextState] = 2 + postsynaptic['M3R'][thisState]

def OLLL():
        postsynaptic['AVER'][nextState] = 21 + postsynaptic['AVER'][thisState]
        postsynaptic['CEPDL'][nextState] = 3 + postsynaptic['CEPDL'][thisState]
        postsynaptic['CEPVL'][nextState] = 4 + postsynaptic['CEPVL'][thisState]
        postsynaptic['IL1DL'][nextState] = 1 + postsynaptic['IL1DL'][thisState]
        postsynaptic['IL1VL'][nextState] = 2 + postsynaptic['IL1VL'][thisState]
        postsynaptic['OLLR'][nextState] = 2 + postsynaptic['OLLR'][thisState]
        postsynaptic['RIBL'][nextState] = 8 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RMDDL'][nextState] = 7 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDL'][nextState] = 2 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDVL'][nextState] = 1 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMEL'][nextState] = 2 + postsynaptic['RMEL'][thisState]
        postsynaptic['SMDDL'][nextState] = 3 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDDR'][nextState] = 4 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVR'][nextState] = 4 + postsynaptic['SMDVR'][thisState]
        postsynaptic['URYDL'][nextState] = 1 + postsynaptic['URYDL'][thisState]

def OLLR():
        postsynaptic['AVEL'][nextState] = 16 + postsynaptic['AVEL'][thisState]
        postsynaptic['CEPDR'][nextState] = 1 + postsynaptic['CEPDR'][thisState]
        postsynaptic['CEPVR'][nextState] = 6 + postsynaptic['CEPVR'][thisState]
        postsynaptic['IL1DR'][nextState] = 3 + postsynaptic['IL1DR'][thisState]
        postsynaptic['IL1VR'][nextState] = 1 + postsynaptic['IL1VR'][thisState]
        postsynaptic['IL2R'][nextState] = 1 + postsynaptic['IL2R'][thisState]
        postsynaptic['OLLL'][nextState] = 2 + postsynaptic['OLLL'][thisState]
        postsynaptic['RIBR'][nextState] = 10 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['RMDDR'][nextState] = 10 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDL'][nextState] = 3 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDVR'][nextState] = 3 + postsynaptic['RMDVR'][thisState]
        postsynaptic['RMER'][nextState] = 2 + postsynaptic['RMER'][thisState]
        postsynaptic['SMDDR'][nextState] = 1 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVL'][nextState] = 4 + postsynaptic['SMDVL'][thisState]
        postsynaptic['SMDVR'][nextState] = 3 + postsynaptic['SMDVR'][thisState]

def OLQDL():
        postsynaptic['CEPDL'][nextState] = 1 + postsynaptic['CEPDL'][thisState]
        postsynaptic['RIBL'][nextState] = 2 + postsynaptic['RIBL'][thisState]
        postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RMDDR'][nextState] = 4 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 1 + postsynaptic['RMDVL'][thisState]
        postsynaptic['SIBVL'][nextState] = 3 + postsynaptic['SIBVL'][thisState]
        postsynaptic['URBL'][nextState] = 1 + postsynaptic['URBL'][thisState]

def OLQDR():
        postsynaptic['CEPDR'][nextState] = 2 + postsynaptic['CEPDR'][thisState]
        postsynaptic['RIBR'][nextState] = 2 + postsynaptic['RIBR'][thisState]
        postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
        postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]
        postsynaptic['RMDDL'][nextState] = 3 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDVR'][nextState] = 1 + postsynaptic['RMDVR'][thisState]
        postsynaptic['RMHR'][nextState] = 1 + postsynaptic['RMHR'][thisState]
        postsynaptic['SIBVR'][nextState] = 2 + postsynaptic['SIBVR'][thisState]
        postsynaptic['URBR'][nextState] = 1 + postsynaptic['URBR'][thisState]

def OLQVL():
        postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]
        postsynaptic['CEPVL'][nextState] = 1 + postsynaptic['CEPVL'][thisState]
        postsynaptic['IL1VL'][nextState] = 1 + postsynaptic['IL1VL'][thisState]
        postsynaptic['IL2VL'][nextState] = 1 + postsynaptic['IL2VL'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]
        postsynaptic['RIPL'][nextState] = 1 + postsynaptic['RIPL'][thisState]
        postsynaptic['RMDDL'][nextState] = 1 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDVR'][nextState] = 4 + postsynaptic['RMDVR'][thisState]
        postsynaptic['SIBDL'][nextState] = 3 + postsynaptic['SIBDL'][thisState]
        postsynaptic['URBL'][nextState] = 1 + postsynaptic['URBL'][thisState]

def OLQVR():
        postsynaptic['CEPVR'][nextState] = 1 + postsynaptic['CEPVR'][thisState]
        postsynaptic['IL1VR'][nextState] = 1 + postsynaptic['IL1VR'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIH'][nextState] = 2 + postsynaptic['RIH'][thisState]
        postsynaptic['RIPR'][nextState] = 2 + postsynaptic['RIPR'][thisState]
        postsynaptic['RMDDR'][nextState] = 1 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 4 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMER'][nextState] = 1 + postsynaptic['RMER'][thisState]
        postsynaptic['SIBDR'][nextState] = 4 + postsynaptic['SIBDR'][thisState]
        postsynaptic['URBR'][nextState] = 1 + postsynaptic['URBR'][thisState]

def PDA():
        postsynaptic['AS11'][nextState] = 1 + postsynaptic['AS11'][thisState]
        postsynaptic['DA9'][nextState] = 1 + postsynaptic['DA9'][thisState]
        postsynaptic['DD6'][nextState] = 1 + postsynaptic['DD6'][thisState]
        postsynaptic['MDL21'][nextState] = 2 + postsynaptic['MDL21'][thisState]
        postsynaptic['PVNR'][nextState] = 1 + postsynaptic['PVNR'][thisState]
        postsynaptic['VD13'][nextState] = 3 + postsynaptic['VD13'][thisState]

def PDB():
        postsynaptic['AS11'][nextState] = 2 + postsynaptic['AS11'][thisState]
        postsynaptic['MVL22'][nextState] = 1 + postsynaptic['MVL22'][thisState]
        postsynaptic['MVR21'][nextState] = 1 + postsynaptic['MVR21'][thisState]
        postsynaptic['RID'][nextState] = 2 + postsynaptic['RID'][thisState]
        postsynaptic['VD13'][nextState] = 2 + postsynaptic['VD13'][thisState]

def PDEL():
        postsynaptic['AVKL'][nextState] = 6 + postsynaptic['AVKL'][thisState]
        postsynaptic['DVA'][nextState] = 24 + postsynaptic['DVA'][thisState]
        postsynaptic['PDER'][nextState] = 1 + postsynaptic['PDER'][thisState]
        postsynaptic['PDER'][nextState] = 3 + postsynaptic['PDER'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVM'][nextState] = 2 + postsynaptic['PVM'][thisState]
        postsynaptic['PVM'][nextState] = 1 + postsynaptic['PVM'][thisState]
        postsynaptic['PVR'][nextState] = 2 + postsynaptic['PVR'][thisState]
        postsynaptic['VA9'][nextState] = 1 + postsynaptic['VA9'][thisState]
        postsynaptic['VD11'][nextState] = 1 + postsynaptic['VD11'][thisState]

def PDER():
        postsynaptic['AVKL'][nextState] = 16 + postsynaptic['AVKL'][thisState]
        postsynaptic['DVA'][nextState] = 35 + postsynaptic['DVA'][thisState]
        postsynaptic['PDEL'][nextState] = 3 + postsynaptic['PDEL'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVM'][nextState] = 1 + postsynaptic['PVM'][thisState]
        postsynaptic['VA8'][nextState] = 1 + postsynaptic['VA8'][thisState]
        postsynaptic['VD9'][nextState] = 1 + postsynaptic['VD9'][thisState]

def PHAL():
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVFL'][nextState] = 3 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVG'][nextState] = 5 + postsynaptic['AVG'][thisState]
        postsynaptic['AVHL'][nextState] = 1 + postsynaptic['AVHL'][thisState]
        postsynaptic['AVHR'][nextState] = 1 + postsynaptic['AVHR'][thisState]
        postsynaptic['DVA'][nextState] = 2 + postsynaptic['DVA'][thisState]
        postsynaptic['PHAR'][nextState] = 5 + postsynaptic['PHAR'][thisState]
        postsynaptic['PHAR'][nextState] = 2 + postsynaptic['PHAR'][thisState]
        postsynaptic['PHBL'][nextState] = 5 + postsynaptic['PHBL'][thisState]
        postsynaptic['PHBR'][nextState] = 5 + postsynaptic['PHBR'][thisState]
        postsynaptic['PVQL'][nextState] = 2 + postsynaptic['PVQL'][thisState]

def PHAR():
        postsynaptic['AVG'][nextState] = 3 + postsynaptic['AVG'][thisState]
        postsynaptic['AVHR'][nextState] = 1 + postsynaptic['AVHR'][thisState]
        postsynaptic['DA8'][nextState] = 1 + postsynaptic['DA8'][thisState]
        postsynaptic['DVA'][nextState] = 1 + postsynaptic['DVA'][thisState]
        postsynaptic['PHAL'][nextState] = 6 + postsynaptic['PHAL'][thisState]
        postsynaptic['PHAL'][nextState] = 2 + postsynaptic['PHAL'][thisState]
        postsynaptic['PHBL'][nextState] = 1 + postsynaptic['PHBL'][thisState]
        postsynaptic['PHBR'][nextState] = 5 + postsynaptic['PHBR'][thisState]
        postsynaptic['PVPL'][nextState] = 3 + postsynaptic['PVPL'][thisState]
        postsynaptic['PVQL'][nextState] = 2 + postsynaptic['PVQL'][thisState]

def PHBL():
        postsynaptic['AVAL'][nextState] = 9 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 6 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['PHBR'][nextState] = 1 + postsynaptic['PHBR'][thisState]
        postsynaptic['PHBR'][nextState] = 3 + postsynaptic['PHBR'][thisState]
        postsynaptic['PVCL'][nextState] = 13 + postsynaptic['PVCL'][thisState]
        postsynaptic['VA12'][nextState] = 1 + postsynaptic['VA12'][thisState]

def PHBR():
        postsynaptic['AVAL'][nextState] = 7 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 7 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVFL'][nextState] = 1 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVHL'][nextState] = 1 + postsynaptic['AVHL'][thisState]
        postsynaptic['DA8'][nextState] = 1 + postsynaptic['DA8'][thisState]
        postsynaptic['PHBL'][nextState] = 1 + postsynaptic['PHBL'][thisState]
        postsynaptic['PHBL'][nextState] = 3 + postsynaptic['PHBL'][thisState]
        postsynaptic['PVCL'][nextState] = 6 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 3 + postsynaptic['PVCR'][thisState]
        postsynaptic['VA12'][nextState] = 2 + postsynaptic['VA12'][thisState]

def PHCL():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['DA9'][nextState] = 7 + postsynaptic['DA9'][thisState]
        postsynaptic['DA9'][nextState] = 1 + postsynaptic['DA9'][thisState]
        postsynaptic['DVA'][nextState] = 6 + postsynaptic['DVA'][thisState]
        postsynaptic['LUAL'][nextState] = 1 + postsynaptic['LUAL'][thisState]
        postsynaptic['PHCR'][nextState] = 1 + postsynaptic['PHCR'][thisState]
        postsynaptic['PLML'][nextState] = 1 + postsynaptic['PLML'][thisState]
        postsynaptic['PVCL'][nextState] = 2 + postsynaptic['PVCL'][thisState]
        postsynaptic['VA12'][nextState] = 3 + postsynaptic['VA12'][thisState]

def PHCR():
        postsynaptic['AVHR'][nextState] = 1 + postsynaptic['AVHR'][thisState]
        postsynaptic['DA9'][nextState] = 2 + postsynaptic['DA9'][thisState]
        postsynaptic['DVA'][nextState] = 8 + postsynaptic['DVA'][thisState]
        postsynaptic['LUAR'][nextState] = 1 + postsynaptic['LUAR'][thisState]
        postsynaptic['PHCL'][nextState] = 2 + postsynaptic['PHCL'][thisState]
        postsynaptic['PVCR'][nextState] = 9 + postsynaptic['PVCR'][thisState]
        postsynaptic['VA12'][nextState] = 2 + postsynaptic['VA12'][thisState]

def PLML():
        postsynaptic['HSNL'][nextState] = 1 + postsynaptic['HSNL'][thisState]
        postsynaptic['LUAL'][nextState] = 1 + postsynaptic['LUAL'][thisState]
        postsynaptic['PHCL'][nextState] = 1 + postsynaptic['PHCL'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]

def PLMR():
        postsynaptic['AS6'][nextState] = 1 + postsynaptic['AS6'][thisState]
        postsynaptic['AVAL'][nextState] = 4 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 4 + postsynaptic['AVDR'][thisState]
        postsynaptic['DVA'][nextState] = 5 + postsynaptic['DVA'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['LUAR'][nextState] = 1 + postsynaptic['LUAR'][thisState]
        postsynaptic['PDEL'][nextState] = 2 + postsynaptic['PDEL'][thisState]
        postsynaptic['PDER'][nextState] = 3 + postsynaptic['PDER'][thisState]
        postsynaptic['PVCL'][nextState] = 2 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVR'][nextState] = 2 + postsynaptic['PVR'][thisState]

def PLNL():
        postsynaptic['SAADL'][nextState] = 5 + postsynaptic['SAADL'][thisState]
        postsynaptic['SMBVL'][nextState] = 6 + postsynaptic['SMBVL'][thisState]

def PLNR():
        postsynaptic['SAADR'][nextState] = 4 + postsynaptic['SAADR'][thisState]
        postsynaptic['SMBVR'][nextState] = 6 + postsynaptic['SMBVR'][thisState]

def PQR():
        postsynaptic['AVAL'][nextState] = 8 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 11 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVDL'][nextState] = 7 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 6 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVG'][nextState] = 1 + postsynaptic['AVG'][thisState]
        postsynaptic['LUAR'][nextState] = 1 + postsynaptic['LUAR'][thisState]
        postsynaptic['PVNL'][nextState] = 1 + postsynaptic['PVNL'][thisState]
        postsynaptic['PVPL'][nextState] = 4 + postsynaptic['PVPL'][thisState]

def PVCL():
        postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]
        postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 4 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 5 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 12 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 5 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 3 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['AVJL'][nextState] = 4 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVJR'][nextState] = 2 + postsynaptic['AVJR'][thisState]
        postsynaptic['DA2'][nextState] = 1 + postsynaptic['DA2'][thisState]
        postsynaptic['DA5'][nextState] = 1 + postsynaptic['DA5'][thisState]
        postsynaptic['DA6'][nextState] = 1 + postsynaptic['DA6'][thisState]
        postsynaptic['DB2'][nextState] = 3 + postsynaptic['DB2'][thisState]
        postsynaptic['DB3'][nextState] = 4 + postsynaptic['DB3'][thisState]
        postsynaptic['DB4'][nextState] = 3 + postsynaptic['DB4'][thisState]
        postsynaptic['DB5'][nextState] = 2 + postsynaptic['DB5'][thisState]
        postsynaptic['DB6'][nextState] = 2 + postsynaptic['DB6'][thisState]
        postsynaptic['DB7'][nextState] = 3 + postsynaptic['DB7'][thisState]
        postsynaptic['DVA'][nextState] = 5 + postsynaptic['DVA'][thisState]
        postsynaptic['PLML'][nextState] = 1 + postsynaptic['PLML'][thisState]
        postsynaptic['PVCR'][nextState] = 7 + postsynaptic['PVCR'][thisState]
        postsynaptic['RID'][nextState] = 5 + postsynaptic['RID'][thisState]
        postsynaptic['RIS'][nextState] = 2 + postsynaptic['RIS'][thisState]
        postsynaptic['SIBVL'][nextState] = 2 + postsynaptic['SIBVL'][thisState]
        postsynaptic['VB10'][nextState] = 3 + postsynaptic['VB10'][thisState]
        postsynaptic['VB11'][nextState] = 1 + postsynaptic['VB11'][thisState]
        postsynaptic['VB3'][nextState] = 1 + postsynaptic['VB3'][thisState]
        postsynaptic['VB4'][nextState] = 1 + postsynaptic['VB4'][thisState]
        postsynaptic['VB5'][nextState] = 1 + postsynaptic['VB5'][thisState]
        postsynaptic['VB6'][nextState] = 2 + postsynaptic['VB6'][thisState]
        postsynaptic['VB8'][nextState] = 1 + postsynaptic['VB8'][thisState]
        postsynaptic['VB9'][nextState] = 2 + postsynaptic['VB9'][thisState]

def PVCR():
        postsynaptic['AQR'][nextState] = 1 + postsynaptic['AQR'][thisState]
        postsynaptic['AS2'][nextState] = 1 + postsynaptic['AS2'][thisState]
        postsynaptic['AVAL'][nextState] = 12 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 10 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 8 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 6 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 5 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['AVJL'][nextState] = 3 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVL'][nextState] = 1 + postsynaptic['AVL'][thisState]
        postsynaptic['DA9'][nextState] = 1 + postsynaptic['DA9'][thisState]
        postsynaptic['DB2'][nextState] = 1 + postsynaptic['DB2'][thisState]
        postsynaptic['DB3'][nextState] = 3 + postsynaptic['DB3'][thisState]
        postsynaptic['DB4'][nextState] = 4 + postsynaptic['DB4'][thisState]
        postsynaptic['DB5'][nextState] = 1 + postsynaptic['DB5'][thisState]
        postsynaptic['DB6'][nextState] = 2 + postsynaptic['DB6'][thisState]
        postsynaptic['DB7'][nextState] = 1 + postsynaptic['DB7'][thisState]
        postsynaptic['FLPL'][nextState] = 1 + postsynaptic['FLPL'][thisState]
        postsynaptic['LUAR'][nextState] = 1 + postsynaptic['LUAR'][thisState]
        postsynaptic['PDEL'][nextState] = 2 + postsynaptic['PDEL'][thisState]
        postsynaptic['PHCR'][nextState] = 1 + postsynaptic['PHCR'][thisState]
        postsynaptic['PLMR'][nextState] = 1 + postsynaptic['PLMR'][thisState]
        postsynaptic['PVCL'][nextState] = 8 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVDL'][nextState] = 1 + postsynaptic['PVDL'][thisState]
        postsynaptic['PVR'][nextState] = 1 + postsynaptic['PVR'][thisState]
        postsynaptic['PVWL'][nextState] = 2 + postsynaptic['PVWL'][thisState]
        postsynaptic['PVWR'][nextState] = 2 + postsynaptic['PVWR'][thisState]
        postsynaptic['RID'][nextState] = 5 + postsynaptic['RID'][thisState]
        postsynaptic['SIBVR'][nextState] = 2 + postsynaptic['SIBVR'][thisState]
        postsynaptic['VA8'][nextState] = 2 + postsynaptic['VA8'][thisState]
        postsynaptic['VA9'][nextState] = 1 + postsynaptic['VA9'][thisState]
        postsynaptic['VB10'][nextState] = 1 + postsynaptic['VB10'][thisState]
        postsynaptic['VB4'][nextState] = 3 + postsynaptic['VB4'][thisState]
        postsynaptic['VB6'][nextState] = 2 + postsynaptic['VB6'][thisState]
        postsynaptic['VB7'][nextState] = 3 + postsynaptic['VB7'][thisState]
        postsynaptic['VB8'][nextState] = 1 + postsynaptic['VB8'][thisState]

def PVDL():
        postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 6 + postsynaptic['AVAR'][thisState]
        postsynaptic['DD5'][nextState] = 1 + postsynaptic['DD5'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 6 + postsynaptic['PVCR'][thisState]
        postsynaptic['VD10'][nextState] = 6 + postsynaptic['VD10'][thisState]

def PVDR():
        postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 9 + postsynaptic['AVAR'][thisState]
        postsynaptic['DVA'][nextState] = 3 + postsynaptic['DVA'][thisState]
        postsynaptic['PVCL'][nextState] = 13 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 10 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVDL'][nextState] = 1 + postsynaptic['PVDL'][thisState]
        postsynaptic['VA9'][nextState] = 1 + postsynaptic['VA9'][thisState]

def PVM():
        postsynaptic['AVKL'][nextState] = 11 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVL'][nextState] = 1 + postsynaptic['AVL'][thisState]
        postsynaptic['AVM'][nextState] = 1 + postsynaptic['AVM'][thisState]
        postsynaptic['DVA'][nextState] = 3 + postsynaptic['DVA'][thisState]
        postsynaptic['PDEL'][nextState] = 7 + postsynaptic['PDEL'][thisState]
        postsynaptic['PDEL'][nextState] = 1 + postsynaptic['PDEL'][thisState]
        postsynaptic['PDER'][nextState] = 8 + postsynaptic['PDER'][thisState]
        postsynaptic['PDER'][nextState] = 1 + postsynaptic['PDER'][thisState]
        postsynaptic['PVCL'][nextState] = 2 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVR'][nextState] = 1 + postsynaptic['PVR'][thisState]

def PVNL():
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVBR'][nextState] = 3 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 3 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVDR'][nextState] = 3 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVFR'][nextState] = 1 + postsynaptic['AVFR'][thisState]
        postsynaptic['AVG'][nextState] = 1 + postsynaptic['AVG'][thisState]
        postsynaptic['AVJL'][nextState] = 5 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVJR'][nextState] = 5 + postsynaptic['AVJR'][thisState]
        postsynaptic['AVL'][nextState] = 2 + postsynaptic['AVL'][thisState]
        postsynaptic['BDUL'][nextState] = 1 + postsynaptic['BDUL'][thisState]
        postsynaptic['BDUR'][nextState] = 2 + postsynaptic['BDUR'][thisState]
        postsynaptic['DD1'][nextState] = 2 + postsynaptic['DD1'][thisState]
        postsynaptic['MVL09'][nextState] = 3 + postsynaptic['MVL09'][thisState]
        postsynaptic['PQR'][nextState] = 1 + postsynaptic['PQR'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVNR'][nextState] = 5 + postsynaptic['PVNR'][thisState]
        postsynaptic['PVQR'][nextState] = 1 + postsynaptic['PVQR'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['PVWL'][nextState] = 1 + postsynaptic['PVWL'][thisState]
        postsynaptic['RIFL'][nextState] = 1 + postsynaptic['RIFL'][thisState]

def PVNR():
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 3 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVJL'][nextState] = 4 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVJR'][nextState] = 1 + postsynaptic['AVJR'][thisState]
        postsynaptic['AVL'][nextState] = 2 + postsynaptic['AVL'][thisState]
        postsynaptic['BDUL'][nextState] = 1 + postsynaptic['BDUL'][thisState]
        postsynaptic['BDUR'][nextState] = 2 + postsynaptic['BDUR'][thisState]
        postsynaptic['DD3'][nextState] = 1 + postsynaptic['DD3'][thisState]
        postsynaptic['HSNR'][nextState] = 2 + postsynaptic['HSNR'][thisState]
        postsynaptic['MVL12'][nextState] = 1 + postsynaptic['MVL12'][thisState]
        postsynaptic['MVL13'][nextState] = 2 + postsynaptic['MVL13'][thisState]
        postsynaptic['PQR'][nextState] = 2 + postsynaptic['PQR'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVNL'][nextState] = 1 + postsynaptic['PVNL'][thisState]
        postsynaptic['PVT'][nextState] = 2 + postsynaptic['PVT'][thisState]
        postsynaptic['PVWL'][nextState] = 2 + postsynaptic['PVWL'][thisState]
        postsynaptic['VC2'][nextState] = 1 + postsynaptic['VC2'][thisState]
        postsynaptic['VC3'][nextState] = 1 + postsynaptic['VC3'][thisState]
        postsynaptic['VD12'][nextState] = 1 + postsynaptic['VD12'][thisState]
        postsynaptic['VD6'][nextState] = 1 + postsynaptic['VD6'][thisState]
        postsynaptic['VD7'][nextState] = 1 + postsynaptic['VD7'][thisState]

def PVPL():
        postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
        postsynaptic['AQR'][nextState] = 8 + postsynaptic['AQR'][thisState]
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 5 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 6 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['AVHR'][nextState] = 1 + postsynaptic['AVHR'][thisState]
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 6 + postsynaptic['AVKR'][thisState]
        postsynaptic['DVC'][nextState] = 2 + postsynaptic['DVC'][thisState]
        postsynaptic['PHAR'][nextState] = 3 + postsynaptic['PHAR'][thisState]
        postsynaptic['PQR'][nextState] = 4 + postsynaptic['PQR'][thisState]
        postsynaptic['PVCR'][nextState] = 3 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVPR'][nextState] = 1 + postsynaptic['PVPR'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['RIGL'][nextState] = 2 + postsynaptic['RIGL'][thisState]
        postsynaptic['VD13'][nextState] = 2 + postsynaptic['VD13'][thisState]
        postsynaptic['VD3'][nextState] = 1 + postsynaptic['VD3'][thisState]

def PVPR():
        postsynaptic['ADFR'][nextState] = 1 + postsynaptic['ADFR'][thisState]
        postsynaptic['AQR'][nextState] = 11 + postsynaptic['AQR'][thisState]
        postsynaptic['ASHR'][nextState] = 1 + postsynaptic['ASHR'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 4 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 5 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVHL'][nextState] = 3 + postsynaptic['AVHL'][thisState]
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVL'][nextState] = 4 + postsynaptic['AVL'][thisState]
        postsynaptic['DD2'][nextState] = 1 + postsynaptic['DD2'][thisState]
        postsynaptic['DVC'][nextState] = 14 + postsynaptic['DVC'][thisState]
        postsynaptic['PVCL'][nextState] = 4 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 7 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVPL'][nextState] = 1 + postsynaptic['PVPL'][thisState]
        postsynaptic['PVQR'][nextState] = 1 + postsynaptic['PVQR'][thisState]
        postsynaptic['RIAR'][nextState] = 2 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIMR'][nextState] = 1 + postsynaptic['RIMR'][thisState]
        postsynaptic['RMGR'][nextState] = 1 + postsynaptic['RMGR'][thisState]
        postsynaptic['VD4'][nextState] = 1 + postsynaptic['VD4'][thisState]
        postsynaptic['VD5'][nextState] = 1 + postsynaptic['VD5'][thisState]

def PVQL():
        postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
        postsynaptic['AIAL'][nextState] = 3 + postsynaptic['AIAL'][thisState]
        postsynaptic['ASJL'][nextState] = 1 + postsynaptic['ASJL'][thisState]
        postsynaptic['ASKL'][nextState] = 4 + postsynaptic['ASKL'][thisState]
        postsynaptic['ASKL'][nextState] = 5 + postsynaptic['ASKL'][thisState]
        postsynaptic['HSNL'][nextState] = 2 + postsynaptic['HSNL'][thisState]
        postsynaptic['PVQR'][nextState] = 2 + postsynaptic['PVQR'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]

def PVQR():
        postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]
        postsynaptic['AIAR'][nextState] = 7 + postsynaptic['AIAR'][thisState]
        postsynaptic['ASER'][nextState] = 1 + postsynaptic['ASER'][thisState]
        postsynaptic['ASKR'][nextState] = 8 + postsynaptic['ASKR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVFL'][nextState] = 1 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVFR'][nextState] = 1 + postsynaptic['AVFR'][thisState]
        postsynaptic['AVL'][nextState] = 1 + postsynaptic['AVL'][thisState]
        postsynaptic['AWAR'][nextState] = 2 + postsynaptic['AWAR'][thisState]
        postsynaptic['DD1'][nextState] = 1 + postsynaptic['DD1'][thisState]
        postsynaptic['DVC'][nextState] = 1 + postsynaptic['DVC'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['PVNL'][nextState] = 1 + postsynaptic['PVNL'][thisState]
        postsynaptic['PVQL'][nextState] = 1 + postsynaptic['PVQL'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['RIFR'][nextState] = 1 + postsynaptic['RIFR'][thisState]
        postsynaptic['VD1'][nextState] = 1 + postsynaptic['VD1'][thisState]

def PVR():
        postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
        postsynaptic['ALML'][nextState] = 1 + postsynaptic['ALML'][thisState]
        postsynaptic['AS6'][nextState] = 1 + postsynaptic['AS6'][thisState]
        postsynaptic['AVBL'][nextState] = 4 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 4 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVJL'][nextState] = 3 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVJR'][nextState] = 2 + postsynaptic['AVJR'][thisState]
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['DA9'][nextState] = 1 + postsynaptic['DA9'][thisState]
        postsynaptic['DB2'][nextState] = 1 + postsynaptic['DB2'][thisState]
        postsynaptic['DB3'][nextState] = 1 + postsynaptic['DB3'][thisState]
        postsynaptic['DVA'][nextState] = 3 + postsynaptic['DVA'][thisState]
        postsynaptic['IL1DL'][nextState] = 1 + postsynaptic['IL1DL'][thisState]
        postsynaptic['IL1DR'][nextState] = 1 + postsynaptic['IL1DR'][thisState]
        postsynaptic['IL1VL'][nextState] = 1 + postsynaptic['IL1VL'][thisState]
        postsynaptic['IL1VR'][nextState] = 1 + postsynaptic['IL1VR'][thisState]
        postsynaptic['LUAL'][nextState] = 1 + postsynaptic['LUAL'][thisState]
        postsynaptic['LUAR'][nextState] = 1 + postsynaptic['LUAR'][thisState]
        postsynaptic['PDEL'][nextState] = 1 + postsynaptic['PDEL'][thisState]
        postsynaptic['PDER'][nextState] = 1 + postsynaptic['PDER'][thisState]
        postsynaptic['PLMR'][nextState] = 2 + postsynaptic['PLMR'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['RIPL'][nextState] = 3 + postsynaptic['RIPL'][thisState]
        postsynaptic['RIPR'][nextState] = 3 + postsynaptic['RIPR'][thisState]
        postsynaptic['SABD'][nextState] = 1 + postsynaptic['SABD'][thisState]
        postsynaptic['URADL'][nextState] = 1 + postsynaptic['URADL'][thisState]

def PVT():
        postsynaptic['AIBL'][nextState] = 3 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBR'][nextState] = 5 + postsynaptic['AIBR'][thisState]
        postsynaptic['AVKL'][nextState] = 9 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 7 + postsynaptic['AVKR'][thisState]
        postsynaptic['AVL'][nextState] = 2 + postsynaptic['AVL'][thisState]
        postsynaptic['DVC'][nextState] = 2 + postsynaptic['DVC'][thisState]
        postsynaptic['PVPL'][nextState] = 1 + postsynaptic['PVPL'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIGL'][nextState] = 2 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIGR'][nextState] = 3 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]
        postsynaptic['RMFL'][nextState] = 2 + postsynaptic['RMFL'][thisState]
        postsynaptic['RMFR'][nextState] = 3 + postsynaptic['RMFR'][thisState]
        postsynaptic['SMBDR'][nextState] = 1 + postsynaptic['SMBDR'][thisState]

def PVWL():
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['PVCR'][nextState] = 2 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVT'][nextState] = 2 + postsynaptic['PVT'][thisState]
        postsynaptic['PVWR'][nextState] = 1 + postsynaptic['PVWR'][thisState]
        postsynaptic['VA12'][nextState] = 1 + postsynaptic['VA12'][thisState]


def PVWR():
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['PVCR'][nextState] = 2 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['VA12'][nextState] = 1 + postsynaptic['VA12'][thisState]

def RIAL():
        postsynaptic['CEPVL'][nextState] = 1 + postsynaptic['CEPVL'][thisState]
        postsynaptic['RIAR'][nextState] = 1 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIVL'][nextState] = 2 + postsynaptic['RIVL'][thisState]
        postsynaptic['RIVR'][nextState] = 4 + postsynaptic['RIVR'][thisState]
        postsynaptic['RMDDL'][nextState] = 12 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDDR'][nextState] = 7 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDL'][nextState] = 6 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDR'][nextState] = 6 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 9 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMDVR'][nextState] = 11 + postsynaptic['RMDVR'][thisState]
        postsynaptic['SIADL'][nextState] = 2 + postsynaptic['SIADL'][thisState]
        postsynaptic['SMDDL'][nextState] = 8 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDDR'][nextState] = 10 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVL'][nextState] = 6 + postsynaptic['SMDVL'][thisState]
        postsynaptic['SMDVR'][nextState] = 11 + postsynaptic['SMDVR'][thisState]

def RIAR():
        postsynaptic['CEPVR'][nextState] = 1 + postsynaptic['CEPVR'][thisState]
        postsynaptic['IL1R'][nextState] = 1 + postsynaptic['IL1R'][thisState]
        postsynaptic['RIAL'][nextState] = 4 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIVL'][nextState] = 1 + postsynaptic['RIVL'][thisState]
        postsynaptic['RMDDL'][nextState] = 10 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDDR'][nextState] = 11 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDL'][nextState] = 3 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDR'][nextState] = 8 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 12 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMDVR'][nextState] = 10 + postsynaptic['RMDVR'][thisState]
        postsynaptic['SAADR'][nextState] = 1 + postsynaptic['SAADR'][thisState]
        postsynaptic['SIADL'][nextState] = 1 + postsynaptic['SIADL'][thisState]
        postsynaptic['SIADR'][nextState] = 1 + postsynaptic['SIADR'][thisState]
        postsynaptic['SIAVL'][nextState] = 1 + postsynaptic['SIAVL'][thisState]
        postsynaptic['SMDDL'][nextState] = 7 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDDR'][nextState] = 7 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVL'][nextState] = 13 + postsynaptic['SMDVL'][thisState]
        postsynaptic['SMDVR'][nextState] = 7 + postsynaptic['SMDVR'][thisState]

def RIBL():
        postsynaptic['AIBR'][nextState] = 2 + postsynaptic['AIBR'][thisState]
        postsynaptic['AUAL'][nextState] = 1 + postsynaptic['AUAL'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 5 + postsynaptic['AVER'][thisState]
        postsynaptic['BAGR'][nextState] = 1 + postsynaptic['BAGR'][thisState]
        postsynaptic['OLQDL'][nextState] = 2 + postsynaptic['OLQDL'][thisState]
        postsynaptic['OLQVL'][nextState] = 1 + postsynaptic['OLQVL'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['RIAL'][nextState] = 3 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 3 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['SIADL'][nextState] = 1 + postsynaptic['SIADL'][thisState]
        postsynaptic['SIAVL'][nextState] = 1 + postsynaptic['SIAVL'][thisState]
        postsynaptic['SIBDL'][nextState] = 1 + postsynaptic['SIBDL'][thisState]
        postsynaptic['SIBVL'][nextState] = 1 + postsynaptic['SIBVL'][thisState]
        postsynaptic['SIBVR'][nextState] = 1 + postsynaptic['SIBVR'][thisState]
        postsynaptic['SMBDL'][nextState] = 1 + postsynaptic['SMBDL'][thisState]
        postsynaptic['SMDDL'][nextState] = 1 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDVR'][nextState] = 4 + postsynaptic['SMDVR'][thisState]

def RIBR():
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIZR'][nextState] = 1 + postsynaptic['AIZR'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVEL'][nextState] = 3 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['BAGL'][nextState] = 1 + postsynaptic['BAGL'][thisState]
        postsynaptic['OLQDR'][nextState] = 2 + postsynaptic['OLQDR'][thisState]
        postsynaptic['OLQVR'][nextState] = 1 + postsynaptic['OLQVR'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['RIAR'][nextState] = 2 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIBL'][nextState] = 3 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIGR'][nextState] = 2 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]
        postsynaptic['SIADR'][nextState] = 1 + postsynaptic['SIADR'][thisState]
        postsynaptic['SIAVR'][nextState] = 1 + postsynaptic['SIAVR'][thisState]
        postsynaptic['SIBDR'][nextState] = 1 + postsynaptic['SIBDR'][thisState]
        postsynaptic['SIBVR'][nextState] = 1 + postsynaptic['SIBVR'][thisState]
        postsynaptic['SMBDR'][nextState] = 1 + postsynaptic['SMBDR'][thisState]
        postsynaptic['SMDDL'][nextState] = 2 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDDR'][nextState] = 1 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVL'][nextState] = 2 + postsynaptic['SMDVL'][thisState]

def RICL():
        postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]
        postsynaptic['ASHL'][nextState] = 2 + postsynaptic['ASHL'][thisState]
        postsynaptic['AVAL'][nextState] = 5 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 6 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 2 + postsynaptic['AVKR'][thisState]
        postsynaptic['AWBR'][nextState] = 1 + postsynaptic['AWBR'][thisState]
        postsynaptic['RIML'][nextState] = 1 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 3 + postsynaptic['RIMR'][thisState]
        postsynaptic['RIVR'][nextState] = 1 + postsynaptic['RIVR'][thisState]
        postsynaptic['RMFR'][nextState] = 1 + postsynaptic['RMFR'][thisState]
        postsynaptic['SMBDL'][nextState] = 2 + postsynaptic['SMBDL'][thisState]
        postsynaptic['SMDDL'][nextState] = 3 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDDR'][nextState] = 3 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVR'][nextState] = 1 + postsynaptic['SMDVR'][thisState]

def RICR():
        postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]
        postsynaptic['ASHR'][nextState] = 2 + postsynaptic['ASHR'][thisState]
        postsynaptic['AVAL'][nextState] = 5 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 5 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['SMBDR'][nextState] = 1 + postsynaptic['SMBDR'][thisState]
        postsynaptic['SMDDL'][nextState] = 4 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDDR'][nextState] = 3 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVL'][nextState] = 2 + postsynaptic['SMDVL'][thisState]
        postsynaptic['SMDVR'][nextState] = 1 + postsynaptic['SMDVR'][thisState]

def RID():
        postsynaptic['ALA'][nextState] = 1 + postsynaptic['ALA'][thisState]
        postsynaptic['AS2'][nextState] = 1 + postsynaptic['AS2'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['DA6'][nextState] = 3 + postsynaptic['DA6'][thisState]
        postsynaptic['DA9'][nextState] = 1 + postsynaptic['DA9'][thisState]
        postsynaptic['DB1'][nextState] = 1 + postsynaptic['DB1'][thisState]
        postsynaptic['DD1'][nextState] = 4 + postsynaptic['DD1'][thisState]
        postsynaptic['DD2'][nextState] = 4 + postsynaptic['DD2'][thisState]
        postsynaptic['DD3'][nextState] = 3 + postsynaptic['DD3'][thisState]
        postsynaptic['MDL14'][nextState] = -2 + postsynaptic['MDL14'][thisState]
        postsynaptic['MDL21'][nextState] = -3 + postsynaptic['MDL21'][thisState]
        postsynaptic['PDB'][nextState] = 2 + postsynaptic['PDB'][thisState]
        postsynaptic['VD13'][nextState] = 1 + postsynaptic['VD13'][thisState]
        postsynaptic['VD5'][nextState] = 1 + postsynaptic['VD5'][thisState]

def RIFL():
        postsynaptic['ALML'][nextState] = 2 + postsynaptic['ALML'][thisState]
        postsynaptic['AVBL'][nextState] = 10 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVG'][nextState] = 1 + postsynaptic['AVG'][thisState]
        postsynaptic['AVHR'][nextState] = 1 + postsynaptic['AVHR'][thisState]
        postsynaptic['AVJR'][nextState] = 2 + postsynaptic['AVJR'][thisState]
        postsynaptic['PVPL'][nextState] = 3 + postsynaptic['PVPL'][thisState]
        postsynaptic['RIML'][nextState] = 4 + postsynaptic['RIML'][thisState]
        postsynaptic['VD1'][nextState] = 1 + postsynaptic['VD1'][thisState]

def RIFR():
        postsynaptic['ASHR'][nextState] = 2 + postsynaptic['ASHR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 17 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVFL'][nextState] = 1 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVG'][nextState] = 1 + postsynaptic['AVG'][thisState]
        postsynaptic['AVHL'][nextState] = 1 + postsynaptic['AVHL'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVJR'][nextState] = 2 + postsynaptic['AVJR'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVPR'][nextState] = 4 + postsynaptic['PVPR'][thisState]
        postsynaptic['RIMR'][nextState] = 4 + postsynaptic['RIMR'][thisState]
        postsynaptic['RIPR'][nextState] = 1 + postsynaptic['RIPR'][thisState]

def RIGL():
        postsynaptic['AIBR'][nextState] = 3 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIZR'][nextState] = 1 + postsynaptic['AIZR'][thisState]
        postsynaptic['ALNL'][nextState] = 1 + postsynaptic['ALNL'][thisState]
        postsynaptic['AQR'][nextState] = 2 + postsynaptic['AQR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 2 + postsynaptic['AVKR'][thisState]
        postsynaptic['BAGR'][nextState] = 2 + postsynaptic['BAGR'][thisState]
        postsynaptic['DVC'][nextState] = 1 + postsynaptic['DVC'][thisState]
        postsynaptic['OLLL'][nextState] = 1 + postsynaptic['OLLL'][thisState]
        postsynaptic['OLQDL'][nextState] = 1 + postsynaptic['OLQDL'][thisState]
        postsynaptic['OLQVL'][nextState] = 1 + postsynaptic['OLQVL'][thisState]
        postsynaptic['RIBL'][nextState] = 2 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIGR'][nextState] = 3 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIR'][nextState] = 2 + postsynaptic['RIR'][thisState]
        postsynaptic['RMEL'][nextState] = 2 + postsynaptic['RMEL'][thisState]
        postsynaptic['RMHR'][nextState] = 3 + postsynaptic['RMHR'][thisState]
        postsynaptic['URYDL'][nextState] = 1 + postsynaptic['URYDL'][thisState]
        postsynaptic['URYVL'][nextState] = 1 + postsynaptic['URYVL'][thisState]
        postsynaptic['VB2'][nextState] = 1 + postsynaptic['VB2'][thisState]
        postsynaptic['VD1'][nextState] = 2 + postsynaptic['VD1'][thisState]

def RIGR():
        postsynaptic['AIBL'][nextState] = 3 + postsynaptic['AIBL'][thisState]
        postsynaptic['ALNR'][nextState] = 1 + postsynaptic['ALNR'][thisState]
        postsynaptic['AQR'][nextState] = 1 + postsynaptic['AQR'][thisState]
        postsynaptic['AVER'][nextState] = 2 + postsynaptic['AVER'][thisState]
        postsynaptic['AVKL'][nextState] = 4 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 2 + postsynaptic['AVKR'][thisState]
        postsynaptic['BAGL'][nextState] = 1 + postsynaptic['BAGL'][thisState]
        postsynaptic['OLLR'][nextState] = 1 + postsynaptic['OLLR'][thisState]
        postsynaptic['OLQDR'][nextState] = 1 + postsynaptic['OLQDR'][thisState]
        postsynaptic['OLQVR'][nextState] = 1 + postsynaptic['OLQVR'][thisState]
        postsynaptic['RIBR'][nextState] = 2 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIGL'][nextState] = 3 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIR'][nextState] = 1 + postsynaptic['RIR'][thisState]
        postsynaptic['RMHL'][nextState] = 4 + postsynaptic['RMHL'][thisState]
        postsynaptic['URYDR'][nextState] = 1 + postsynaptic['URYDR'][thisState]
        postsynaptic['URYVR'][nextState] = 1 + postsynaptic['URYVR'][thisState]

def RIH():
        postsynaptic['ADFR'][nextState] = 1 + postsynaptic['ADFR'][thisState]
        postsynaptic['AIZL'][nextState] = 4 + postsynaptic['AIZL'][thisState]
        postsynaptic['AIZR'][nextState] = 4 + postsynaptic['AIZR'][thisState]
        postsynaptic['AUAR'][nextState] = 1 + postsynaptic['AUAR'][thisState]
        postsynaptic['BAGR'][nextState] = 1 + postsynaptic['BAGR'][thisState]
        postsynaptic['CEPDL'][nextState] = 2 + postsynaptic['CEPDL'][thisState]
        postsynaptic['CEPDR'][nextState] = 2 + postsynaptic['CEPDR'][thisState]
        postsynaptic['CEPVL'][nextState] = 2 + postsynaptic['CEPVL'][thisState]
        postsynaptic['CEPVR'][nextState] = 2 + postsynaptic['CEPVR'][thisState]
        postsynaptic['FLPL'][nextState] = 1 + postsynaptic['FLPL'][thisState]
        postsynaptic['IL2L'][nextState] = 2 + postsynaptic['IL2L'][thisState]
        postsynaptic['IL2R'][nextState] = 1 + postsynaptic['IL2R'][thisState]
        postsynaptic['OLQDL'][nextState] = 4 + postsynaptic['OLQDL'][thisState]
        postsynaptic['OLQDR'][nextState] = 2 + postsynaptic['OLQDR'][thisState]
        postsynaptic['OLQVL'][nextState] = 1 + postsynaptic['OLQVL'][thisState]
        postsynaptic['OLQVR'][nextState] = 6 + postsynaptic['OLQVR'][thisState]
        postsynaptic['RIAL'][nextState] = 10 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 8 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIBL'][nextState] = 5 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 4 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIPL'][nextState] = 4 + postsynaptic['RIPL'][thisState]
        postsynaptic['RIPR'][nextState] = 6 + postsynaptic['RIPR'][thisState]
        postsynaptic['RMER'][nextState] = 2 + postsynaptic['RMER'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]
        postsynaptic['URYVR'][nextState] = 1 + postsynaptic['URYVR'][thisState]

def RIML():
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['AIYL'][nextState] = 1 + postsynaptic['AIYL'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 3 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVEL'][nextState] = 2 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 3 + postsynaptic['AVER'][thisState]
        postsynaptic['MDR05'][nextState] = 2 + postsynaptic['MDR05'][thisState]
        postsynaptic['MVR05'][nextState] = 2 + postsynaptic['MVR05'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIS'][nextState] = 1 + postsynaptic['RIS'][thisState]
        postsynaptic['RMDL'][nextState] = 1 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDR'][nextState] = 1 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMFR'][nextState] = 1 + postsynaptic['RMFR'][thisState]
        postsynaptic['SAADR'][nextState] = 1 + postsynaptic['SAADR'][thisState]
        postsynaptic['SAAVL'][nextState] = 3 + postsynaptic['SAAVL'][thisState]
        postsynaptic['SAAVR'][nextState] = 2 + postsynaptic['SAAVR'][thisState]
        postsynaptic['SMDDR'][nextState] = 5 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVL'][nextState] = 1 + postsynaptic['SMDVL'][thisState]

def RIMR():
        postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]
        postsynaptic['AIBL'][nextState] = 4 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['AIYR'][nextState] = 1 + postsynaptic['AIYR'][thisState]
        postsynaptic['AVAL'][nextState] = 5 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 5 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVEL'][nextState] = 3 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 2 + postsynaptic['AVER'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['MDL05'][nextState] = 1 + postsynaptic['MDL05'][thisState]
        postsynaptic['MDL07'][nextState] = 1 + postsynaptic['MDL07'][thisState]
        postsynaptic['MVL05'][nextState] = 1 + postsynaptic['MVL05'][thisState]
        postsynaptic['MVL07'][nextState] = 1 + postsynaptic['MVL07'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIS'][nextState] = 2 + postsynaptic['RIS'][thisState]
        postsynaptic['RMDL'][nextState] = 1 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDR'][nextState] = 1 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMFL'][nextState] = 1 + postsynaptic['RMFL'][thisState]
        postsynaptic['RMFR'][nextState] = 1 + postsynaptic['RMFR'][thisState]
        postsynaptic['SAAVL'][nextState] = 3 + postsynaptic['SAAVL'][thisState]
        postsynaptic['SAAVR'][nextState] = 3 + postsynaptic['SAAVR'][thisState]
        postsynaptic['SMDDL'][nextState] = 2 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDDR'][nextState] = 4 + postsynaptic['SMDDR'][thisState]

def RIPL():
        postsynaptic['OLQDL'][nextState] = 1 + postsynaptic['OLQDL'][thisState]
        postsynaptic['OLQDR'][nextState] = 1 + postsynaptic['OLQDR'][thisState]
        postsynaptic['RMED'][nextState] = 1 + postsynaptic['RMED'][thisState]

def RIPR():
        postsynaptic['OLQDL'][nextState] = 1 + postsynaptic['OLQDL'][thisState]
        postsynaptic['OLQDR'][nextState] = 1 + postsynaptic['OLQDR'][thisState]
        postsynaptic['RMED'][nextState] = 1 + postsynaptic['RMED'][thisState]

def RIR():
        postsynaptic['AFDR'][nextState] = 1 + postsynaptic['AFDR'][thisState]
        postsynaptic['AIZL'][nextState] = 3 + postsynaptic['AIZL'][thisState]
        postsynaptic['AIZR'][nextState] = 5 + postsynaptic['AIZR'][thisState]
        postsynaptic['AUAL'][nextState] = 1 + postsynaptic['AUAL'][thisState]
        postsynaptic['AWBR'][nextState] = 1 + postsynaptic['AWBR'][thisState]
        postsynaptic['BAGL'][nextState] = 1 + postsynaptic['BAGL'][thisState]
        postsynaptic['BAGR'][nextState] = 2 + postsynaptic['BAGR'][thisState]
        postsynaptic['DVA'][nextState] = 2 + postsynaptic['DVA'][thisState]
        postsynaptic['HSNL'][nextState] = 1 + postsynaptic['HSNL'][thisState]
        postsynaptic['PVPL'][nextState] = 1 + postsynaptic['PVPL'][thisState]
        postsynaptic['RIAL'][nextState] = 5 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 1 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['URXL'][nextState] = 5 + postsynaptic['URXL'][thisState]
        postsynaptic['URXR'][nextState] = 1 + postsynaptic['URXR'][thisState]

def RIS():
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['AVEL'][nextState] = 7 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 7 + postsynaptic['AVER'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 4 + postsynaptic['AVKR'][thisState]
        postsynaptic['AVL'][nextState] = 2 + postsynaptic['AVL'][thisState]
        postsynaptic['CEPDR'][nextState] = 1 + postsynaptic['CEPDR'][thisState]
        postsynaptic['CEPVL'][nextState] = 2 + postsynaptic['CEPVL'][thisState]
        postsynaptic['CEPVR'][nextState] = 1 + postsynaptic['CEPVR'][thisState]
        postsynaptic['DB1'][nextState] = 1 + postsynaptic['DB1'][thisState]
        postsynaptic['OLLR'][nextState] = 1 + postsynaptic['OLLR'][thisState]
        postsynaptic['RIBL'][nextState] = 3 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 5 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIML'][nextState] = 2 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 5 + postsynaptic['RIMR'][thisState]
        postsynaptic['RMDDL'][nextState] = 1 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDL'][nextState] = 2 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDR'][nextState] = 4 + postsynaptic['RMDR'][thisState]
        postsynaptic['SMDDL'][nextState] = 1 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDDR'][nextState] = 3 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVL'][nextState] = 1 + postsynaptic['SMDVL'][thisState]
        postsynaptic['SMDVR'][nextState] = 1 + postsynaptic['SMDVR'][thisState]
        postsynaptic['URYVR'][nextState] = 1 + postsynaptic['URYVR'][thisState]

def RIVL():
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['MVR05'][nextState] = -2 + postsynaptic['MVR05'][thisState]
        postsynaptic['MVR06'][nextState] = -2 + postsynaptic['MVR06'][thisState]
        postsynaptic['MVR08'][nextState] = -3 + postsynaptic['MVR08'][thisState]
        postsynaptic['RIAL'][nextState] = 1 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 1 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIVR'][nextState] = 2 + postsynaptic['RIVR'][thisState]
        postsynaptic['RMDL'][nextState] = 2 + postsynaptic['RMDL'][thisState]
        postsynaptic['SAADR'][nextState] = 3 + postsynaptic['SAADR'][thisState]
        postsynaptic['SDQR'][nextState] = 2 + postsynaptic['SDQR'][thisState]
        postsynaptic['SIAVR'][nextState] = 2 + postsynaptic['SIAVR'][thisState]
        postsynaptic['SMDDR'][nextState] = 1 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVL'][nextState] = 1 + postsynaptic['SMDVL'][thisState]

def RIVR():
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['MVL05'][nextState] = -2 + postsynaptic['MVL05'][thisState]
        postsynaptic['MVL06'][nextState] = -2 + postsynaptic['MVL06'][thisState]
        postsynaptic['MVL08'][nextState] = -2 + postsynaptic['MVL08'][thisState]
        postsynaptic['MVR04'][nextState] = -2 + postsynaptic['MVR04'][thisState]
        postsynaptic['MVR06'][nextState] = -2 + postsynaptic['MVR06'][thisState]
        postsynaptic['RIAL'][nextState] = 2 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 1 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIVL'][nextState] = 2 + postsynaptic['RIVL'][thisState]
        postsynaptic['RMDDL'][nextState] = 1 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDR'][nextState] = 1 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMDVR'][nextState] = 1 + postsynaptic['RMDVR'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]
        postsynaptic['SAADL'][nextState] = 2 + postsynaptic['SAADL'][thisState]
        postsynaptic['SDQR'][nextState] = 2 + postsynaptic['SDQR'][thisState]
        postsynaptic['SIAVL'][nextState] = 2 + postsynaptic['SIAVL'][thisState]
        postsynaptic['SMDDL'][nextState] = 2 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDVR'][nextState] = 4 + postsynaptic['SMDVR'][thisState]

def RMDDL():
        postsynaptic['MDR01'][nextState] = 1 + postsynaptic['MDR01'][thisState]
        postsynaptic['MDR02'][nextState] = 1 + postsynaptic['MDR02'][thisState]
        postsynaptic['MDR03'][nextState] = 1 + postsynaptic['MDR03'][thisState]
        postsynaptic['MDR04'][nextState] = 1 + postsynaptic['MDR04'][thisState]
        postsynaptic['MDR08'][nextState] = 2 + postsynaptic['MDR08'][thisState]
        postsynaptic['MVR01'][nextState] = 1 + postsynaptic['MVR01'][thisState]
        postsynaptic['OLQVL'][nextState] = 1 + postsynaptic['OLQVL'][thisState]
        postsynaptic['RMDL'][nextState] = 1 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDVL'][nextState] = 1 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMDVR'][nextState] = 7 + postsynaptic['RMDVR'][thisState]
        postsynaptic['SMDDL'][nextState] = 1 + postsynaptic['SMDDL'][thisState]

def RMDDR():
        postsynaptic['MDL01'][nextState] = 1 + postsynaptic['MDL01'][thisState]
        postsynaptic['MDL02'][nextState] = 1 + postsynaptic['MDL02'][thisState]
        postsynaptic['MDL03'][nextState] = 2 + postsynaptic['MDL03'][thisState]
        postsynaptic['MDL04'][nextState] = 1 + postsynaptic['MDL04'][thisState]
        postsynaptic['MDR04'][nextState] = 1 + postsynaptic['MDR04'][thisState]
        postsynaptic['MVR01'][nextState] = 1 + postsynaptic['MVR01'][thisState]
        postsynaptic['MVR02'][nextState] = 1 + postsynaptic['MVR02'][thisState]
        postsynaptic['OLQVR'][nextState] = 1 + postsynaptic['OLQVR'][thisState]
        postsynaptic['RMDVL'][nextState] = 12 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMDVR'][nextState] = 1 + postsynaptic['RMDVR'][thisState]
        postsynaptic['SAADR'][nextState] = 1 + postsynaptic['SAADR'][thisState]
        postsynaptic['SMDDR'][nextState] = 1 + postsynaptic['SMDDR'][thisState]
        postsynaptic['URYDL'][nextState] = 1 + postsynaptic['URYDL'][thisState]

def RMDL():
        postsynaptic['MDL03'][nextState] = 1 + postsynaptic['MDL03'][thisState]
        postsynaptic['MDL05'][nextState] = 2 + postsynaptic['MDL05'][thisState]
        postsynaptic['MDR01'][nextState] = 1 + postsynaptic['MDR01'][thisState]
        postsynaptic['MDR03'][nextState] = 1 + postsynaptic['MDR03'][thisState]
        postsynaptic['MVL01'][nextState] = 1 + postsynaptic['MVL01'][thisState]
        postsynaptic['MVR01'][nextState] = 1 + postsynaptic['MVR01'][thisState]
        postsynaptic['MVR03'][nextState] = 1 + postsynaptic['MVR03'][thisState]
        postsynaptic['MVR05'][nextState] = 2 + postsynaptic['MVR05'][thisState]
        postsynaptic['MVR07'][nextState] = 1 + postsynaptic['MVR07'][thisState]
        postsynaptic['OLLR'][nextState] = 2 + postsynaptic['OLLR'][thisState]
        postsynaptic['RIAL'][nextState] = 4 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 3 + postsynaptic['RIAR'][thisState]
        postsynaptic['RMDDL'][nextState] = 1 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDDR'][nextState] = 1 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDR'][nextState] = 3 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 1 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMER'][nextState] = 1 + postsynaptic['RMER'][thisState]
        postsynaptic['RMFL'][nextState] = 1 + postsynaptic['RMFL'][thisState]

def RMDR():
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['MDL03'][nextState] = 1 + postsynaptic['MDL03'][thisState]
        postsynaptic['MDL05'][nextState] = 1 + postsynaptic['MDL05'][thisState]
        postsynaptic['MDR05'][nextState] = 1 + postsynaptic['MDR05'][thisState]
        postsynaptic['MVL03'][nextState] = 1 + postsynaptic['MVL03'][thisState]
        postsynaptic['MVL05'][nextState] = 1 + postsynaptic['MVL05'][thisState]
        postsynaptic['RIAL'][nextState] = 3 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 7 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIMR'][nextState] = 2 + postsynaptic['RIMR'][thisState]
        postsynaptic['RIS'][nextState] = 1 + postsynaptic['RIS'][thisState]
        postsynaptic['RMDDL'][nextState] = 1 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDL'][nextState] = 1 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDVR'][nextState] = 1 + postsynaptic['RMDVR'][thisState]

def RMDVL():
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['MDR01'][nextState] = 1 + postsynaptic['MDR01'][thisState]
        postsynaptic['MVL04'][nextState] = 1 + postsynaptic['MVL04'][thisState]
        postsynaptic['MVR01'][nextState] = 1 + postsynaptic['MVR01'][thisState]
        postsynaptic['MVR02'][nextState] = 1 + postsynaptic['MVR02'][thisState]
        postsynaptic['MVR03'][nextState] = 1 + postsynaptic['MVR03'][thisState]
        postsynaptic['MVR04'][nextState] = 1 + postsynaptic['MVR04'][thisState]
        postsynaptic['MVR05'][nextState] = 1 + postsynaptic['MVR05'][thisState]
        postsynaptic['MVR06'][nextState] = 1 + postsynaptic['MVR06'][thisState]
        postsynaptic['MVR08'][nextState] = 1 + postsynaptic['MVR08'][thisState]
        postsynaptic['OLQDL'][nextState] = 1 + postsynaptic['OLQDL'][thisState]
        postsynaptic['RMDDL'][nextState] = 1 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDDR'][nextState] = 6 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDL'][nextState] = 1 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDVR'][nextState] = 1 + postsynaptic['RMDVR'][thisState]
        postsynaptic['SAAVL'][nextState] = 1 + postsynaptic['SAAVL'][thisState]
        postsynaptic['SMDVL'][nextState] = 1 + postsynaptic['SMDVL'][thisState]

def RMDVR():
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['MDL01'][nextState] = 1 + postsynaptic['MDL01'][thisState]
        postsynaptic['MVL01'][nextState] = 1 + postsynaptic['MVL01'][thisState]
        postsynaptic['MVL02'][nextState] = 1 + postsynaptic['MVL02'][thisState]
        postsynaptic['MVL03'][nextState] = 1 + postsynaptic['MVL03'][thisState]
        postsynaptic['MVL04'][nextState] = 1 + postsynaptic['MVL04'][thisState]
        postsynaptic['MVL05'][nextState] = 1 + postsynaptic['MVL05'][thisState]
        postsynaptic['MVL06'][nextState] = 1 + postsynaptic['MVL06'][thisState]
        postsynaptic['MVL08'][nextState] = 1 + postsynaptic['MVL08'][thisState]
        postsynaptic['MVR04'][nextState] = 1 + postsynaptic['MVR04'][thisState]
        postsynaptic['MVR06'][nextState] = 1 + postsynaptic['MVR06'][thisState]
        postsynaptic['MVR08'][nextState] = 1 + postsynaptic['MVR08'][thisState]
        postsynaptic['OLQDR'][nextState] = 1 + postsynaptic['OLQDR'][thisState]
        postsynaptic['RMDDL'][nextState] = 4 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDDR'][nextState] = 1 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDR'][nextState] = 1 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 1 + postsynaptic['RMDVL'][thisState]
        postsynaptic['SAAVR'][nextState] = 1 + postsynaptic['SAAVR'][thisState]
        postsynaptic['SIBDR'][nextState] = 1 + postsynaptic['SIBDR'][thisState]
        postsynaptic['SIBVR'][nextState] = 1 + postsynaptic['SIBVR'][thisState]
        postsynaptic['SMDVR'][nextState] = 1 + postsynaptic['SMDVR'][thisState]

def RMED():
        postsynaptic['IL1VL'][nextState] = 1 + postsynaptic['IL1VL'][thisState]
        postsynaptic['MVL02'][nextState] = -4 + postsynaptic['MVL02'][thisState]
        postsynaptic['MVL04'][nextState] = -4 + postsynaptic['MVL04'][thisState]
        postsynaptic['MVL06'][nextState] = -4 + postsynaptic['MVL06'][thisState]
        postsynaptic['MVR02'][nextState] = -4 + postsynaptic['MVR02'][thisState]
        postsynaptic['MVR04'][nextState] = -4 + postsynaptic['MVR04'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIPL'][nextState] = 1 + postsynaptic['RIPL'][thisState]
        postsynaptic['RIPR'][nextState] = 1 + postsynaptic['RIPR'][thisState]
        postsynaptic['RMEV'][nextState] = 2 + postsynaptic['RMEV'][thisState]

def RMEL():
        postsynaptic['MDR01'][nextState] = -5 + postsynaptic['MDR01'][thisState]
        postsynaptic['MDR03'][nextState] = -5 + postsynaptic['MDR03'][thisState]
        postsynaptic['MVR01'][nextState] = -5 + postsynaptic['MVR01'][thisState]
        postsynaptic['MVR03'][nextState] = -5 + postsynaptic['MVR03'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]

def RMER():
        postsynaptic['MDL01'][nextState] = -7 + postsynaptic['MDL01'][thisState]
        postsynaptic['MDL03'][nextState] = -7 + postsynaptic['MDL03'][thisState]
        postsynaptic['MVL01'][nextState] = -7 + postsynaptic['MVL01'][thisState]
        postsynaptic['RMEV'][nextState] = 1 + postsynaptic['RMEV'][thisState]

def RMEV():
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]
        postsynaptic['IL1DL'][nextState] = 1 + postsynaptic['IL1DL'][thisState]
        postsynaptic['IL1DR'][nextState] = 1 + postsynaptic['IL1DR'][thisState]
        postsynaptic['MDL02'][nextState] = -3 + postsynaptic['MDL02'][thisState]
        postsynaptic['MDL04'][nextState] = -3 + postsynaptic['MDL04'][thisState]
        postsynaptic['MDL06'][nextState] = -3 + postsynaptic['MDL06'][thisState]
        postsynaptic['MDR02'][nextState] = -3 + postsynaptic['MDR02'][thisState]
        postsynaptic['MDR04'][nextState] = -3 + postsynaptic['MDR04'][thisState]
        postsynaptic['RMED'][nextState] = 2 + postsynaptic['RMED'][thisState]
        postsynaptic['RMEL'][nextState] = 1 + postsynaptic['RMEL'][thisState]
        postsynaptic['RMER'][nextState] = 1 + postsynaptic['RMER'][thisState]
        postsynaptic['SMDDR'][nextState] = 1 + postsynaptic['SMDDR'][thisState]

def RMFL():
        postsynaptic['AVKL'][nextState] = 4 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 4 + postsynaptic['AVKR'][thisState]
        postsynaptic['MDR03'][nextState] = 1 + postsynaptic['MDR03'][thisState]
        postsynaptic['MVR01'][nextState] = 1 + postsynaptic['MVR01'][thisState]
        postsynaptic['MVR03'][nextState] = 1 + postsynaptic['MVR03'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['RMDR'][nextState] = 3 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMGR'][nextState] = 1 + postsynaptic['RMGR'][thisState]
        postsynaptic['URBR'][nextState] = 1 + postsynaptic['URBR'][thisState]

def RMFR():
        postsynaptic['AVKL'][nextState] = 3 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 3 + postsynaptic['AVKR'][thisState]
        postsynaptic['RMDL'][nextState] = 2 + postsynaptic['RMDL'][thisState]

def RMGL():
        postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
        postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['ALML'][nextState] = 1 + postsynaptic['ALML'][thisState]
        postsynaptic['ALNL'][nextState] = 1 + postsynaptic['ALNL'][thisState]
        postsynaptic['ASHL'][nextState] = 2 + postsynaptic['ASHL'][thisState]
        postsynaptic['ASKL'][nextState] = 2 + postsynaptic['ASKL'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVEL'][nextState] = 2 + postsynaptic['AVEL'][thisState]
        postsynaptic['AWBL'][nextState] = 1 + postsynaptic['AWBL'][thisState]
        postsynaptic['CEPDL'][nextState] = 1 + postsynaptic['CEPDL'][thisState]
        postsynaptic['IL2L'][nextState] = 1 + postsynaptic['IL2L'][thisState]
        postsynaptic['MDL05'][nextState] = 2 + postsynaptic['MDL05'][thisState]
        postsynaptic['MVL05'][nextState] = 2 + postsynaptic['MVL05'][thisState]
        postsynaptic['RID'][nextState] = 1 + postsynaptic['RID'][thisState]
        postsynaptic['RMDL'][nextState] = 1 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDR'][nextState] = 3 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 3 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMHL'][nextState] = 3 + postsynaptic['RMHL'][thisState]
        postsynaptic['RMHR'][nextState] = 1 + postsynaptic['RMHR'][thisState]
        postsynaptic['SIAVL'][nextState] = 1 + postsynaptic['SIAVL'][thisState]
        postsynaptic['SIBVL'][nextState] = 3 + postsynaptic['SIBVL'][thisState]
        postsynaptic['SIBVR'][nextState] = 1 + postsynaptic['SIBVR'][thisState]
        postsynaptic['SMBVL'][nextState] = 1 + postsynaptic['SMBVL'][thisState]
        postsynaptic['URXL'][nextState] = 2 + postsynaptic['URXL'][thisState]

def RMGR():
        postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]
        postsynaptic['AIMR'][nextState] = 1 + postsynaptic['AIMR'][thisState]
        postsynaptic['ALNR'][nextState] = 1 + postsynaptic['ALNR'][thisState]
        postsynaptic['ASHR'][nextState] = 2 + postsynaptic['ASHR'][thisState]
        postsynaptic['ASKR'][nextState] = 1 + postsynaptic['ASKR'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['AVER'][nextState] = 3 + postsynaptic['AVER'][thisState]
        postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]
        postsynaptic['AWBR'][nextState] = 1 + postsynaptic['AWBR'][thisState]
        postsynaptic['IL2R'][nextState] = 1 + postsynaptic['IL2R'][thisState]
        postsynaptic['MDR05'][nextState] = 1 + postsynaptic['MDR05'][thisState]
        postsynaptic['MVR05'][nextState] = 1 + postsynaptic['MVR05'][thisState]
        postsynaptic['MVR07'][nextState] = 1 + postsynaptic['MVR07'][thisState]
        postsynaptic['RIR'][nextState] = 1 + postsynaptic['RIR'][thisState]
        postsynaptic['RMDL'][nextState] = 4 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDR'][nextState] = 2 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMDVR'][nextState] = 5 + postsynaptic['RMDVR'][thisState]
        postsynaptic['RMHR'][nextState] = 1 + postsynaptic['RMHR'][thisState]
        postsynaptic['URXR'][nextState] = 2 + postsynaptic['URXR'][thisState]

def RMHL():
        postsynaptic['MDR01'][nextState] = 2 + postsynaptic['MDR01'][thisState]
        postsynaptic['MDR03'][nextState] = 3 + postsynaptic['MDR03'][thisState]
        postsynaptic['MVR01'][nextState] = 2 + postsynaptic['MVR01'][thisState]
        postsynaptic['RMDR'][nextState] = 1 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMGL'][nextState] = 3 + postsynaptic['RMGL'][thisState]
        postsynaptic['SIBVR'][nextState] = 1 + postsynaptic['SIBVR'][thisState]

def RMHR():
        postsynaptic['MDL01'][nextState] = 2 + postsynaptic['MDL01'][thisState]
        postsynaptic['MDL03'][nextState] = 2 + postsynaptic['MDL03'][thisState]
        postsynaptic['MDL05'][nextState] = 2 + postsynaptic['MDL05'][thisState]
        postsynaptic['MVL01'][nextState] = 2 + postsynaptic['MVL01'][thisState]
        postsynaptic['RMER'][nextState] = 1 + postsynaptic['RMER'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]
        postsynaptic['RMGR'][nextState] = 1 + postsynaptic['RMGR'][thisState]

def SAADL():
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]
        postsynaptic['RIML'][nextState] = 3 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 6 + postsynaptic['RIMR'][thisState]
        postsynaptic['RMGR'][nextState] = 1 + postsynaptic['RMGR'][thisState]
        postsynaptic['SMBDL'][nextState] = 1 + postsynaptic['SMBDL'][thisState]

def SAADR():
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['AVAR'][nextState] = 3 + postsynaptic['AVAR'][thisState]
        postsynaptic['OLLL'][nextState] = 1 + postsynaptic['OLLL'][thisState]
        postsynaptic['RIML'][nextState] = 4 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 5 + postsynaptic['RIMR'][thisState]
        postsynaptic['RMDDR'][nextState] = 1 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMFL'][nextState] = 1 + postsynaptic['RMFL'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]

def SAAVL():
        postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
        postsynaptic['ALNL'][nextState] = 1 + postsynaptic['ALNL'][thisState]
        postsynaptic['AVAL'][nextState] = 16 + postsynaptic['AVAL'][thisState]
        postsynaptic['OLLR'][nextState] = 1 + postsynaptic['OLLR'][thisState]
        postsynaptic['RIML'][nextState] = 2 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 12 + postsynaptic['RIMR'][thisState]
        postsynaptic['RMDVL'][nextState] = 2 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMFR'][nextState] = 2 + postsynaptic['RMFR'][thisState]
        postsynaptic['SMBVR'][nextState] = 3 + postsynaptic['SMBVR'][thisState]
        postsynaptic['SMDDR'][nextState] = 8 + postsynaptic['SMDDR'][thisState]

def SAAVR():
        postsynaptic['AVAR'][nextState] = 13 + postsynaptic['AVAR'][thisState]
        postsynaptic['RIML'][nextState] = 5 + postsynaptic['RIML'][thisState]
        postsynaptic['RIMR'][nextState] = 2 + postsynaptic['RIMR'][thisState]
        postsynaptic['RMDVR'][nextState] = 1 + postsynaptic['RMDVR'][thisState]
        postsynaptic['SMBVL'][nextState] = 2 + postsynaptic['SMBVL'][thisState]
        postsynaptic['SMDDL'][nextState] = 6 + postsynaptic['SMDDL'][thisState]

def SABD():
        postsynaptic['AVAL'][nextState] = 4 + postsynaptic['AVAL'][thisState]
        postsynaptic['VA2'][nextState] = 4 + postsynaptic['VA2'][thisState]
        postsynaptic['VA3'][nextState] = 2 + postsynaptic['VA3'][thisState]
        postsynaptic['VA4'][nextState] = 1 + postsynaptic['VA4'][thisState]

def SABVL():
        postsynaptic['AVAR'][nextState] = 3 + postsynaptic['AVAR'][thisState]
        postsynaptic['DA1'][nextState] = 2 + postsynaptic['DA1'][thisState]
        postsynaptic['DA2'][nextState] = 1 + postsynaptic['DA2'][thisState]

def SABVR():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['DA1'][nextState] = 3 + postsynaptic['DA1'][thisState]

def SDQL():
        postsynaptic['ALML'][nextState] = 2 + postsynaptic['ALML'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 3 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
        postsynaptic['FLPL'][nextState] = 1 + postsynaptic['FLPL'][thisState]
        postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
        postsynaptic['RIS'][nextState] = 3 + postsynaptic['RIS'][thisState]
        postsynaptic['RMFL'][nextState] = 1 + postsynaptic['RMFL'][thisState]
        postsynaptic['SDQR'][nextState] = 1 + postsynaptic['SDQR'][thisState]

def SDQR():
        postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]
        postsynaptic['AIBL'][nextState] = 2 + postsynaptic['AIBL'][thisState]
        postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVBL'][nextState] = 7 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 4 + postsynaptic['AVBR'][thisState]
        postsynaptic['DVA'][nextState] = 3 + postsynaptic['DVA'][thisState]
        postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
        postsynaptic['RIVL'][nextState] = 2 + postsynaptic['RIVL'][thisState]
        postsynaptic['RIVR'][nextState] = 2 + postsynaptic['RIVR'][thisState]
        postsynaptic['RMHL'][nextState] = 2 + postsynaptic['RMHL'][thisState]
        postsynaptic['RMHR'][nextState] = 1 + postsynaptic['RMHR'][thisState]
        postsynaptic['SDQL'][nextState] = 1 + postsynaptic['SDQL'][thisState]
        postsynaptic['SIBVL'][nextState] = 1 + postsynaptic['SIBVL'][thisState]

def SIADL():
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]

def SIADR():
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]

def SIAVL():
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]

def SIAVR():
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]

def SIBDL():
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['SIBVL'][nextState] = 1 + postsynaptic['SIBVL'][thisState]

def SIBDR():
        postsynaptic['AIML'][nextState] = 1 + postsynaptic['AIML'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['SIBVR'][nextState] = 1 + postsynaptic['SIBVR'][thisState]

def SIBVL():
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['SDQR'][nextState] = 1 + postsynaptic['SDQR'][thisState]
        postsynaptic['SIBDL'][nextState] = 1 + postsynaptic['SIBDL'][thisState]

def SIBVR():
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RMHL'][nextState] = 1 + postsynaptic['RMHL'][thisState]
        postsynaptic['SIBDR'][nextState] = 1 + postsynaptic['SIBDR'][thisState]

def SMBDL():
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 1 + postsynaptic['AVKR'][thisState]
        postsynaptic['MDR01'][nextState] = 2 + postsynaptic['MDR01'][thisState]
        postsynaptic['MDR02'][nextState] = 2 + postsynaptic['MDR02'][thisState]
        postsynaptic['MDR03'][nextState] = 2 + postsynaptic['MDR03'][thisState]
        postsynaptic['MDR04'][nextState] = 2 + postsynaptic['MDR04'][thisState]
        postsynaptic['MDR06'][nextState] = 3 + postsynaptic['MDR06'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RMED'][nextState] = 3 + postsynaptic['RMED'][thisState]
        postsynaptic['SAADL'][nextState] = 1 + postsynaptic['SAADL'][thisState]
        postsynaptic['SAAVR'][nextState] = 1 + postsynaptic['SAAVR'][thisState]

def SMBDR():
        postsynaptic['ALNL'][nextState] = 1 + postsynaptic['ALNL'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 2 + postsynaptic['AVKR'][thisState]
        postsynaptic['MDL02'][nextState] = 1 + postsynaptic['MDL02'][thisState]
        postsynaptic['MDL03'][nextState] = 1 + postsynaptic['MDL03'][thisState]
        postsynaptic['MDL04'][nextState] = 1 + postsynaptic['MDL04'][thisState]
        postsynaptic['MDL06'][nextState] = 2 + postsynaptic['MDL06'][thisState]
        postsynaptic['MDR04'][nextState] = 1 + postsynaptic['MDR04'][thisState]
        postsynaptic['MDR08'][nextState] = 1 + postsynaptic['MDR08'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RMED'][nextState] = 4 + postsynaptic['RMED'][thisState]
        postsynaptic['SAAVL'][nextState] = 3 + postsynaptic['SAAVL'][thisState]

def SMBVL():
        postsynaptic['MVL01'][nextState] = 1 + postsynaptic['MVL01'][thisState]
        postsynaptic['MVL02'][nextState] = 1 + postsynaptic['MVL02'][thisState]
        postsynaptic['MVL03'][nextState] = 1 + postsynaptic['MVL03'][thisState]
        postsynaptic['MVL04'][nextState] = 1 + postsynaptic['MVL04'][thisState]
        postsynaptic['MVL05'][nextState] = 1 + postsynaptic['MVL05'][thisState]
        postsynaptic['MVL06'][nextState] = 1 + postsynaptic['MVL06'][thisState]
        postsynaptic['MVL08'][nextState] = 1 + postsynaptic['MVL08'][thisState]
        postsynaptic['PLNL'][nextState] = 1 + postsynaptic['PLNL'][thisState]
        postsynaptic['RMEV'][nextState] = 5 + postsynaptic['RMEV'][thisState]
        postsynaptic['SAADL'][nextState] = 3 + postsynaptic['SAADL'][thisState]
        postsynaptic['SAAVR'][nextState] = 2 + postsynaptic['SAAVR'][thisState]

def SMBVR():
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['AVKR'][nextState] = 1 + postsynaptic['AVKR'][thisState]
        postsynaptic['MVR01'][nextState] = 1 + postsynaptic['MVR01'][thisState]
        postsynaptic['MVR02'][nextState] = 1 + postsynaptic['MVR02'][thisState]
        postsynaptic['MVR03'][nextState] = 1 + postsynaptic['MVR03'][thisState]
        postsynaptic['MVR04'][nextState] = 1 + postsynaptic['MVR04'][thisState]
        postsynaptic['MVR06'][nextState] = 1 + postsynaptic['MVR06'][thisState]
        postsynaptic['MVR07'][nextState] = 1 + postsynaptic['MVR07'][thisState]
        postsynaptic['RMEV'][nextState] = 3 + postsynaptic['RMEV'][thisState]
        postsynaptic['SAADR'][nextState] = 4 + postsynaptic['SAADR'][thisState]
        postsynaptic['SAAVL'][nextState] = 3 + postsynaptic['SAAVL'][thisState]

def SMDDL():
        postsynaptic['MDL04'][nextState] = 1 + postsynaptic['MDL04'][thisState]
        postsynaptic['MDL06'][nextState] = 1 + postsynaptic['MDL06'][thisState]
        postsynaptic['MDL08'][nextState] = 1 + postsynaptic['MDL08'][thisState]
        postsynaptic['MDR02'][nextState] = 1 + postsynaptic['MDR02'][thisState]
        postsynaptic['MDR03'][nextState] = 1 + postsynaptic['MDR03'][thisState]
        postsynaptic['MDR04'][nextState] = 1 + postsynaptic['MDR04'][thisState]
        postsynaptic['MDR05'][nextState] = 1 + postsynaptic['MDR05'][thisState]
        postsynaptic['MDR06'][nextState] = 1 + postsynaptic['MDR06'][thisState]
        postsynaptic['MDR07'][nextState] = 1 + postsynaptic['MDR07'][thisState]
        postsynaptic['MVL02'][nextState] = 1 + postsynaptic['MVL02'][thisState]
        postsynaptic['MVL04'][nextState] = 1 + postsynaptic['MVL04'][thisState]
        postsynaptic['RIAL'][nextState] = 1 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 1 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIS'][nextState] = 1 + postsynaptic['RIS'][thisState]
        postsynaptic['RMDDL'][nextState] = 1 + postsynaptic['RMDDL'][thisState]
        postsynaptic['SMDVR'][nextState] = 2 + postsynaptic['SMDVR'][thisState]

def SMDDR():
        postsynaptic['MDL04'][nextState] = 1 + postsynaptic['MDL04'][thisState]
        postsynaptic['MDL05'][nextState] = 1 + postsynaptic['MDL05'][thisState]
        postsynaptic['MDL06'][nextState] = 1 + postsynaptic['MDL06'][thisState]
        postsynaptic['MDL08'][nextState] = 1 + postsynaptic['MDL08'][thisState]
        postsynaptic['MDR04'][nextState] = 1 + postsynaptic['MDR04'][thisState]
        postsynaptic['MDR06'][nextState] = 1 + postsynaptic['MDR06'][thisState]
        postsynaptic['MVR02'][nextState] = 1 + postsynaptic['MVR02'][thisState]
        postsynaptic['RIAL'][nextState] = 2 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 1 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIS'][nextState] = 1 + postsynaptic['RIS'][thisState]
        postsynaptic['RMDDR'][nextState] = 1 + postsynaptic['RMDDR'][thisState]
        postsynaptic['VD1'][nextState] = 1 + postsynaptic['VD1'][thisState]

def SMDVL():
        postsynaptic['MVL03'][nextState] = 1 + postsynaptic['MVL03'][thisState]
        postsynaptic['MVL06'][nextState] = 1 + postsynaptic['MVL06'][thisState]
        postsynaptic['MVR02'][nextState] = 1 + postsynaptic['MVR02'][thisState]
        postsynaptic['MVR03'][nextState] = 1 + postsynaptic['MVR03'][thisState]
        postsynaptic['MVR04'][nextState] = 1 + postsynaptic['MVR04'][thisState]
        postsynaptic['MVR06'][nextState] = 1 + postsynaptic['MVR06'][thisState]
        postsynaptic['PVR'][nextState] = 1 + postsynaptic['PVR'][thisState]
        postsynaptic['RIAL'][nextState] = 3 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 8 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIBR'][nextState] = 2 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIS'][nextState] = 1 + postsynaptic['RIS'][thisState]
        postsynaptic['RIVL'][nextState] = 2 + postsynaptic['RIVL'][thisState]
        postsynaptic['RMDDR'][nextState] = 1 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 1 + postsynaptic['RMDVL'][thisState]
        postsynaptic['SMDDR'][nextState] = 4 + postsynaptic['SMDDR'][thisState]
        postsynaptic['SMDVR'][nextState] = 1 + postsynaptic['SMDVR'][thisState]

def SMDVR():
        postsynaptic['MVL02'][nextState] = 1 + postsynaptic['MVL02'][thisState]
        postsynaptic['MVL03'][nextState] = 1 + postsynaptic['MVL03'][thisState]
        postsynaptic['MVL04'][nextState] = 1 + postsynaptic['MVL04'][thisState]
        postsynaptic['MVR07'][nextState] = 1 + postsynaptic['MVR07'][thisState]
        postsynaptic['RIAL'][nextState] = 7 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIAR'][nextState] = 5 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIBL'][nextState] = 2 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIVR'][nextState] = 1 + postsynaptic['RIVR'][thisState]
        postsynaptic['RIVR'][nextState] = 2 + postsynaptic['RIVR'][thisState]
        postsynaptic['RMDDL'][nextState] = 1 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDVR'][nextState] = 1 + postsynaptic['RMDVR'][thisState]
        postsynaptic['SMDDL'][nextState] = 2 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDVL'][nextState] = 1 + postsynaptic['SMDVL'][thisState]
        postsynaptic['VB1'][nextState] = 1 + postsynaptic['VB1'][thisState]

def URADL():
        postsynaptic['IL1DL'][nextState] = 2 + postsynaptic['IL1DL'][thisState]
        postsynaptic['MDL02'][nextState] = 2 + postsynaptic['MDL02'][thisState]
        postsynaptic['MDL03'][nextState] = 2 + postsynaptic['MDL03'][thisState]
        postsynaptic['MDL04'][nextState] = 2 + postsynaptic['MDL04'][thisState]
        postsynaptic['RIPL'][nextState] = 3 + postsynaptic['RIPL'][thisState]
        postsynaptic['RMEL'][nextState] = 1 + postsynaptic['RMEL'][thisState]

def URADR():
        postsynaptic['IL1DR'][nextState] = 1 + postsynaptic['IL1DR'][thisState]
        postsynaptic['MDR01'][nextState] = 3 + postsynaptic['MDR01'][thisState]
        postsynaptic['MDR02'][nextState] = 2 + postsynaptic['MDR02'][thisState]
        postsynaptic['MDR03'][nextState] = 3 + postsynaptic['MDR03'][thisState]
        postsynaptic['RIPR'][nextState] = 3 + postsynaptic['RIPR'][thisState]
        postsynaptic['RMDVR'][nextState] = 1 + postsynaptic['RMDVR'][thisState]
        postsynaptic['RMED'][nextState] = 1 + postsynaptic['RMED'][thisState]
        postsynaptic['RMER'][nextState] = 1 + postsynaptic['RMER'][thisState]
        postsynaptic['URYDR'][nextState] = 1 + postsynaptic['URYDR'][thisState]

def URAVL():
        postsynaptic['MVL01'][nextState] = 2 + postsynaptic['MVL01'][thisState]
        postsynaptic['MVL02'][nextState] = 2 + postsynaptic['MVL02'][thisState]
        postsynaptic['MVL03'][nextState] = 3 + postsynaptic['MVL03'][thisState]
        postsynaptic['MVL04'][nextState] = 2 + postsynaptic['MVL04'][thisState]
        postsynaptic['RIPL'][nextState] = 3 + postsynaptic['RIPL'][thisState]
        postsynaptic['RMEL'][nextState] = 1 + postsynaptic['RMEL'][thisState]
        postsynaptic['RMER'][nextState] = 1 + postsynaptic['RMER'][thisState]
        postsynaptic['RMEV'][nextState] = 2 + postsynaptic['RMEV'][thisState]

def URAVR():
        postsynaptic['IL1R'][nextState] = 1 + postsynaptic['IL1R'][thisState]
        postsynaptic['MVR01'][nextState] = 2 + postsynaptic['MVR01'][thisState]
        postsynaptic['MVR02'][nextState] = 2 + postsynaptic['MVR02'][thisState]
        postsynaptic['MVR03'][nextState] = 2 + postsynaptic['MVR03'][thisState]
        postsynaptic['MVR04'][nextState] = 2 + postsynaptic['MVR04'][thisState]
        postsynaptic['RIPR'][nextState] = 3 + postsynaptic['RIPR'][thisState]
        postsynaptic['RMDVL'][nextState] = 1 + postsynaptic['RMDVL'][thisState]
        postsynaptic['RMER'][nextState] = 2 + postsynaptic['RMER'][thisState]
        postsynaptic['RMEV'][nextState] = 2 + postsynaptic['RMEV'][thisState]

def URBL():
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['CEPDL'][nextState] = 1 + postsynaptic['CEPDL'][thisState]
        postsynaptic['IL1L'][nextState] = 1 + postsynaptic['IL1L'][thisState]
        postsynaptic['OLQDL'][nextState] = 1 + postsynaptic['OLQDL'][thisState]
        postsynaptic['OLQVL'][nextState] = 1 + postsynaptic['OLQVL'][thisState]
        postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
        postsynaptic['RMDDR'][nextState] = 1 + postsynaptic['RMDDR'][thisState]
        postsynaptic['SIAVL'][nextState] = 1 + postsynaptic['SIAVL'][thisState]
        postsynaptic['SMBDR'][nextState] = 1 + postsynaptic['SMBDR'][thisState]
        postsynaptic['URXL'][nextState] = 2 + postsynaptic['URXL'][thisState]

def URBR():
        postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['CEPDR'][nextState] = 1 + postsynaptic['CEPDR'][thisState]
        postsynaptic['IL1R'][nextState] = 3 + postsynaptic['IL1R'][thisState]
        postsynaptic['IL2R'][nextState] = 1 + postsynaptic['IL2R'][thisState]
        postsynaptic['OLQDR'][nextState] = 1 + postsynaptic['OLQDR'][thisState]
        postsynaptic['OLQVR'][nextState] = 1 + postsynaptic['OLQVR'][thisState]
        postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
        postsynaptic['RMDL'][nextState] = 1 + postsynaptic['RMDL'][thisState]
        postsynaptic['RMDR'][nextState] = 1 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMFL'][nextState] = 1 + postsynaptic['RMFL'][thisState]
        postsynaptic['SIAVR'][nextState] = 2 + postsynaptic['SIAVR'][thisState]
        postsynaptic['SMBDL'][nextState] = 1 + postsynaptic['SMBDL'][thisState]
        postsynaptic['URXR'][nextState] = 4 + postsynaptic['URXR'][thisState]

def URXL():
        postsynaptic['ASHL'][nextState] = 1 + postsynaptic['ASHL'][thisState]
        postsynaptic['AUAL'][nextState] = 5 + postsynaptic['AUAL'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVEL'][nextState] = 4 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVJR'][nextState] = 1 + postsynaptic['AVJR'][thisState]
        postsynaptic['RIAL'][nextState] = 8 + postsynaptic['RIAL'][thisState]
        postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
        postsynaptic['RIGL'][nextState] = 3 + postsynaptic['RIGL'][thisState]
        postsynaptic['RMGL'][nextState] = 2 + postsynaptic['RMGL'][thisState]
        postsynaptic['RMGL'][nextState] = 1 + postsynaptic['RMGL'][thisState]

def URXR():
        postsynaptic['AUAR'][nextState] = 4 + postsynaptic['AUAR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVER'][nextState] = 2 + postsynaptic['AVER'][thisState]
        postsynaptic['IL2R'][nextState] = 1 + postsynaptic['IL2R'][thisState]
        postsynaptic['OLQVR'][nextState] = 1 + postsynaptic['OLQVR'][thisState]
        postsynaptic['RIAR'][nextState] = 3 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIGR'][nextState] = 2 + postsynaptic['RIGR'][thisState]
        postsynaptic['RIPR'][nextState] = 3 + postsynaptic['RIPR'][thisState]
        postsynaptic['RMDR'][nextState] = 1 + postsynaptic['RMDR'][thisState]
        postsynaptic['RMGR'][nextState] = 2 + postsynaptic['RMGR'][thisState]
        postsynaptic['SIAVR'][nextState] = 1 + postsynaptic['SIAVR'][thisState]

def URYDL():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVER'][nextState] = 2 + postsynaptic['AVER'][thisState]
        postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RMDDR'][nextState] = 4 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 6 + postsynaptic['RMDVL'][thisState]
        postsynaptic['SMDDL'][nextState] = 1 + postsynaptic['SMDDL'][thisState]
        postsynaptic['SMDDR'][nextState] = 1 + postsynaptic['SMDDR'][thisState]

def URYDR():
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVEL'][nextState] = 2 + postsynaptic['AVEL'][thisState]
        postsynaptic['AVER'][nextState] = 2 + postsynaptic['AVER'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['RMDDL'][nextState] = 3 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDVR'][nextState] = 5 + postsynaptic['RMDVR'][thisState]
        postsynaptic['SMDDL'][nextState] = 4 + postsynaptic['SMDDL'][thisState]

def URYVL():
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVER'][nextState] = 5 + postsynaptic['AVER'][thisState]
        postsynaptic['IL1VL'][nextState] = 1 + postsynaptic['IL1VL'][thisState]
        postsynaptic['RIAL'][nextState] = 1 + postsynaptic['RIAL'][thisState]
        postsynaptic['RIBL'][nextState] = 2 + postsynaptic['RIBL'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['RIH'][nextState] = 1 + postsynaptic['RIH'][thisState]
        postsynaptic['RIS'][nextState] = 1 + postsynaptic['RIS'][thisState]
        postsynaptic['RMDDL'][nextState] = 4 + postsynaptic['RMDDL'][thisState]
        postsynaptic['RMDVR'][nextState] = 2 + postsynaptic['RMDVR'][thisState]
        postsynaptic['SIBVR'][nextState] = 1 + postsynaptic['SIBVR'][thisState]
        postsynaptic['SMDVR'][nextState] = 4 + postsynaptic['SMDVR'][thisState]

def URYVR():
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVEL'][nextState] = 6 + postsynaptic['AVEL'][thisState]
        postsynaptic['IL1VR'][nextState] = 1 + postsynaptic['IL1VR'][thisState]
        postsynaptic['RIAR'][nextState] = 1 + postsynaptic['RIAR'][thisState]
        postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
        postsynaptic['RIGR'][nextState] = 1 + postsynaptic['RIGR'][thisState]
        postsynaptic['RMDDR'][nextState] = 6 + postsynaptic['RMDDR'][thisState]
        postsynaptic['RMDVL'][nextState] = 4 + postsynaptic['RMDVL'][thisState]
        postsynaptic['SIBDR'][nextState] = 1 + postsynaptic['SIBDR'][thisState]
        postsynaptic['SIBVL'][nextState] = 1 + postsynaptic['SIBVL'][thisState]
        postsynaptic['SMDVL'][nextState] = 3 + postsynaptic['SMDVL'][thisState]

def VA1():
        postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
        postsynaptic['DA2'][nextState] = 2 + postsynaptic['DA2'][thisState]
        postsynaptic['DD1'][nextState] = 9 + postsynaptic['DD1'][thisState]
        postsynaptic['MVL07'][nextState] = 3 + postsynaptic['MVL07'][thisState]
        postsynaptic['MVL08'][nextState] = 3 + postsynaptic['MVL08'][thisState]
        postsynaptic['MVR07'][nextState] = 3 + postsynaptic['MVR07'][thisState]
        postsynaptic['MVR08'][nextState] = 3 + postsynaptic['MVR08'][thisState]
        postsynaptic['VD1'][nextState] = 2 + postsynaptic['VD1'][thisState]

def VA2():
        postsynaptic['AVAL'][nextState] = 5 + postsynaptic['AVAL'][thisState]
        postsynaptic['DD1'][nextState] = 13 + postsynaptic['DD1'][thisState]
        postsynaptic['MVL07'][nextState] = 5 + postsynaptic['MVL07'][thisState]
        postsynaptic['MVL10'][nextState] = 5 + postsynaptic['MVL10'][thisState]
        postsynaptic['MVR07'][nextState] = 5 + postsynaptic['MVR07'][thisState]
        postsynaptic['MVR10'][nextState] = 5 + postsynaptic['MVR10'][thisState]
        postsynaptic['SABD'][nextState] = 3 + postsynaptic['SABD'][thisState]
        postsynaptic['VA3'][nextState] = 2 + postsynaptic['VA3'][thisState]
        postsynaptic['VB1'][nextState] = 2 + postsynaptic['VB1'][thisState]
        postsynaptic['VD1'][nextState] = 2 + postsynaptic['VD1'][thisState]
        postsynaptic['VD1'][nextState] = 1 + postsynaptic['VD1'][thisState]
        postsynaptic['VD2'][nextState] = 11 + postsynaptic['VD2'][thisState]

def VA3():
        postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['DD1'][nextState] = 18 + postsynaptic['DD1'][thisState]
        postsynaptic['DD2'][nextState] = 11 + postsynaptic['DD2'][thisState]
        postsynaptic['MVL09'][nextState] = 5 + postsynaptic['MVL09'][thisState]
        postsynaptic['MVL10'][nextState] = 5 + postsynaptic['MVL10'][thisState]
        postsynaptic['MVL12'][nextState] = 5 + postsynaptic['MVL12'][thisState]
        postsynaptic['MVR09'][nextState] = 5 + postsynaptic['MVR09'][thisState]
        postsynaptic['MVR10'][nextState] = 5 + postsynaptic['MVR10'][thisState]
        postsynaptic['MVR12'][nextState] = 5 + postsynaptic['MVR12'][thisState]
        postsynaptic['SABD'][nextState] = 2 + postsynaptic['SABD'][thisState]
        postsynaptic['VA4'][nextState] = 1 + postsynaptic['VA4'][thisState]
        postsynaptic['VD2'][nextState] = 3 + postsynaptic['VD2'][thisState]
        postsynaptic['VD3'][nextState] = 3 + postsynaptic['VD3'][thisState]

def VA4():
        postsynaptic['AS2'][nextState] = 2 + postsynaptic['AS2'][thisState]
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
        postsynaptic['DA5'][nextState] = 1 + postsynaptic['DA5'][thisState]
        postsynaptic['DD2'][nextState] = 21 + postsynaptic['DD2'][thisState]
        postsynaptic['MVL11'][nextState] = 6 + postsynaptic['MVL11'][thisState]
        postsynaptic['MVL12'][nextState] = 6 + postsynaptic['MVL12'][thisState]
        postsynaptic['MVR11'][nextState] = 6 + postsynaptic['MVR11'][thisState]
        postsynaptic['MVR12'][nextState] = 6 + postsynaptic['MVR12'][thisState]
        postsynaptic['SABD'][nextState] = 1 + postsynaptic['SABD'][thisState]
        postsynaptic['VB3'][nextState] = 2 + postsynaptic['VB3'][thisState]
        postsynaptic['VD4'][nextState] = 3 + postsynaptic['VD4'][thisState]
        
def VA5():
        postsynaptic['AS3'][nextState] = 2 + postsynaptic['AS3'][thisState]
        postsynaptic['AVAL'][nextState] = 5 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 3 + postsynaptic['AVAR'][thisState]
        postsynaptic['DA5'][nextState] = 2 + postsynaptic['DA5'][thisState]
        postsynaptic['DD2'][nextState] = 5 + postsynaptic['DD2'][thisState]
        postsynaptic['DD3'][nextState] = 13 + postsynaptic['DD3'][thisState]
        postsynaptic['MVL11'][nextState] = 5 + postsynaptic['MVL11'][thisState]
        postsynaptic['MVL14'][nextState] = 5 + postsynaptic['MVL14'][thisState]
        postsynaptic['MVR11'][nextState] = 5 + postsynaptic['MVR11'][thisState]
        postsynaptic['MVR14'][nextState] = 5 + postsynaptic['MVR14'][thisState]
        postsynaptic['VD5'][nextState] = 2 + postsynaptic['VD5'][thisState]

def VA6():
        postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['DD3'][nextState] = 24 + postsynaptic['DD3'][thisState]
        postsynaptic['MVL13'][nextState] = 5 + postsynaptic['MVL13'][thisState]
        postsynaptic['MVL14'][nextState] = 5 + postsynaptic['MVL14'][thisState]
        postsynaptic['MVR13'][nextState] = 5 + postsynaptic['MVR13'][thisState]
        postsynaptic['MVR14'][nextState] = 5 + postsynaptic['MVR14'][thisState]
        postsynaptic['VB5'][nextState] = 2 + postsynaptic['VB5'][thisState]
        postsynaptic['VD5'][nextState] = 1 + postsynaptic['VD5'][thisState]
        postsynaptic['VD6'][nextState] = 2 + postsynaptic['VD6'][thisState]

def VA7():
        postsynaptic['AS5'][nextState] = 1 + postsynaptic['AS5'][thisState]
        postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 4 + postsynaptic['AVAR'][thisState]
        postsynaptic['DD3'][nextState] = 3 + postsynaptic['DD3'][thisState]
        postsynaptic['DD4'][nextState] = 12 + postsynaptic['DD4'][thisState]
        postsynaptic['MVL13'][nextState] = 4 + postsynaptic['MVL13'][thisState]
        postsynaptic['MVL15'][nextState] = 4 + postsynaptic['MVL15'][thisState]
        postsynaptic['MVL16'][nextState] = 4 + postsynaptic['MVL16'][thisState]
        postsynaptic['MVR13'][nextState] = 4 + postsynaptic['MVR13'][thisState]
        postsynaptic['MVR15'][nextState] = 4 + postsynaptic['MVR15'][thisState]
        postsynaptic['MVR16'][nextState] = 4 + postsynaptic['MVR16'][thisState]
        postsynaptic['MVULVA'][nextState] = 4 + postsynaptic['MVULVA'][thisState]
        postsynaptic['VB3'][nextState] = 1 + postsynaptic['VB3'][thisState]
        postsynaptic['VD7'][nextState] = 9 + postsynaptic['VD7'][thisState]

def VA8():
        postsynaptic['AS6'][nextState] = 1 + postsynaptic['AS6'][thisState]
        postsynaptic['AVAL'][nextState] = 10 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 4 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DD4'][nextState] = 21 + postsynaptic['DD4'][thisState]
        postsynaptic['MVL15'][nextState] = 6 + postsynaptic['MVL15'][thisState]
        postsynaptic['MVL16'][nextState] = 6 + postsynaptic['MVL16'][thisState]
        postsynaptic['MVR15'][nextState] = 6 + postsynaptic['MVR15'][thisState]
        postsynaptic['MVR16'][nextState] = 6 + postsynaptic['MVR16'][thisState]
        postsynaptic['PDER'][nextState] = 1 + postsynaptic['PDER'][thisState]
        postsynaptic['PVCR'][nextState] = 2 + postsynaptic['PVCR'][thisState]
        postsynaptic['VA8'][nextState] = 1 + postsynaptic['VA8'][thisState]
        postsynaptic['VA9'][nextState] = 1 + postsynaptic['VA9'][thisState]
        postsynaptic['VB6'][nextState] = 1 + postsynaptic['VB6'][thisState]
        postsynaptic['VB8'][nextState] = 1 + postsynaptic['VB8'][thisState]
        postsynaptic['VB8'][nextState] = 3 + postsynaptic['VB8'][thisState]
        postsynaptic['VB9'][nextState] = 3 + postsynaptic['VB9'][thisState]
        postsynaptic['VD7'][nextState] = 5 + postsynaptic['VD7'][thisState]
        postsynaptic['VD8'][nextState] = 5 + postsynaptic['VD8'][thisState]
        postsynaptic['VD8'][nextState] = 1 + postsynaptic['VD8'][thisState]

def VA9():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DD4'][nextState] = 3 + postsynaptic['DD4'][thisState]
        postsynaptic['DD5'][nextState] = 15 + postsynaptic['DD5'][thisState]
        postsynaptic['DVB'][nextState] = 1 + postsynaptic['DVB'][thisState]
        postsynaptic['DVC'][nextState] = 1 + postsynaptic['DVC'][thisState]
        postsynaptic['MVL15'][nextState] = 5 + postsynaptic['MVL15'][thisState]
        postsynaptic['MVL18'][nextState] = 5 + postsynaptic['MVL18'][thisState]
        postsynaptic['MVR15'][nextState] = 5 + postsynaptic['MVR15'][thisState]
        postsynaptic['MVR18'][nextState] = 5 + postsynaptic['MVR18'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['VB8'][nextState] = 6 + postsynaptic['VB8'][thisState]
        postsynaptic['VB8'][nextState] = 1 + postsynaptic['VB8'][thisState]
        postsynaptic['VB9'][nextState] = 4 + postsynaptic['VB9'][thisState]
        postsynaptic['VD7'][nextState] = 1 + postsynaptic['VD7'][thisState]
        postsynaptic['VD9'][nextState] = 10 + postsynaptic['VD9'][thisState]


def VA10():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['MVL17'][nextState] = 5 + postsynaptic['MVL17'][thisState]
        postsynaptic['MVL18'][nextState] = 5 + postsynaptic['MVL18'][thisState]
        postsynaptic['MVR17'][nextState] = 5 + postsynaptic['MVR17'][thisState]
        postsynaptic['MVR18'][nextState] = 5 + postsynaptic['MVR18'][thisState]

def VA11():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 7 + postsynaptic['AVAR'][thisState]
        postsynaptic['DD6'][nextState] = 10 + postsynaptic['DD6'][thisState]
        postsynaptic['MVL19'][nextState] = 5 + postsynaptic['MVL19'][thisState]
        postsynaptic['MVL20'][nextState] = 5 + postsynaptic['MVL20'][thisState]
        postsynaptic['MVR19'][nextState] = 5 + postsynaptic['MVR19'][thisState]
        postsynaptic['MVR20'][nextState] = 5 + postsynaptic['MVR20'][thisState]
        postsynaptic['PVNR'][nextState] = 2 + postsynaptic['PVNR'][thisState]
        postsynaptic['VB10'][nextState] = 1 + postsynaptic['VB10'][thisState]
        postsynaptic['VD12'][nextState] = 4 + postsynaptic['VD12'][thisState]

def VA12():
        postsynaptic['AS11'][nextState] = 2 + postsynaptic['AS11'][thisState]
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['DA8'][nextState] = 3 + postsynaptic['DA8'][thisState]
        postsynaptic['DA9'][nextState] = 5 + postsynaptic['DA9'][thisState]
        postsynaptic['DB7'][nextState] = 4 + postsynaptic['DB7'][thisState]
        postsynaptic['DD6'][nextState] = 2 + postsynaptic['DD6'][thisState]
        postsynaptic['LUAL'][nextState] = 2 + postsynaptic['LUAL'][thisState]
        postsynaptic['MVL21'][nextState] = 5 + postsynaptic['MVL21'][thisState]
        postsynaptic['MVL22'][nextState] = 5 + postsynaptic['MVL22'][thisState]
        postsynaptic['MVL23'][nextState] = 5 + postsynaptic['MVL23'][thisState]
        postsynaptic['MVR21'][nextState] = 5 + postsynaptic['MVR21'][thisState]
        postsynaptic['MVR22'][nextState] = 5 + postsynaptic['MVR22'][thisState]
        postsynaptic['MVR23'][nextState] = 5 + postsynaptic['MVR23'][thisState]
        postsynaptic['MVR24'][nextState] = 5 + postsynaptic['MVR24'][thisState]
        postsynaptic['PHCL'][nextState] = 1 + postsynaptic['PHCL'][thisState]
        postsynaptic['PHCR'][nextState] = 1 + postsynaptic['PHCR'][thisState]
        postsynaptic['PVCL'][nextState] = 2 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 3 + postsynaptic['PVCR'][thisState]
        postsynaptic['VA11'][nextState] = 1 + postsynaptic['VA11'][thisState]
        postsynaptic['VB11'][nextState] = 1 + postsynaptic['VB11'][thisState]
        postsynaptic['VD12'][nextState] = 3 + postsynaptic['VD12'][thisState]
        postsynaptic['VD13'][nextState] = 11 + postsynaptic['VD13'][thisState]

def VB1():
        postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVKL'][nextState] = 4 + postsynaptic['AVKL'][thisState]
        postsynaptic['DB2'][nextState] = 2 + postsynaptic['DB2'][thisState]
        postsynaptic['DD1'][nextState] = 1 + postsynaptic['DD1'][thisState]
        postsynaptic['DVA'][nextState] = 1 + postsynaptic['DVA'][thisState]
        postsynaptic['MVL07'][nextState] = 1 + postsynaptic['MVL07'][thisState]
        postsynaptic['MVL08'][nextState] = 1 + postsynaptic['MVL08'][thisState]
        postsynaptic['MVR07'][nextState] = 1 + postsynaptic['MVR07'][thisState]
        postsynaptic['MVR08'][nextState] = 1 + postsynaptic['MVR08'][thisState]
        postsynaptic['RIML'][nextState] = 2 + postsynaptic['RIML'][thisState]
        postsynaptic['RMFL'][nextState] = 2 + postsynaptic['RMFL'][thisState]
        postsynaptic['SAADL'][nextState] = 9 + postsynaptic['SAADL'][thisState]
        postsynaptic['SAADR'][nextState] = 2 + postsynaptic['SAADR'][thisState]
        postsynaptic['SABD'][nextState] = 1 + postsynaptic['SABD'][thisState]
        postsynaptic['SMDVR'][nextState] = 1 + postsynaptic['SMDVR'][thisState]
        postsynaptic['VA1'][nextState] = 3 + postsynaptic['VA1'][thisState]
        postsynaptic['VA3'][nextState] = 1 + postsynaptic['VA3'][thisState]
        postsynaptic['VB2'][nextState] = 4 + postsynaptic['VB2'][thisState]
        postsynaptic['VD1'][nextState] = 3 + postsynaptic['VD1'][thisState]
        postsynaptic['VD2'][nextState] = 1 + postsynaptic['VD2'][thisState]

def VB2():
        postsynaptic['AVBL'][nextState] = 3 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DB4'][nextState] = 1 + postsynaptic['DB4'][thisState]
        postsynaptic['DD1'][nextState] = 20 + postsynaptic['DD1'][thisState]
        postsynaptic['DD2'][nextState] = 1 + postsynaptic['DD2'][thisState]
        postsynaptic['MVL07'][nextState] = 4 + postsynaptic['MVL07'][thisState]
        postsynaptic['MVL09'][nextState] = 4 + postsynaptic['MVL09'][thisState]
        postsynaptic['MVL10'][nextState] = 4 + postsynaptic['MVL10'][thisState]
        postsynaptic['MVL12'][nextState] = 4 + postsynaptic['MVL12'][thisState]
        postsynaptic['MVR07'][nextState] = 4 + postsynaptic['MVR07'][thisState]
        postsynaptic['MVR09'][nextState] = 4 + postsynaptic['MVR09'][thisState]
        postsynaptic['MVR10'][nextState] = 4 + postsynaptic['MVR10'][thisState]
        postsynaptic['MVR12'][nextState] = 4 + postsynaptic['MVR12'][thisState]
        postsynaptic['RIGL'][nextState] = 1 + postsynaptic['RIGL'][thisState]
        postsynaptic['VA2'][nextState] = 1 + postsynaptic['VA2'][thisState]
        postsynaptic['VB1'][nextState] = 4 + postsynaptic['VB1'][thisState]
        postsynaptic['VB3'][nextState] = 1 + postsynaptic['VB3'][thisState]
        postsynaptic['VB5'][nextState] = 1 + postsynaptic['VB5'][thisState]
        postsynaptic['VB7'][nextState] = 2 + postsynaptic['VB7'][thisState]
        postsynaptic['VC2'][nextState] = 1 + postsynaptic['VC2'][thisState]
        postsynaptic['VD2'][nextState] = 9 + postsynaptic['VD2'][thisState]
        postsynaptic['VD3'][nextState] = 3 + postsynaptic['VD3'][thisState]

def VB3():
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DB1'][nextState] = 1 + postsynaptic['DB1'][thisState]
        postsynaptic['DD2'][nextState] = 37 + postsynaptic['DD2'][thisState]
        postsynaptic['MVL11'][nextState] = 6 + postsynaptic['MVL11'][thisState]
        postsynaptic['MVL12'][nextState] = 6 + postsynaptic['MVL12'][thisState]
        postsynaptic['MVL14'][nextState] = 6 + postsynaptic['MVL14'][thisState]
        postsynaptic['MVR11'][nextState] = 6 + postsynaptic['MVR11'][thisState]
        postsynaptic['MVR12'][nextState] = 6 + postsynaptic['MVR12'][thisState]
        postsynaptic['MVR14'][nextState] = 6 + postsynaptic['MVR14'][thisState]
        postsynaptic['VA4'][nextState] = 1 + postsynaptic['VA4'][thisState]
        postsynaptic['VA7'][nextState] = 1 + postsynaptic['VA7'][thisState]
        postsynaptic['VB2'][nextState] = 1 + postsynaptic['VB2'][thisState]

def VB4():
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DB1'][nextState] = 1 + postsynaptic['DB1'][thisState]
        postsynaptic['DB4'][nextState] = 1 + postsynaptic['DB4'][thisState]
        postsynaptic['DD2'][nextState] = 6 + postsynaptic['DD2'][thisState]
        postsynaptic['DD3'][nextState] = 16 + postsynaptic['DD3'][thisState]
        postsynaptic['MVL11'][nextState] = 5 + postsynaptic['MVL11'][thisState]
        postsynaptic['MVL14'][nextState] = 5 + postsynaptic['MVL14'][thisState]
        postsynaptic['MVR11'][nextState] = 5 + postsynaptic['MVR11'][thisState]
        postsynaptic['MVR14'][nextState] = 5 + postsynaptic['MVR14'][thisState]
        postsynaptic['VB5'][nextState] = 1 + postsynaptic['VB5'][thisState]

def VB5():
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['DD3'][nextState] = 27 + postsynaptic['DD3'][thisState]
        postsynaptic['MVL13'][nextState] = 6 + postsynaptic['MVL13'][thisState]
        postsynaptic['MVL14'][nextState] = 6 + postsynaptic['MVL14'][thisState]
        postsynaptic['MVR13'][nextState] = 6 + postsynaptic['MVR13'][thisState]
        postsynaptic['MVR14'][nextState] = 6 + postsynaptic['MVR14'][thisState]
        postsynaptic['VB2'][nextState] = 1 + postsynaptic['VB2'][thisState]
        postsynaptic['VB4'][nextState] = 1 + postsynaptic['VB4'][thisState]
        postsynaptic['VB6'][nextState] = 8 + postsynaptic['VB6'][thisState]

def VB6():
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['DA4'][nextState] = 1 + postsynaptic['DA4'][thisState]
        postsynaptic['DD4'][nextState] = 30 + postsynaptic['DD4'][thisState]
        postsynaptic['MVL15'][nextState] = 6 + postsynaptic['MVL15'][thisState]
        postsynaptic['MVL16'][nextState] = 6 + postsynaptic['MVL16'][thisState]
        postsynaptic['MVR15'][nextState] = 6 + postsynaptic['MVR15'][thisState]
        postsynaptic['MVR16'][nextState] = 6 + postsynaptic['MVR16'][thisState]
        postsynaptic['MVULVA'][nextState] = 6 + postsynaptic['MVULVA'][thisState]
        postsynaptic['VA8'][nextState] = 1 + postsynaptic['VA8'][thisState]
        postsynaptic['VB5'][nextState] = 1 + postsynaptic['VB5'][thisState]
        postsynaptic['VB7'][nextState] = 1 + postsynaptic['VB7'][thisState]
        postsynaptic['VD6'][nextState] = 1 + postsynaptic['VD6'][thisState]
        postsynaptic['VD7'][nextState] = 8 + postsynaptic['VD7'][thisState]

def VB7():
        postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 2 + postsynaptic['AVBR'][thisState]
        postsynaptic['DD4'][nextState] = 2 + postsynaptic['DD4'][thisState]
        postsynaptic['MVL15'][nextState] = 5 + postsynaptic['MVL15'][thisState]
        postsynaptic['MVR15'][nextState] = 5 + postsynaptic['MVR15'][thisState]
        postsynaptic['VB2'][nextState] = 2 + postsynaptic['VB2'][thisState]

def VB8():
        postsynaptic['AVBL'][nextState] = 7 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 3 + postsynaptic['AVBR'][thisState]
        postsynaptic['DD5'][nextState] = 30 + postsynaptic['DD5'][thisState]
        postsynaptic['MVL17'][nextState] = 5 + postsynaptic['MVL17'][thisState]
        postsynaptic['MVL18'][nextState] = 5 + postsynaptic['MVL18'][thisState]
        postsynaptic['MVL20'][nextState] = 5 + postsynaptic['MVL20'][thisState]
        postsynaptic['MVR17'][nextState] = 5 + postsynaptic['MVR17'][thisState]
        postsynaptic['MVR18'][nextState] = 5 + postsynaptic['MVR18'][thisState]
        postsynaptic['MVR20'][nextState] = 5 + postsynaptic['MVR20'][thisState]
        postsynaptic['VA8'][nextState] = 3 + postsynaptic['VA8'][thisState]
        postsynaptic['VA9'][nextState] = 9 + postsynaptic['VA9'][thisState]
        postsynaptic['VA9'][nextState] = 1 + postsynaptic['VA9'][thisState]
        postsynaptic['VB9'][nextState] = 6 + postsynaptic['VB9'][thisState]
        postsynaptic['VD10'][nextState] = 1 + postsynaptic['VD10'][thisState]
        postsynaptic['VD9'][nextState] = 10 + postsynaptic['VD9'][thisState]

def VB9():
        postsynaptic['AVAL'][nextState] = 5 + postsynaptic['AVAL'][thisState]
        postsynaptic['AVAR'][nextState] = 4 + postsynaptic['AVAR'][thisState]
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 6 + postsynaptic['AVBR'][thisState]
        postsynaptic['DD5'][nextState] = 8 + postsynaptic['DD5'][thisState]
        postsynaptic['DVB'][nextState] = 1 + postsynaptic['DVB'][thisState]
        postsynaptic['MVL17'][nextState] = 6 + postsynaptic['MVL17'][thisState]
        postsynaptic['MVL20'][nextState] = 6 + postsynaptic['MVL20'][thisState]
        postsynaptic['MVR17'][nextState] = 6 + postsynaptic['MVR17'][thisState]
        postsynaptic['MVR20'][nextState] = 6 + postsynaptic['MVR20'][thisState]
        postsynaptic['PVCL'][nextState] = 2 + postsynaptic['PVCL'][thisState]
        postsynaptic['VA8'][nextState] = 3 + postsynaptic['VA8'][thisState]
        postsynaptic['VA9'][nextState] = 4 + postsynaptic['VA9'][thisState]
        postsynaptic['VB8'][nextState] = 1 + postsynaptic['VB8'][thisState]
        postsynaptic['VB8'][nextState] = 3 + postsynaptic['VB8'][thisState]
        postsynaptic['VD10'][nextState] = 5 + postsynaptic['VD10'][thisState]

def VB10():
        postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]
        postsynaptic['DD6'][nextState] = 9 + postsynaptic['DD6'][thisState]
        postsynaptic['MVL19'][nextState] = 5 + postsynaptic['MVL19'][thisState]
        postsynaptic['MVL20'][nextState] = 5 + postsynaptic['MVL20'][thisState]
        postsynaptic['MVR19'][nextState] = 5 + postsynaptic['MVR19'][thisState]
        postsynaptic['MVR20'][nextState] = 5 + postsynaptic['MVR20'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['VD11'][nextState] = 1 + postsynaptic['VD11'][thisState]
        postsynaptic['VD12'][nextState] = 2 + postsynaptic['VD12'][thisState]

def VB11():
        postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DD6'][nextState] = 7 + postsynaptic['DD6'][thisState]
        postsynaptic['MVL21'][nextState] = 5 + postsynaptic['MVL21'][thisState]
        postsynaptic['MVL22'][nextState] = 5 + postsynaptic['MVL22'][thisState]
        postsynaptic['MVL23'][nextState] = 5 + postsynaptic['MVL23'][thisState]
        postsynaptic['MVR21'][nextState] = 5 + postsynaptic['MVR21'][thisState]
        postsynaptic['MVR22'][nextState] = 5 + postsynaptic['MVR22'][thisState]
        postsynaptic['MVR23'][nextState] = 5 + postsynaptic['MVR23'][thisState]
        postsynaptic['MVR24'][nextState] = 5 + postsynaptic['MVR24'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['VA12'][nextState] = 2 + postsynaptic['VA12'][thisState]

def VC1():
        postsynaptic['AVL'][nextState] = 2 + postsynaptic['AVL'][thisState]
        postsynaptic['DD1'][nextState] = 7 + postsynaptic['DD1'][thisState]
        postsynaptic['DD2'][nextState] = 6 + postsynaptic['DD2'][thisState]
        postsynaptic['DD3'][nextState] = 6 + postsynaptic['DD3'][thisState]
        postsynaptic['DVC'][nextState] = 1 + postsynaptic['DVC'][thisState]
        postsynaptic['MVULVA'][nextState] = 6 + postsynaptic['MVULVA'][thisState]
        postsynaptic['PVT'][nextState] = 2 + postsynaptic['PVT'][thisState]
        postsynaptic['VC2'][nextState] = 9 + postsynaptic['VC2'][thisState]
        postsynaptic['VC3'][nextState] = 3 + postsynaptic['VC3'][thisState]
        postsynaptic['VD1'][nextState] = 5 + postsynaptic['VD1'][thisState]
        postsynaptic['VD2'][nextState] = 1 + postsynaptic['VD2'][thisState]
        postsynaptic['VD3'][nextState] = 1 + postsynaptic['VD3'][thisState]
        postsynaptic['VD4'][nextState] = 2 + postsynaptic['VD4'][thisState]
        postsynaptic['VD5'][nextState] = 5 + postsynaptic['VD5'][thisState]
        postsynaptic['VD6'][nextState] = 1 + postsynaptic['VD6'][thisState]

def VC2():
        postsynaptic['DB4'][nextState] = 1 + postsynaptic['DB4'][thisState]
        postsynaptic['DD1'][nextState] = 6 + postsynaptic['DD1'][thisState]
        postsynaptic['DD2'][nextState] = 4 + postsynaptic['DD2'][thisState]
        postsynaptic['DD3'][nextState] = 9 + postsynaptic['DD3'][thisState]
        postsynaptic['DVC'][nextState] = 1 + postsynaptic['DVC'][thisState]
        postsynaptic['MVULVA'][nextState] = 10 + postsynaptic['MVULVA'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVQR'][nextState] = 1 + postsynaptic['PVQR'][thisState]
        postsynaptic['PVT'][nextState] = 2 + postsynaptic['PVT'][thisState]
        postsynaptic['VC1'][nextState] = 10 + postsynaptic['VC1'][thisState]
        postsynaptic['VC3'][nextState] = 6 + postsynaptic['VC3'][thisState]
        postsynaptic['VD1'][nextState] = 2 + postsynaptic['VD1'][thisState]
        postsynaptic['VD2'][nextState] = 2 + postsynaptic['VD2'][thisState]
        postsynaptic['VD4'][nextState] = 5 + postsynaptic['VD4'][thisState]
        postsynaptic['VD5'][nextState] = 5 + postsynaptic['VD5'][thisState]
        postsynaptic['VD6'][nextState] = 1 + postsynaptic['VD6'][thisState]

def VC3():
        postsynaptic['AVL'][nextState] = 1 + postsynaptic['AVL'][thisState]
        postsynaptic['DD1'][nextState] = 2 + postsynaptic['DD1'][thisState]
        postsynaptic['DD2'][nextState] = 4 + postsynaptic['DD2'][thisState]
        postsynaptic['DD3'][nextState] = 5 + postsynaptic['DD3'][thisState]
        postsynaptic['DD4'][nextState] = 13 + postsynaptic['DD4'][thisState]
        postsynaptic['DVC'][nextState] = 1 + postsynaptic['DVC'][thisState]
        postsynaptic['HSNR'][nextState] = 1 + postsynaptic['HSNR'][thisState]
        postsynaptic['MVULVA'][nextState] = 11 + postsynaptic['MVULVA'][thisState]
        postsynaptic['PVNR'][nextState] = 1 + postsynaptic['PVNR'][thisState]
        postsynaptic['PVPR'][nextState] = 1 + postsynaptic['PVPR'][thisState]
        postsynaptic['PVQR'][nextState] = 4 + postsynaptic['PVQR'][thisState]
        postsynaptic['VC1'][nextState] = 4 + postsynaptic['VC1'][thisState]
        postsynaptic['VC2'][nextState] = 3 + postsynaptic['VC2'][thisState]
        postsynaptic['VC4'][nextState] = 1 + postsynaptic['VC4'][thisState]
        postsynaptic['VC5'][nextState] = 2 + postsynaptic['VC5'][thisState]
        postsynaptic['VD1'][nextState] = 1 + postsynaptic['VD1'][thisState]
        postsynaptic['VD2'][nextState] = 1 + postsynaptic['VD2'][thisState]
        postsynaptic['VD3'][nextState] = 1 + postsynaptic['VD3'][thisState]
        postsynaptic['VD4'][nextState] = 2 + postsynaptic['VD4'][thisState]
        postsynaptic['VD5'][nextState] = 4 + postsynaptic['VD5'][thisState]
        postsynaptic['VD6'][nextState] = 4 + postsynaptic['VD6'][thisState]
        postsynaptic['VD7'][nextState] = 5 + postsynaptic['VD7'][thisState]

def VC4():
        postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
        postsynaptic['AVFR'][nextState] = 1 + postsynaptic['AVFR'][thisState]
        postsynaptic['AVHR'][nextState] = 1 + postsynaptic['AVHR'][thisState]
        postsynaptic['MVULVA'][nextState] = 7 + postsynaptic['MVULVA'][thisState]
        postsynaptic['VC1'][nextState] = 1 + postsynaptic['VC1'][thisState]
        postsynaptic['VC3'][nextState] = 5 + postsynaptic['VC3'][thisState]
        postsynaptic['VC5'][nextState] = 2 + postsynaptic['VC5'][thisState]

def VC5():
        postsynaptic['AVFL'][nextState] = 1 + postsynaptic['AVFL'][thisState]
        postsynaptic['AVFR'][nextState] = 1 + postsynaptic['AVFR'][thisState]
        postsynaptic['DVC'][nextState] = 2 + postsynaptic['DVC'][thisState]
        postsynaptic['HSNL'][nextState] = 1 + postsynaptic['HSNL'][thisState]
        postsynaptic['MVULVA'][nextState] = 2 + postsynaptic['MVULVA'][thisState]
        postsynaptic['OLLR'][nextState] = 1 + postsynaptic['OLLR'][thisState]
        postsynaptic['PVT'][nextState] = 1 + postsynaptic['PVT'][thisState]
        postsynaptic['URBL'][nextState] = 3 + postsynaptic['URBL'][thisState]
        postsynaptic['VC3'][nextState] = 3 + postsynaptic['VC3'][thisState]
        postsynaptic['VC4'][nextState] = 2 + postsynaptic['VC4'][thisState]

def VC6():
        postsynaptic['MVULVA'][nextState] = 1 + postsynaptic['MVULVA'][thisState]
           
def VD1():
        postsynaptic['DD1'][nextState] = 5 + postsynaptic['DD1'][thisState]
        postsynaptic['DVC'][nextState] = 5 + postsynaptic['DVC'][thisState]
        postsynaptic['MVL05'][nextState] = -5 + postsynaptic['MVL05'][thisState]
        postsynaptic['MVL08'][nextState] = -5 + postsynaptic['MVL08'][thisState]
        postsynaptic['MVR05'][nextState] = -5 + postsynaptic['MVR05'][thisState]
        postsynaptic['MVR08'][nextState] = -5 + postsynaptic['MVR08'][thisState]
        postsynaptic['RIFL'][nextState] = 1 + postsynaptic['RIFL'][thisState]
        postsynaptic['RIGL'][nextState] = 2 + postsynaptic['RIGL'][thisState]
        postsynaptic['SMDDR'][nextState] = 1 + postsynaptic['SMDDR'][thisState]
        postsynaptic['VA1'][nextState] = 2 + postsynaptic['VA1'][thisState]
        postsynaptic['VA2'][nextState] = 1 + postsynaptic['VA2'][thisState]
        postsynaptic['VC1'][nextState] = 1 + postsynaptic['VC1'][thisState]
        postsynaptic['VD2'][nextState] = 7 + postsynaptic['VD2'][thisState]

def VD2():
        postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]
        postsynaptic['DD1'][nextState] = 3 + postsynaptic['DD1'][thisState]
        postsynaptic['MVL07'][nextState] = -7 + postsynaptic['MVL07'][thisState]
        postsynaptic['MVL10'][nextState] = -7 + postsynaptic['MVL10'][thisState]
        postsynaptic['MVR07'][nextState] = -7 + postsynaptic['MVR07'][thisState]
        postsynaptic['MVR10'][nextState] = -7 + postsynaptic['MVR10'][thisState]
        postsynaptic['VA2'][nextState] = 9 + postsynaptic['VA2'][thisState]
        postsynaptic['VB2'][nextState] = 3 + postsynaptic['VB2'][thisState]
        postsynaptic['VD1'][nextState] = 7 + postsynaptic['VD1'][thisState]
        postsynaptic['VD3'][nextState] = 2 + postsynaptic['VD3'][thisState]

def VD3():
        postsynaptic['MVL09'][nextState] = -7 + postsynaptic['MVL09'][thisState]
        postsynaptic['MVL12'][nextState] = -9 + postsynaptic['MVL12'][thisState]
        postsynaptic['MVR09'][nextState] = -7 + postsynaptic['MVR09'][thisState]
        postsynaptic['MVR12'][nextState] = -7 + postsynaptic['MVR12'][thisState]
        postsynaptic['PVPL'][nextState] = 1 + postsynaptic['PVPL'][thisState]
        postsynaptic['VA3'][nextState] = 2 + postsynaptic['VA3'][thisState]
        postsynaptic['VB2'][nextState] = 2 + postsynaptic['VB2'][thisState]
        postsynaptic['VD2'][nextState] = 2 + postsynaptic['VD2'][thisState]
        postsynaptic['VD4'][nextState] = 1 + postsynaptic['VD4'][thisState]

def VD4():
        postsynaptic['DD2'][nextState] = 2 + postsynaptic['DD2'][thisState]
        postsynaptic['MVL11'][nextState] = -9 + postsynaptic['MVL11'][thisState]
        postsynaptic['MVL12'][nextState] = -9 + postsynaptic['MVL12'][thisState]
        postsynaptic['MVR11'][nextState] = -9 + postsynaptic['MVR11'][thisState]
        postsynaptic['MVR12'][nextState] = -9 + postsynaptic['MVR12'][thisState]
        postsynaptic['PVPR'][nextState] = 1 + postsynaptic['PVPR'][thisState]
        postsynaptic['VD3'][nextState] = 1 + postsynaptic['VD3'][thisState]
        postsynaptic['VD5'][nextState] = 1 + postsynaptic['VD5'][thisState]

def VD5():
        postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
        postsynaptic['MVL14'][nextState] = -17 + postsynaptic['MVL14'][thisState]
        postsynaptic['MVR14'][nextState] = -17 + postsynaptic['MVR14'][thisState]
        postsynaptic['PVPR'][nextState] = 1 + postsynaptic['PVPR'][thisState]
        postsynaptic['VA5'][nextState] = 2 + postsynaptic['VA5'][thisState]
        postsynaptic['VB4'][nextState] = 2 + postsynaptic['VB4'][thisState]
        postsynaptic['VD4'][nextState] = 1 + postsynaptic['VD4'][thisState]
        postsynaptic['VD6'][nextState] = 2 + postsynaptic['VD6'][thisState]

def VD6():
        postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
        postsynaptic['MVL13'][nextState] = -7 + postsynaptic['MVL13'][thisState]
        postsynaptic['MVL14'][nextState] = -7 + postsynaptic['MVL14'][thisState]
        postsynaptic['MVL16'][nextState] = -7 + postsynaptic['MVL16'][thisState]
        postsynaptic['MVR13'][nextState] = -7 + postsynaptic['MVR13'][thisState]
        postsynaptic['MVR14'][nextState] = -7 + postsynaptic['MVR14'][thisState]
        postsynaptic['MVR16'][nextState] = -7 + postsynaptic['MVR16'][thisState]
        postsynaptic['VA6'][nextState] = 1 + postsynaptic['VA6'][thisState]
        postsynaptic['VB5'][nextState] = 2 + postsynaptic['VB5'][thisState]
        postsynaptic['VD5'][nextState] = 2 + postsynaptic['VD5'][thisState]
        postsynaptic['VD7'][nextState] = 1 + postsynaptic['VD7'][thisState]

def VD7():
        postsynaptic['MVL15'][nextState] = -7 + postsynaptic['MVL15'][thisState]
        postsynaptic['MVL16'][nextState] = -7 + postsynaptic['MVL16'][thisState]
        postsynaptic['MVR15'][nextState] = -7 + postsynaptic['MVR15'][thisState]
        postsynaptic['MVR16'][nextState] = -7 + postsynaptic['MVR16'][thisState]
        postsynaptic['MVULVA'][nextState] = -15 + postsynaptic['MVULVA'][thisState]
        postsynaptic['VA9'][nextState] = 1 + postsynaptic['VA9'][thisState]
        postsynaptic['VD6'][nextState] = 1 + postsynaptic['VD6'][thisState]

def VD8():
        postsynaptic['DD4'][nextState] = 2 + postsynaptic['DD4'][thisState]
        postsynaptic['MVL15'][nextState] = -18 + postsynaptic['MVL15'][thisState]
        postsynaptic['MVR15'][nextState] = -18 + postsynaptic['MVR15'][thisState]
        postsynaptic['VA8'][nextState] = 5 + postsynaptic['VA8'][thisState]

def VD9():
        postsynaptic['MVL17'][nextState] = -10 + postsynaptic['MVL17'][thisState]
        postsynaptic['MVL18'][nextState] = -10 + postsynaptic['MVL18'][thisState]
        postsynaptic['MVR17'][nextState] = -10 + postsynaptic['MVR17'][thisState]
        postsynaptic['MVR18'][nextState] = -10 + postsynaptic['MVR18'][thisState]
        postsynaptic['PDER'][nextState] = 1 + postsynaptic['PDER'][thisState]
        postsynaptic['VD10'][nextState] = 5 + postsynaptic['VD10'][thisState]

def VD10():
        postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
        postsynaptic['DD5'][nextState] = 2 + postsynaptic['DD5'][thisState]
        postsynaptic['DVC'][nextState] = 4 + postsynaptic['DVC'][thisState]
        postsynaptic['MVL17'][nextState] = -9 + postsynaptic['MVL17'][thisState]
        postsynaptic['MVL20'][nextState] = -9 + postsynaptic['MVL20'][thisState]
        postsynaptic['MVR17'][nextState] = -9 + postsynaptic['MVR17'][thisState]
        postsynaptic['MVR20'][nextState] = -9 + postsynaptic['MVR20'][thisState]
        postsynaptic['VB9'][nextState] = 2 + postsynaptic['VB9'][thisState]
        postsynaptic['VD9'][nextState] = 5 + postsynaptic['VD9'][thisState]

def VD11():
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['MVL19'][nextState] = -9 + postsynaptic['MVL19'][thisState]
        postsynaptic['MVL20'][nextState] = -9 + postsynaptic['MVL20'][thisState]
        postsynaptic['MVR19'][nextState] = -9 + postsynaptic['MVR19'][thisState]
        postsynaptic['MVR20'][nextState] = -9 + postsynaptic['MVR20'][thisState]
        postsynaptic['VA11'][nextState] = 1 + postsynaptic['VA11'][thisState]
        postsynaptic['VB10'][nextState] = 1 + postsynaptic['VB10'][thisState]

def VD12():
        postsynaptic['MVL19'][nextState] = -5 + postsynaptic['MVL19'][thisState]
        postsynaptic['MVL21'][nextState] = -5 + postsynaptic['MVL21'][thisState]
        postsynaptic['MVR19'][nextState] = -5 + postsynaptic['MVR19'][thisState]
        postsynaptic['MVR22'][nextState] = -5 + postsynaptic['MVR22'][thisState]
        postsynaptic['VA11'][nextState] = 3 + postsynaptic['VA11'][thisState]
        postsynaptic['VA12'][nextState] = 2 + postsynaptic['VA12'][thisState]
        postsynaptic['VB10'][nextState] = 1 + postsynaptic['VB10'][thisState]
        postsynaptic['VB11'][nextState] = 1 + postsynaptic['VB11'][thisState]

def VD13():
        postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
        postsynaptic['MVL21'][nextState] = -9 + postsynaptic['MVL21'][thisState]
        postsynaptic['MVL22'][nextState] = -9 + postsynaptic['MVL22'][thisState]
        postsynaptic['MVL23'][nextState] = -9 + postsynaptic['MVL23'][thisState]
        postsynaptic['MVR21'][nextState] = -9 + postsynaptic['MVR21'][thisState]
        postsynaptic['MVR22'][nextState] = -9 + postsynaptic['MVR22'][thisState]
        postsynaptic['MVR23'][nextState] = -9 + postsynaptic['MVR23'][thisState]
        postsynaptic['MVR24'][nextState] = -9 + postsynaptic['MVR24'][thisState]
        postsynaptic['PVCL'][nextState] = 1 + postsynaptic['PVCL'][thisState]
        postsynaptic['PVCR'][nextState] = 1 + postsynaptic['PVCR'][thisState]
        postsynaptic['PVPL'][nextState] = 2 + postsynaptic['PVPL'][thisState]
        postsynaptic['VA12'][nextState] = 1 + postsynaptic['VA12'][thisState]
        
        
def createpostsynaptic():
        # The PostSynaptic dictionary maintains the accumulated values for
        # each neuron and muscle. The Accumulated values are initialized to Zero
        postsynaptic['ADAL'] = 0,0
        postsynaptic['ADAR'] = 0,0
        postsynaptic['ADEL'] = 0,0
        postsynaptic['ADER'] = 0,0
        postsynaptic['ADFL'] = 0,0
        postsynaptic['ADFR'] = 0,0
        postsynaptic['ADLL'] = 0,0
        postsynaptic['ADLR'] = 0,0
        postsynaptic['AFDL'] = 0,0
        postsynaptic['AFDR'] = 0,0
        postsynaptic['AIAL'] = 0,0
        postsynaptic['AIAR'] = 0,0
        postsynaptic['AIBL'] = 0,0
        postsynaptic['AIBR'] = 0,0
        postsynaptic['AIML'] = 0,0
        postsynaptic['AIMR'] = 0,0
        postsynaptic['AINL'] = 0,0
        postsynaptic['AINR'] = 0,0
        postsynaptic['AIYL'] = 0,0
        postsynaptic['AIYR'] = 0,0
        postsynaptic['AIZL'] = 0,0
        postsynaptic['AIZR'] = 0,0
        postsynaptic['ALA'] = 0,0
        postsynaptic['ALML'] = 0,0
        postsynaptic['ALMR'] = 0,0
        postsynaptic['ALNL'] = 0,0
        postsynaptic['ALNR'] = 0,0
        postsynaptic['AQR'] = 0,0
        postsynaptic['AS1'] = 0,0
        postsynaptic['AS10'] = 0,0
        postsynaptic['AS11'] = 0,0
        postsynaptic['AS2'] = 0,0
        postsynaptic['AS3'] = 0,0
        postsynaptic['AS4'] = 0,0
        postsynaptic['AS5'] = 0,0
        postsynaptic['AS6'] = 0,0
        postsynaptic['AS7'] = 0,0
        postsynaptic['AS8'] = 0,0
        postsynaptic['AS9'] = 0,0
        postsynaptic['ASEL'] = 0,0
        postsynaptic['ASER'] = 0,0
        postsynaptic['ASGL'] = 0,0
        postsynaptic['ASGR'] = 0,0
        postsynaptic['ASHL'] = 0,0
        postsynaptic['ASHR'] = 0,0
        postsynaptic['ASIL'] = 0,0
        postsynaptic['ASIR'] = 0,0
        postsynaptic['ASJL'] = 0,0
        postsynaptic['ASJR'] = 0,0
        postsynaptic['ASKL'] = 0,0
        postsynaptic['ASKR'] = 0,0
        postsynaptic['AUAL'] = 0,0
        postsynaptic['AUAR'] = 0,0
        postsynaptic['AVAL'] = 0,0
        postsynaptic['AVAR'] = 0,0
        postsynaptic['AVBL'] = 0,0
        postsynaptic['AVBR'] = 0,0
        postsynaptic['AVDL'] = 0,0
        postsynaptic['AVDR'] = 0,0
        postsynaptic['AVEL'] = 0,0
        postsynaptic['AVER'] = 0,0
        postsynaptic['AVFL'] = 0,0
        postsynaptic['AVFR'] = 0,0
        postsynaptic['AVG'] = 0,0
        postsynaptic['AVHL'] = 0,0
        postsynaptic['AVHR'] = 0,0
        postsynaptic['AVJL'] = 0,0
        postsynaptic['AVJR'] = 0,0
        postsynaptic['AVKL'] = 0,0
        postsynaptic['AVKR'] = 0,0
        postsynaptic['AVL'] = 0,0
        postsynaptic['AVM'] = 0,0
        postsynaptic['AWAL'] = 0,0
        postsynaptic['AWAR'] = 0,0
        postsynaptic['AWBL'] = 0,0
        postsynaptic['AWBR'] = 0,0
        postsynaptic['AWCL'] = 0,0
        postsynaptic['AWCR'] = 0,0
        postsynaptic['BAGL'] = 0,0
        postsynaptic['BAGR'] = 0,0
        postsynaptic['BDUL'] = 0,0
        postsynaptic['BDUR'] = 0,0
        postsynaptic['CEPDL'] = 0,0
        postsynaptic['CEPDR'] = 0,0
        postsynaptic['CEPVL'] = 0,0
        postsynaptic['CEPVR'] = 0,0
        postsynaptic['DA1'] = 0,0
        postsynaptic['DA2'] = 0,0
        postsynaptic['DA3'] = 0,0
        postsynaptic['DA4'] = 0,0
        postsynaptic['DA5'] = 0,0
        postsynaptic['DA6'] = 0,0
        postsynaptic['DA7'] = 0,0
        postsynaptic['DA8'] = 0,0
        postsynaptic['DA9'] = 0,0
        postsynaptic['DB1'] = 0,0
        postsynaptic['DB2'] = 0,0
        postsynaptic['DB3'] = 0,0
        postsynaptic['DB4'] = 0,0
        postsynaptic['DB5'] = 0,0
        postsynaptic['DB6'] = 0,0
        postsynaptic['DB7'] = 0,0
        postsynaptic['DD1'] = 0,0
        postsynaptic['DD2'] = 0,0
        postsynaptic['DD3'] = 0,0
        postsynaptic['DD4'] = 0,0
        postsynaptic['DD5'] = 0,0
        postsynaptic['DD6'] = 0,0
        postsynaptic['DVA'] = 0,0
        postsynaptic['DVB'] = 0,0
        postsynaptic['DVC'] = 0,0
        postsynaptic['FLPL'] = 0,0
        postsynaptic['FLPR'] = 0,0
        postsynaptic['HSNL'] = 0,0
        postsynaptic['HSNR'] = 0,0
        postsynaptic['I1L'] = 0,0
        postsynaptic['I1R'] = 0,0
        postsynaptic['I2L'] = 0,0
        postsynaptic['I2R'] = 0,0
        postsynaptic['I3'] = 0,0
        postsynaptic['I4'] = 0,0
        postsynaptic['I5'] = 0,0
        postsynaptic['I6'] = 0,0
        postsynaptic['IL1DL'] = 0,0
        postsynaptic['IL1DR'] = 0,0
        postsynaptic['IL1L'] = 0,0
        postsynaptic['IL1R'] = 0,0
        postsynaptic['IL1VL'] = 0,0
        postsynaptic['IL1VR'] = 0,0
        postsynaptic['IL2L'] = 0,0
        postsynaptic['IL2R'] = 0,0
        postsynaptic['IL2DL'] = 0,0
        postsynaptic['IL2DR'] = 0,0
        postsynaptic['IL2VL'] = 0,0
        postsynaptic['IL2VR'] = 0,0
        postsynaptic['LUAL'] = 0,0
        postsynaptic['LUAR'] = 0,0
        postsynaptic['M1'] = 0,0
        postsynaptic['M2L'] = 0,0
        postsynaptic['M2R'] = 0,0
        postsynaptic['M3L'] = 0,0
        postsynaptic['M3R'] = 0,0
        postsynaptic['M4'] = 0,0
        postsynaptic['M5'] = 0,0
        postsynaptic['MANAL'] = 0,0
        postsynaptic['MCL'] = 0,0
        postsynaptic['MCR'] = 0,0
        postsynaptic['MDL01'] = 0,0
        postsynaptic['MDL02'] = 0,0
        postsynaptic['MDL03'] = 0,0
        postsynaptic['MDL04'] = 0,0
        postsynaptic['MDL05'] = 0,0
        postsynaptic['MDL06'] = 0,0
        postsynaptic['MDL07'] = 0,0
        postsynaptic['MDL08'] = 0,0
        postsynaptic['MDL09'] = 0,0
        postsynaptic['MDL10'] = 0,0
        postsynaptic['MDL11'] = 0,0
        postsynaptic['MDL12'] = 0,0
        postsynaptic['MDL13'] = 0,0
        postsynaptic['MDL14'] = 0,0
        postsynaptic['MDL15'] = 0,0
        postsynaptic['MDL16'] = 0,0
        postsynaptic['MDL17'] = 0,0
        postsynaptic['MDL18'] = 0,0
        postsynaptic['MDL19'] = 0,0
        postsynaptic['MDL20'] = 0,0
        postsynaptic['MDL21'] = 0,0
        postsynaptic['MDL22'] = 0,0
        postsynaptic['MDL23'] = 0,0
        postsynaptic['MDL24'] = 0,0
        postsynaptic['MDR01'] = 0,0
        postsynaptic['MDR02'] = 0,0
        postsynaptic['MDR03'] = 0,0
        postsynaptic['MDR04'] = 0,0
        postsynaptic['MDR05'] = 0,0
        postsynaptic['MDR06'] = 0,0
        postsynaptic['MDR07'] = 0,0
        postsynaptic['MDR08'] = 0,0
        postsynaptic['MDR09'] = 0,0
        postsynaptic['MDR10'] = 0,0
        postsynaptic['MDR11'] = 0,0
        postsynaptic['MDR12'] = 0,0
        postsynaptic['MDR13'] = 0,0
        postsynaptic['MDR14'] = 0,0
        postsynaptic['MDR15'] = 0,0
        postsynaptic['MDR16'] = 0,0
        postsynaptic['MDR17'] = 0,0
        postsynaptic['MDR18'] = 0,0
        postsynaptic['MDR19'] = 0,0
        postsynaptic['MDR20'] = 0,0
        postsynaptic['MDR21'] = 0,0
        postsynaptic['MDR22'] = 0,0
        postsynaptic['MDR23'] = 0,0
        postsynaptic['MDR24'] = 0,0
        postsynaptic['MI'] = 0,0
        postsynaptic['MVL01'] = 0,0
        postsynaptic['MVL02'] = 0,0
        postsynaptic['MVL03'] = 0,0
        postsynaptic['MVL04'] = 0,0
        postsynaptic['MVL05'] = 0,0
        postsynaptic['MVL06'] = 0,0
        postsynaptic['MVL07'] = 0,0
        postsynaptic['MVL08'] = 0,0
        postsynaptic['MVL09'] = 0,0
        postsynaptic['MVL10'] = 0,0
        postsynaptic['MVL11'] = 0,0
        postsynaptic['MVL12'] = 0,0
        postsynaptic['MVL13'] = 0,0
        postsynaptic['MVL14'] = 0,0
        postsynaptic['MVL15'] = 0,0
        postsynaptic['MVL16'] = 0,0
        postsynaptic['MVL17'] = 0,0
        postsynaptic['MVL18'] = 0,0
        postsynaptic['MVL19'] = 0,0
        postsynaptic['MVL20'] = 0,0
        postsynaptic['MVL21'] = 0,0
        postsynaptic['MVL22'] = 0,0
        postsynaptic['MVL23'] = 0,0
        postsynaptic['MVR01'] = 0,0
        postsynaptic['MVR02'] = 0,0
        postsynaptic['MVR03'] = 0,0
        postsynaptic['MVR04'] = 0,0
        postsynaptic['MVR05'] = 0,0
        postsynaptic['MVR06'] = 0,0
        postsynaptic['MVR07'] = 0,0
        postsynaptic['MVR08'] = 0,0
        postsynaptic['MVR09'] = 0,0
        postsynaptic['MVR10'] = 0,0
        postsynaptic['MVR11'] = 0,0
        postsynaptic['MVR12'] = 0,0
        postsynaptic['MVR13'] = 0,0
        postsynaptic['MVR14'] = 0,0
        postsynaptic['MVR15'] = 0,0
        postsynaptic['MVR16'] = 0,0
        postsynaptic['MVR17'] = 0,0
        postsynaptic['MVR18'] = 0,0
        postsynaptic['MVR19'] = 0,0
        postsynaptic['MVR20'] = 0,0
        postsynaptic['MVR21'] = 0,0
        postsynaptic['MVR22'] = 0,0
        postsynaptic['MVR23'] = 0,0
        postsynaptic['MVR24'] = 0,0
        postsynaptic['MVULVA'] = 0,0
        postsynaptic['NSML'] = 0,0
        postsynaptic['NSMR'] = 0,0
        postsynaptic['OLLL'] = 0,0
        postsynaptic['OLLR'] = 0,0
        postsynaptic['OLQDL'] = 0,0
        postsynaptic['OLQDR'] = 0,0
        postsynaptic['OLQVL'] = 0,0
        postsynaptic['OLQVR'] = 0,0
        postsynaptic['PDA'] = 0,0
        postsynaptic['PDB'] = 0,0
        postsynaptic['PDEL'] = 0,0
        postsynaptic['PDER'] = 0,0
        postsynaptic['PHAL'] = 0,0
        postsynaptic['PHAR'] = 0,0
        postsynaptic['PHBL'] = 0,0
        postsynaptic['PHBR'] = 0,0
        postsynaptic['PHCL'] = 0,0
        postsynaptic['PHCR'] = 0,0
        postsynaptic['PLML'] = 0,0
        postsynaptic['PLMR'] = 0,0
        postsynaptic['PLNL'] = 0,0
        postsynaptic['PLNR'] = 0,0
        postsynaptic['PQR'] = 0,0
        postsynaptic['PVCL'] = 0,0
        postsynaptic['PVCR'] = 0,0
        postsynaptic['PVDL'] = 0,0
        postsynaptic['PVDR'] = 0,0
        postsynaptic['PVM'] = 0,0
        postsynaptic['PVNL'] = 0,0
        postsynaptic['PVNR'] = 0,0
        postsynaptic['PVPL'] = 0,0
        postsynaptic['PVPR'] = 0,0
        postsynaptic['PVQL'] = 0,0
        postsynaptic['PVQR'] = 0,0
        postsynaptic['PVR'] = 0,0
        postsynaptic['PVT'] = 0,0
        postsynaptic['PVWL'] = 0,0
        postsynaptic['PVWR'] = 0,0
        postsynaptic['RIAL'] = 0,0
        postsynaptic['RIAR'] = 0,0
        postsynaptic['RIBL'] = 0,0
        postsynaptic['RIBR'] = 0,0
        postsynaptic['RICL'] = 0,0
        postsynaptic['RICR'] = 0,0
        postsynaptic['RID'] = 0,0
        postsynaptic['RIFL'] = 0,0
        postsynaptic['RIFR'] = 0,0
        postsynaptic['RIGL'] = 0,0
        postsynaptic['RIGR'] = 0,0
        postsynaptic['RIH'] = 0,0
        postsynaptic['RIML'] = 0,0
        postsynaptic['RIMR'] = 0,0
        postsynaptic['RIPL'] = 0,0
        postsynaptic['RIPR'] = 0,0
        postsynaptic['RIR'] = 0,0
        postsynaptic['RIS'] = 0,0
        postsynaptic['RIVL'] = 0,0
        postsynaptic['RIVR'] = 0,0
        postsynaptic['RMDDL'] = 0,0
        postsynaptic['RMDDR'] = 0,0
        postsynaptic['RMDL'] = 0,0
        postsynaptic['RMDR'] = 0,0
        postsynaptic['RMDVL'] = 0,0
        postsynaptic['RMDVR'] = 0,0
        postsynaptic['RMED'] = 0,0
        postsynaptic['RMEL'] = 0,0
        postsynaptic['RMER'] = 0,0
        postsynaptic['RMEV'] = 0,0
        postsynaptic['RMFL'] = 0,0
        postsynaptic['RMFR'] = 0,0
        postsynaptic['RMGL'] = 0,0
        postsynaptic['RMGR'] = 0,0
        postsynaptic['RMHL'] = 0,0
        postsynaptic['RMHR'] = 0,0
        postsynaptic['SAADL'] = 0,0
        postsynaptic['SAADR'] = 0,0
        postsynaptic['SAAVL'] = 0,0
        postsynaptic['SAAVR'] = 0,0
        postsynaptic['SABD'] = 0,0
        postsynaptic['SABVL'] = 0,0
        postsynaptic['SABVR'] = 0,0
        postsynaptic['SDQL'] = 0,0
        postsynaptic['SDQR'] = 0,0
        postsynaptic['SIADL'] = 0,0
        postsynaptic['SIADR'] = 0,0
        postsynaptic['SIAVL'] = 0,0
        postsynaptic['SIAVR'] = 0,0
        postsynaptic['SIBDL'] = 0,0
        postsynaptic['SIBDR'] = 0,0
        postsynaptic['SIBVL'] = 0,0
        postsynaptic['SIBVR'] = 0,0
        postsynaptic['SMBDL'] = 0,0
        postsynaptic['SMBDR'] = 0,0
        postsynaptic['SMBVL'] = 0,0
        postsynaptic['SMBVR'] = 0,0
        postsynaptic['SMDDL'] = 0,0
        postsynaptic['SMDDR'] = 0,0
        postsynaptic['SMDVL'] = 0,0
        postsynaptic['SMDVR'] = 0,0
        postsynaptic['URADL'] = 0,0
        postsynaptic['URADR'] = 0,0
        postsynaptic['URAVL'] = 0,0
        postsynaptic['URAVR'] = 0,0
        postsynaptic['URBL'] = 0,0
        postsynaptic['URBR'] = 0,0
        postsynaptic['URXL'] = 0,0
        postsynaptic['URXR'] = 0,0
        postsynaptic['URYDL'] = 0,0
        postsynaptic['URYDR'] = 0,0
        postsynaptic['URYVL'] = 0,0
        postsynaptic['URYVR'] = 0,0
        postsynaptic['VA1'] = 0,0
        postsynaptic['VA10'] = 0,0
        postsynaptic['VA11'] = 0,0
        postsynaptic['VA12'] = 0,0
        postsynaptic['VA2'] = 0,0
        postsynaptic['VA3'] = 0,0
        postsynaptic['VA4'] = 0,0
        postsynaptic['VA5'] = 0,0
        postsynaptic['VA6'] = 0,0
        postsynaptic['VA7'] = 0,0
        postsynaptic['VA8'] = 0,0
        postsynaptic['VA9'] = 0,0
        postsynaptic['VB1'] = 0,0
        postsynaptic['VB10'] = 0,0
        postsynaptic['VB11'] = 0,0
        postsynaptic['VB2'] = 0,0
        postsynaptic['VB3'] = 0,0
        postsynaptic['VB4'] = 0,0
        postsynaptic['VB5'] = 0,0
        postsynaptic['VB6'] = 0,0
        postsynaptic['VB7'] = 0,0
        postsynaptic['VB8'] = 0,0
        postsynaptic['VB9'] = 0,0
        postsynaptic['VC1'] = 0,0
        postsynaptic['VC2'] = 0,0
        postsynaptic['VC3'] = 0,0
        postsynaptic['VC4'] = 0,0
        postsynaptic['VC5'] = 0,0
        postsynaptic['VC6'] = 0,0
        postsynaptic['VD1'] = 0,0
        postsynaptic['VD10'] = 0,0
        postsynaptic['VD11'] = 0,0
        postsynaptic['VD12'] = 0,0
        postsynaptic['VD13'] = 0,0
        postsynaptic['VD2'] = 0,0
        postsynaptic['VD3'] = 0,0
        postsynaptic['VD4'] = 0,0
        postsynaptic['VD5'] = 0,0
        postsynaptic['VD6'] = 0,0
        postsynaptic['VD7'] = 0,0
        postsynaptic['VD8'] = 0,0
        postsynaptic['VD9'] = 0,0

#global postsynapticNext = copy.deepcopy(postsynaptic)

def motorcontrol():
        global accumright
        global accumleft

        # accumulate left and right muscles and the accumulated values are
        # used to move the left and right motors of the robot
        for pscheck in postsynaptic:
                if pscheck[thisState] in musDleft or pscheck[thisState] in musVleft:
                   accumleft += postsynaptic[pscheck][thisState]
                   postsynaptic[pscheck][thisState] = 0                 #Both states have to be set to 0 once the muscle is fired, or
                   postsynaptic[pscheck][nextState] = 0                 # it will keep returning beyond the threshold within one iteration.
                elif pscheck[thisState] in musDright or pscheck[thisState] in musVright:
                   accumright += postsynaptic[pscheck]
                   postsynaptic[pscheck][thisState] = 0
                   postsynaptic[pscheck][nextState] = 0
        # We turn the wheels according to the motor weight accumulation
        new_speed = abs(accumleft) + abs(accumright)
        if new_speed > 150:
                new_speed = 150
        elif new_speed < 75:
                new_speed = 75
        print "Left: ", accumleft, "Right:", accumright, "Speed: ", new_speed
        ## Start Commented section
        set_speed(new_speed)
        if accumleft == 0 and accumright == 0:
                stop()
        elif accumright <= 0 and accumleft < 0:
                set_speed(150)
                turnratio = float(accumright) / float(accumleft)
                # print "Turn Ratio: ", turnratio
                if turnratio <= 0.6:
                         left_rot()
                         time.sleep(0.8)
                elif turnratio >= 2:
                         right_rot()
                         time.sleep(0.8)
                bwd()
                time.sleep(0.5)
        elif accumright <= 0 and accumleft >= 0:
                right_rot()
                time.sleep(.8)
        elif accumright >= 0 and accumleft <= 0:
                left_rot()
                time.sleep(.8)
        elif accumright >= 0 and accumleft > 0:
                turnratio = float(accumright) / float(accumleft)
                # print "Turn Ratio: ", turnratio
                if turnratio <= 0.6:
                         left_rot()
                         time.sleep(0.8)
                elif turnratio >= 2:
                         right_rot()
                         time.sleep(0.8)
                fwd()
                time.sleep(0.5)
        else:
                stop()
         ## End Commented section
        accumleft = 0
        accumright = 0
        time.sleep(0.5)


def dendriteAccumulate(dneuron):
        f = eval(dneuron)
        f()

def fireNeuron(fneuron):
        # The threshold has been exceeded and we fire the neurite
        if fneuron != "MVULVA":
                f = eval(fneuron)
                f()

def runconnectome():
        # Each time a set of neuron is stimulated, this method will execute
        # The weigted values are accumulated in the PostSynaptic array
        # Once the accumulation is read, we see what neurons are greater
        # then the threshold and fire the neuron or muscle that has exceeded
        # the threshold 

        for ps in postsynaptic:
                if ps[:3] not in muscles and abs(postsynaptic[ps]) > threshold:
                        fireNeuron(ps)
                        postsynaptic[ps] = 0
        motorcontrol()
        thisState,nextState=nextState,thisState    
                         

# Create the dictionary      
createpostsynaptic()
dist=0
set_speed(120)
print "Voltage: ", volt()
tfood = 0
try:
### Here is where you would put in a method to stimulate the neurons ###
### We stimulate chemosensory neurons constantly unless nose touch   ###
### (sonar) is stimulated and then we fire nose touch neurites       ###
### Use CNTRL-C to stop the program
    while True:
        ## Start comment - use a fixed value if you want to stimulte nose touch
        ## use something like "dist = 27" if you want to stop nose stimulation
        dist = us_dist(15)
        ## End Comment

        #Do we need to switch states at the end of each loop? No, this is done inside the runconnectome()
        #function, called inside each loop.
        if dist>0 and dist<30:
            print "OBSTACLE (Nose Touch)", dist 
            dendriteAccumulate("FLPR")
            dendriteAccumulate("FLPL")
            dendriteAccumulate("ASHL")
            dendriteAccumulate("ASHR")
            dendriteAccumulate("IL1VL")
            dendriteAccumulate("IL1VR")
            dendriteAccumulate("OLQDL")
            dendriteAccumulate("OLQDR")
            dendriteAccumulate("OLQVR")
            dendriteAccumulate("OLQVL")
            runconnectome()
        else:
            if tfood < 2:
                    print "FOOD"
                    dendriteAccumulate("ADFL")
                    dendriteAccumulate("ADFR")
                    dendriteAccumulate("ASGR")
                    dendriteAccumulate("ASGL")
                    dendriteAccumulate("ASIL")
                    dendriteAccumulate("ASIR")
                    dendriteAccumulate("ASJR")
                    dendriteAccumulate("ASJL")
                    runconnectome()
                    time.sleep(0.5)
            tfood += 0.5
            if (tfood > 20):
                    tfood = 0
        

       
except KeyboardInterrupt:
    ## Start Comment
    stop()
    ## End Comment
    print "Ctrl+C detected. Program Stopped!"
    

