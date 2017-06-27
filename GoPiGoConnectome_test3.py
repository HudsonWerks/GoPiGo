# GoPiGo Connectome
# Written by Timothy Busbice, Gabriel Garrett, Geoffrey Churchill (c) 2014, in Python 2.7
# The GoPiGo Connectome uses a Postsynaptic dictionary based on the C Elegans Connectome Model
# This application can be ran on the Raspberry Pi GoPiGo robot with a Sonar that represents Nose Touch when activated
# To run standalone without a GoPiGo robot, simply comment out the sections with Start and End comments
# Modifications by Charles Hamilton
## Start Comment
from gopigo import *
## End Comment

##IMPORT CAH - dictionary library
import connectlib

#IMPORT CAH - process and system functions
import subprocess
import os
import sys


# The postsynaptic dictionary contains the accumulated weighted values as the
# connectome is executed
postsynaptic = {}

global thisState
global nextState
thisState = 0
nextState = 1

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
# arr=postsynaptic['AIBR'] potential optimization

# def ADAL():
#         postsynaptic['ADAR'][nextState] = 2 + postsynaptic['ADAR'][thisState]
#         postsynaptic['ADFL'][nextState] = 1 + postsynaptic['ADFL'][thisState]
#         postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
#         postsynaptic['AIBR'][nextState] = 2 + postsynaptic['AIBR'][thisState]
#         postsynaptic['ASHL'][nextState] = 1 + postsynaptic['ASHL'][thisState]
#         postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
#         postsynaptic['AVBL'][nextState] = 4 + postsynaptic['AVBL'][thisState]
#         postsynaptic['AVBR'][nextState] = 7 + postsynaptic['AVBR'][thisState]
#         postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
#         postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
#         postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
#         postsynaptic['AVJR'][nextState] = 5 + postsynaptic['AVJR'][thisState]
#         postsynaptic['FLPR'][nextState] = 1 + postsynaptic['FLPR'][thisState]
#         postsynaptic['PVQL'][nextState] = 1 + postsynaptic['PVQL'][thisState]
#         postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
#         postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
#         postsynaptic['RIML'][nextState] = 3 + postsynaptic['RIML'][thisState]
#         postsynaptic['RIPL'][nextState] = 1 + postsynaptic['RIPL'][thisState]
#         postsynaptic['SMDVR'][nextState] = 2 + postsynaptic['SMDVR'][thisState]
#
# def ADAR():
#         postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
#
# def ADEL():
# def ADER():
# def ADFL():
# def ADFR():
# def ADLL():
# def ADLR():
# def AFDL():
# def AFDR():
# def AIAL():
# def AIAR():
# def AIBL():
# def AIBR():
# def AIML():
# def AIMR():
# def AINL():
# def AINR():
# def AIYL():
# def AIYR():
# def AIZL():
# def AIZR():
# def ALA():
# def ALML():
# def ALMR():
# def ALNL():
# def ALNR():
# def AQR():
# def AS1():
# def AS2():
# def AS3():
# def AS4():
# def AS5():
# def AS6():
# def AS7():
# def AS8():
# def AS9():
# def AS10():
# def AS11():
# def ASEL():
# def ASER():
# def ASGL():
# def ASGR():
# def ASHL():
# def ASHR():
# def ASIL():
# def ASIR():
# def ASJL():
# def ASJR():
# def ASKL():
# def ASKR():
# def AUAL():
# def AUAR():
# def AVAL():
# def AVAR():
# def AVBL():
# def AVBR():
# def AVDL():
# def AVDR():
# def AVEL():
# def AVER():
# def AVFL():
# def AVFR():
# def AVG():
# def AVHL():
# def AVHR():
# def AVJL():
# def AVJR():
# def AVKL():
# def AVKR():
# def AVL():
# def AVM():
# def AWAL():
# def AWAR():
# def AWBL():
# def AWBR():
# def AWCL():
# def AWCR():
# def BAGL():
# def BAGR():
# def BDUL():
# def BDUR():
# def CEPDL():
# def CEPDR():
# def CEPVL():
# def CEPVR():
# def DA1():
# def DA2():
# def DA3():
# def DA4():
# def DA5():
# def DA6():
# def DA7():
# def DA8():
# def DA9():
# def DB1():
# def DB2():
# def DB3():
# def DB4():
# def DB5():
# def DB6():
# def DB7():
# def DD1():
# def DD2():
# def DD3():
# def DD4():
# def DD5():
# def DD6():
# def DVA():
# def DVB():
# def DVC():
# def FLPL():
# def FLPR():
# def HSNL():
# def HSNR():
# def I1L():
# def I1R():
# def I2L():
# def I2R():
# def I3():
# def I4():
# def I5():
# def I6():
# def IL1DL():
# def IL1DR():
# def IL1L():
# def IL1R():
# def IL1VL():
# def IL1VR():
# def IL2DL():
# def IL2DR():
# def IL2L():
# def IL2R():
# def IL2VL():
# def IL2VR():
# def LUAL():
# def LUAR():
# def M1():
# def M2L():
# def M2R():
# def M3L():
# def M3R():
# def M4():
# def M5():
# def MCL():
# def MCR():
# def MI():
# def NSML():
# def NSMR():
# def OLLL():
# def OLLR():
# def OLQDL():
# def OLQDR():
# def OLQVL():
# def OLQVR():
# def PDA():
# def PDB():
# def PDEL():
# def PDER():
# def PHAL():
# def PHAR():
# def PHBL():
# def PHBR():
# def PHCL():
# def PHCR():
# def PLML():
# def PLMR():
# def PLNL():
# def PLNR():
# def PQR():
# def PVCL():
# def PVCR():
# def PVDL():
# def PVDR():
'# def PVM():
# def PVNL():
# def PVNR():
# def PVPL():
# def PVPR():
# def PVQL():
# def PVQR():
# def PVR():
# def PVT():
# def PVWL():
# def PVWR():
# def RIAL():
# def RIAR():
# def RIBL():
# def RIBR():
# def RICL():
# def RICR():
# def RID():
# def RIFL():
# def RIFR():
# def RIGL():
# def RIGR():
# def RIH():
# def RIML():
# def RIMR():
# def RIPL():
# def RIPR():
# def RIR():
# def RIS():
# def RIVL():
# def RIVR():
# def RMDDL():
# def RMDDR():
# def RMDL():
# def RMDR():
# def RMDVL():
# def RMDVR():
# def RMED():
# def RMEL():
# def RMER():
# def RMEV():
# def RMFL():
# def RMFR():
# def RMGL():
# def RMGR():
# def RMHL():
# def RMHR():
# def SAADL():
# def SAADR():
# def SAAVL():
# def SAAVR():
# def SABD():
# def SABVL():
# def SABVR():
# def SDQL():
# def SDQR():
# def SIADL():
# def SIADR():
# def SIAVR():
# def SIBDL():
# def SIBDR():
# def SIBVL():
# def SIBVR():
# def SMBDL():
# def SMDVR():
# def URADL():
# def URYVR():
# def VA1():
# def VA12():
# def VB1():
# def VB11():
# def VC1():
# def VC2():
# def VC3():
# def VC4():
# def VC5():
# def VC6():
# def VD1():
# def VD2():
# def VD3():
# def VD4():
# def VD5():
# def VD6():
# def VD7():
# def VD8():
# def VD9():
# def VD10():
# def VD11():
# def VD12():
# def VD13():

# def createpostsynaptic():
#         # The PostSynaptic dictionary maintains the accumulated values for
#         # each neuron and muscle. The Accumulated values are initialized to Zero
#         postsynaptic['ADAL'] = [0,0]
#         postsynaptic['ADAR'] = [0,0]
#         postsynaptic['ADEL'] = [0,0]
#         postsynaptic['ADER'] = [0,0]
#         postsynaptic['ADFL'] = [0,0]
#         postsynaptic['ADFR'] = [0,0]
#         postsynaptic['ADLL'] = [0,0]
#         postsynaptic['ADLR'] = [0,0]
#         postsynaptic['AFDL'] = [0,0]
#         postsynaptic['AFDR'] = [0,0]
#         postsynaptic['AIAL'] = [0,0]
#         postsynaptic['AIAR'] = [0,0]
#         postsynaptic['AIBL'] = [0,0]
#         postsynaptic['AIBR'] = [0,0]
#         postsynaptic['AIML'] = [0,0]
#         postsynaptic['AIMR'] = [0,0]
#         postsynaptic['AINL'] = [0,0]
#         postsynaptic['AINR'] = [0,0]
#         postsynaptic['AIYL'] = [0,0]
#         postsynaptic['AIYR'] = [0,0]
#         postsynaptic['AIZL'] = [0,0]
#         postsynaptic['AIZR'] = [0,0]
#         postsynaptic['ALA'] = [0,0]
#         postsynaptic['ALML'] = [0,0]
#         postsynaptic['ALMR'] = [0,0]
#         postsynaptic['ALNL'] = [0,0]
#         postsynaptic['ALNR'] = [0,0]
#         postsynaptic['AQR'] = [0,0]
#         postsynaptic['AS1'] = [0,0]
#         postsynaptic['AS10'] = [0,0]
#         postsynaptic['AS11'] = [0,0]
#         postsynaptic['AS2'] = [0,0]
#         postsynaptic['AS3'] = [0,0]
#         postsynaptic['AS4'] = [0,0]
#         postsynaptic['AS5'] = [0,0]
#         postsynaptic['AS6'] = [0,0]
#         postsynaptic['AS7'] = [0,0]
#         postsynaptic['AS8'] = [0,0]
#         postsynaptic['AS9'] = [0,0]
#         postsynaptic['ASEL'] = [0,0]
#         postsynaptic['ASER'] = [0,0]
#         postsynaptic['ASGL'] = [0,0]
#         postsynaptic['ASGR'] = [0,0]
#         postsynaptic['ASHL'] = [0,0]
#         postsynaptic['ASHR'] = [0,0]
#         postsynaptic['ASIL'] = [0,0]
#         postsynaptic['ASIR'] = [0,0]
#         postsynaptic['ASJL'] = [0,0]
#         postsynaptic['ASJR'] = [0,0]
#         postsynaptic['ASKL'] = [0,0]
#         postsynaptic['ASKR'] = [0,0]
#         postsynaptic['AUAL'] = [0,0]
#         postsynaptic['AUAR'] = [0,0]
#         postsynaptic['AVAL'] = [0,0]
#         postsynaptic['AVAR'] = [0,0]
#         postsynaptic['AVBL'] = [0,0]
#         postsynaptic['AVBR'] = [0,0]
#         postsynaptic['AVDL'] = [0,0]
#         postsynaptic['AVDR'] = [0,0]
#         postsynaptic['AVEL'] = [0,0]
#         postsynaptic['AVER'] = [0,0]
#         postsynaptic['AVFL'] = [0,0]
#         postsynaptic['AVFR'] = [0,0]
#         postsynaptic['AVG'] = [0,0]
#         postsynaptic['AVHL'] = [0,0]
#         postsynaptic['AVHR'] = [0,0]
#         postsynaptic['AVJL'] = [0,0]
#         postsynaptic['AVJR'] = [0,0]
#         postsynaptic['AVKL'] = [0,0]
#         postsynaptic['AVKR'] = [0,0]
#         postsynaptic['AVL'] = [0,0]
#         postsynaptic['AVM'] = [0,0]
#         postsynaptic['AWAL'] = [0,0]
#         postsynaptic['AWAR'] = [0,0]
#         postsynaptic['AWBL'] = [0,0]
#         postsynaptic['AWBR'] = [0,0]
#         postsynaptic['AWCL'] = [0,0]
#         postsynaptic['AWCR'] = [0,0]
#         postsynaptic['BAGL'] = [0,0]
#         postsynaptic['BAGR'] = [0,0]
#         postsynaptic['BDUL'] = [0,0]
#         postsynaptic['BDUR'] = [0,0]
#         postsynaptic['CEPDL'] = [0,0]
#         postsynaptic['CEPDR'] = [0,0]
#         postsynaptic['CEPVL'] = [0,0]
#         postsynaptic['CEPVR'] = [0,0]
#         postsynaptic['DA1'] = [0,0]
#         postsynaptic['DA2'] = [0,0]
#         postsynaptic['DA3'] = [0,0]
#         postsynaptic['DA4'] = [0,0]
#         postsynaptic['DA5'] = [0,0]
#         postsynaptic['DA6'] = [0,0]
#         postsynaptic['DA7'] = [0,0]
#         postsynaptic['DA8'] = [0,0]
#         postsynaptic['DA9'] = [0,0]
#         postsynaptic['DB1'] = [0,0]
#         postsynaptic['DB2'] = [0,0]
#         postsynaptic['DB3'] = [0,0]
#         postsynaptic['DB4'] = [0,0]
#         postsynaptic['DB5'] = [0,0]
#         postsynaptic['DB6'] = [0,0]
#         postsynaptic['DB7'] = [0,0]
#         postsynaptic['DD1'] = [0,0]
#         postsynaptic['DD2'] = [0,0]
#         postsynaptic['DD3'] = [0,0]
#         postsynaptic['DD4'] = [0,0]
#         postsynaptic['DD5'] = [0,0]
#         postsynaptic['DD6'] = [0,0]
#         postsynaptic['DVA'] = [0,0]
#         postsynaptic['DVB'] = [0,0]
#         postsynaptic['DVC'] = [0,0]
#         postsynaptic['FLPL'] = [0,0]
#         postsynaptic['FLPR'] = [0,0]
#         postsynaptic['HSNL'] = [0,0]
#         postsynaptic['HSNR'] = [0,0]
#         postsynaptic['I1L'] = [0,0]
#         postsynaptic['I1R'] = [0,0]
#         postsynaptic['I2L'] = [0,0]
#         postsynaptic['I2R'] = [0,0]
#         postsynaptic['I3'] = [0,0]
#         postsynaptic['I4'] = [0,0]
#         postsynaptic['I5'] = [0,0]
#         postsynaptic['I6'] = [0,0]
#         postsynaptic['IL1DL'] = [0,0]
#         postsynaptic['IL1DR'] = [0,0]
#         postsynaptic['IL1L'] = [0,0]
#         postsynaptic['IL1R'] = [0,0]
#         postsynaptic['IL1VL'] = [0,0]
#         postsynaptic['IL1VR'] = [0,0]
#         postsynaptic['IL2L'] = [0,0]
#         postsynaptic['IL2R'] = [0,0]
#         postsynaptic['IL2DL'] = [0,0]
#         postsynaptic['IL2DR'] = [0,0]
#         postsynaptic['IL2VL'] = [0,0]
#         postsynaptic['IL2VR'] = [0,0]
#         postsynaptic['LUAL'] = [0,0]
#         postsynaptic['LUAR'] = [0,0]
#         postsynaptic['M1'] = [0,0]
#         postsynaptic['M2L'] = [0,0]
#         postsynaptic['M2R'] = [0,0]
#         postsynaptic['M3L'] = [0,0]
#         postsynaptic['M3R'] = [0,0]
#         postsynaptic['M4'] = [0,0]
#         postsynaptic['M5'] = [0,0]
#         postsynaptic['MANAL'] = [0,0]
#         postsynaptic['MCL'] = [0,0]
#         postsynaptic['MCR'] = [0,0]
#         postsynaptic['MDL01'] = [0,0]
#         postsynaptic['MDL02'] = [0,0]
#         postsynaptic['MDL03'] = [0,0]
#         postsynaptic['MDL04'] = [0,0]
#         postsynaptic['MDL05'] = [0,0]
#         postsynaptic['MDL06'] = [0,0]
#         postsynaptic['MDL07'] = [0,0]
#         postsynaptic['MDL08'] = [0,0]
#         postsynaptic['MDL09'] = [0,0]
#         postsynaptic['MDL10'] = [0,0]
#         postsynaptic['MDL11'] = [0,0]
#         postsynaptic['MDL12'] = [0,0]
#         postsynaptic['MDL13'] = [0,0]
#         postsynaptic['MDL14'] = [0,0]
#         postsynaptic['MDL15'] = [0,0]
#         postsynaptic['MDL16'] = [0,0]
#         postsynaptic['MDL17'] = [0,0]
#         postsynaptic['MDL18'] = [0,0]
#         postsynaptic['MDL19'] = [0,0]
#         postsynaptic['MDL20'] = [0,0]
#         postsynaptic['MDL21'] = [0,0]
#         postsynaptic['MDL22'] = [0,0]
#         postsynaptic['MDL23'] = [0,0]
#         postsynaptic['MDL24'] = [0,0]
#         postsynaptic['MDR01'] = [0,0]
#         postsynaptic['MDR02'] = [0,0]
#         postsynaptic['MDR03'] = [0,0]
#         postsynaptic['MDR04'] = [0,0]
#         postsynaptic['MDR05'] = [0,0]
#         postsynaptic['MDR06'] = [0,0]
#         postsynaptic['MDR07'] = [0,0]
#         postsynaptic['MDR08'] = [0,0]
#         postsynaptic['MDR09'] = [0,0]
#         postsynaptic['MDR10'] = [0,0]
#         postsynaptic['MDR11'] = [0,0]
#         postsynaptic['MDR12'] = [0,0]
#         postsynaptic['MDR13'] = [0,0]
#         postsynaptic['MDR14'] = [0,0]
#         postsynaptic['MDR15'] = [0,0]
#         postsynaptic['MDR16'] = [0,0]
#         postsynaptic['MDR17'] = [0,0]
#         postsynaptic['MDR18'] = [0,0]
#         postsynaptic['MDR19'] = [0,0]
#         postsynaptic['MDR20'] = [0,0]
#         postsynaptic['MDR21'] = [0,0]
#         postsynaptic['MDR22'] = [0,0]
#         postsynaptic['MDR23'] = [0,0]
#         postsynaptic['MDR24'] = [0,0]
#         postsynaptic['MI'] = [0,0]
#         postsynaptic['MVL01'] = [0,0]
#         postsynaptic['MVL02'] = [0,0]
#         postsynaptic['MVL03'] = [0,0]
#         postsynaptic['MVL04'] = [0,0]
#         postsynaptic['MVL05'] = [0,0]
#         postsynaptic['MVL06'] = [0,0]
#         postsynaptic['MVL07'] = [0,0]
#         postsynaptic['MVL08'] = [0,0]
#         postsynaptic['MVL09'] = [0,0]
#         postsynaptic['MVL10'] = [0,0]
#         postsynaptic['MVL11'] = [0,0]
#         postsynaptic['MVL12'] = [0,0]
#         postsynaptic['MVL13'] = [0,0]
#         postsynaptic['MVL14'] = [0,0]
#         postsynaptic['MVL15'] = [0,0]
#         postsynaptic['MVL16'] = [0,0]
#         postsynaptic['MVL17'] = [0,0]
#         postsynaptic['MVL18'] = [0,0]
#         postsynaptic['MVL19'] = [0,0]
#         postsynaptic['MVL20'] = [0,0]
#         postsynaptic['MVL21'] = [0,0]
#         postsynaptic['MVL22'] = [0,0]
#         postsynaptic['MVL23'] = [0,0]
#         postsynaptic['MVR01'] = [0,0]
#         postsynaptic['MVR02'] = [0,0]
#         postsynaptic['MVR03'] = [0,0]
#         postsynaptic['MVR04'] = [0,0]
#         postsynaptic['MVR05'] = [0,0]
#         postsynaptic['MVR06'] = [0,0]
#         postsynaptic['MVR07'] = [0,0]
#         postsynaptic['MVR08'] = [0,0]
#         postsynaptic['MVR09'] = [0,0]
#         postsynaptic['MVR10'] = [0,0]
#         postsynaptic['MVR11'] = [0,0]
#         postsynaptic['MVR12'] = [0,0]
#         postsynaptic['MVR13'] = [0,0]
#         postsynaptic['MVR14'] = [0,0]
#         postsynaptic['MVR15'] = [0,0]
#         postsynaptic['MVR16'] = [0,0]
#         postsynaptic['MVR17'] = [0,0]
#         postsynaptic['MVR18'] = [0,0]
#         postsynaptic['MVR19'] = [0,0]
#         postsynaptic['MVR20'] = [0,0]
#         postsynaptic['MVR21'] = [0,0]
#         postsynaptic['MVR22'] = [0,0]
#         postsynaptic['MVR23'] = [0,0]
#         postsynaptic['MVR24'] = [0,0]
#         postsynaptic['MVULVA'] = [0,0]
#         postsynaptic['NSML'] = [0,0]
#         postsynaptic['NSMR'] = [0,0]
#         postsynaptic['OLLL'] = [0,0]
#         postsynaptic['OLLR'] = [0,0]
#         postsynaptic['OLQDL'] = [0,0]
#         postsynaptic['OLQDR'] = [0,0]
#         postsynaptic['OLQVL'] = [0,0]
#         postsynaptic['OLQVR'] = [0,0]
#         postsynaptic['PDA'] = [0,0]
#         postsynaptic['PDB'] = [0,0]
#         postsynaptic['PDEL'] = [0,0]
#         postsynaptic['PDER'] = [0,0]
#         postsynaptic['PHAL'] = [0,0]
#         postsynaptic['PHAR'] = [0,0]
#         postsynaptic['PHBL'] = [0,0]
#         postsynaptic['PHBR'] = [0,0]
#         postsynaptic['PHCL'] = [0,0]
#         postsynaptic['PHCR'] = [0,0]
#         postsynaptic['PLML'] = [0,0]
#         postsynaptic['PLMR'] = [0,0]
#         postsynaptic['PLNL'] = [0,0]
#         postsynaptic['PLNR'] = [0,0]
#         postsynaptic['PQR'] = [0,0]
#         postsynaptic['PVCL'] = [0,0]
#         postsynaptic['PVCR'] = [0,0]
#         postsynaptic['PVDL'] = [0,0]
#         postsynaptic['PVDR'] = [0,0]
#         postsynaptic['PVM'] = [0,0]
#         postsynaptic['PVNL'] = [0,0]
#         postsynaptic['PVNR'] = [0,0]
#         postsynaptic['PVPL'] = [0,0]
#         postsynaptic['PVPR'] = [0,0]
#         postsynaptic['PVQL'] = [0,0]
#         postsynaptic['PVQR'] = [0,0]
#         postsynaptic['PVR'] = [0,0]
#         postsynaptic['PVT'] = [0,0]
#         postsynaptic['PVWL'] = [0,0]
#         postsynaptic['PVWR'] = [0,0]
#         postsynaptic['RIAL'] = [0,0]
#         postsynaptic['RIAR'] = [0,0]
#         postsynaptic['RIBL'] = [0,0]
#         postsynaptic['RIBR'] = [0,0]
#         postsynaptic['RICL'] = [0,0]
#         postsynaptic['RICR'] = [0,0]
#         postsynaptic['RID'] = [0,0]
#         postsynaptic['RIFL'] = [0,0]
#         postsynaptic['RIFR'] = [0,0]
#         postsynaptic['RIGL'] = [0,0]
#         postsynaptic['RIGR'] = [0,0]
#         postsynaptic['RIH'] = [0,0]
#         postsynaptic['RIML'] = [0,0]
#         postsynaptic['RIMR'] = [0,0]
#         postsynaptic['RIPL'] = [0,0]
#         postsynaptic['RIPR'] = [0,0]
#         postsynaptic['RIR'] = [0,0]
#         postsynaptic['RIS'] = [0,0]
#         postsynaptic['RIVL'] = [0,0]
#         postsynaptic['RIVR'] = [0,0]
#         postsynaptic['RMDDL'] = [0,0]
#         postsynaptic['RMDDR'] = [0,0]
#         postsynaptic['RMDL'] = [0,0]
#         postsynaptic['RMDR'] = [0,0]
#         postsynaptic['RMDVL'] = [0,0]
#         postsynaptic['RMDVR'] = [0,0]
#         postsynaptic['RMED'] = [0,0]
#         postsynaptic['RMEL'] = [0,0]
#         postsynaptic['RMER'] = [0,0]
#         postsynaptic['RMEV'] = [0,0]
#         postsynaptic['RMFL'] = [0,0]
#         postsynaptic['RMFR'] = [0,0]
#         postsynaptic['RMGL'] = [0,0]
#         postsynaptic['RMGR'] = [0,0]
#         postsynaptic['RMHL'] = [0,0]
#         postsynaptic['RMHR'] = [0,0]
#         postsynaptic['SAADL'] = [0,0]
#         postsynaptic['SAADR'] = [0,0]
#         postsynaptic['SAAVL'] = [0,0]
#         postsynaptic['SAAVR'] = [0,0]
#         postsynaptic['SABD'] = [0,0]
#         postsynaptic['SABVL'] = [0,0]
#         postsynaptic['SABVR'] = [0,0]
#         postsynaptic['SDQL'] = [0,0]
#         postsynaptic['SDQR'] = [0,0]
#         postsynaptic['SIADL'] = [0,0]
#         postsynaptic['SIADR'] = [0,0]
#         postsynaptic['SIAVL'] = [0,0]
#         postsynaptic['SIAVR'] = [0,0]
#         postsynaptic['SIBDL'] = [0,0]
#         postsynaptic['SIBDR'] = [0,0]
#         postsynaptic['SIBVL'] = [0,0]
#         postsynaptic['SIBVR'] = [0,0]
#         postsynaptic['SMBDL'] = [0,0]
#         postsynaptic['SMBDR'] = [0,0]
#         postsynaptic['SMBVL'] = [0,0]
#         postsynaptic['SMBVR'] = [0,0]
#         postsynaptic['SMDDL'] = [0,0]
#         postsynaptic['SMDDR'] = [0,0]
#         postsynaptic['SMDVL'] = [0,0]
#         postsynaptic['SMDVR'] = [0,0]
#         postsynaptic['URADL'] = [0,0]
#         postsynaptic['URADR'] = [0,0]
#         postsynaptic['URAVL'] = [0,0]
#         postsynaptic['URAVR'] = [0,0]
#         postsynaptic['URBL'] = [0,0]
#         postsynaptic['URBR'] = [0,0]
#         postsynaptic['URXL'] = [0,0]
#         postsynaptic['URXR'] = [0,0]
#         postsynaptic['URYDL'] = [0,0]
#         postsynaptic['URYDR'] = [0,0]
#         postsynaptic['URYVL'] = [0,0]
#         postsynaptic['URYVR'] = [0,0]
#         postsynaptic['VA1'] = [0,0]
#         postsynaptic['VA10'] = [0,0]
#         postsynaptic['VA11'] = [0,0]
#         postsynaptic['VA12'] = [0,0]
#         postsynaptic['VA2'] = [0,0]
#         postsynaptic['VA3'] = [0,0]
#         postsynaptic['VA4'] = [0,0]
#         postsynaptic['VA5'] = [0,0]
#         postsynaptic['VA6'] = [0,0]
#         postsynaptic['VA7'] = [0,0]
#         postsynaptic['VA8'] = [0,0]
#         postsynaptic['VA9'] = [0,0]
#         postsynaptic['VB1'] = [0,0]
#         postsynaptic['VB10'] = [0,0]
#         postsynaptic['VB11'] = [0,0]
#         postsynaptic['VB2'] = [0,0]
#         postsynaptic['VB3'] = [0,0]
#         postsynaptic['VB4'] = [0,0]
#         postsynaptic['VB5'] = [0,0]
#         postsynaptic['VB6'] = [0,0]
#         postsynaptic['VB7'] = [0,0]
#         postsynaptic['VB8'] = [0,0]
#         postsynaptic['VB9'] = [0,0]
#         postsynaptic['VC1'] = [0,0]
#         postsynaptic['VC2'] = [0,0]
#         postsynaptic['VC3'] = [0,0]
#         postsynaptic['VC4'] = [0,0]
#         postsynaptic['VC5'] = [0,0]
#         postsynaptic['VC6'] = [0,0]
#         postsynaptic['VD1'] = [0,0]
#         postsynaptic['VD10'] = [0,0]
#         postsynaptic['VD11'] = [0,0]
#         postsynaptic['VD12'] = [0,0]
#         postsynaptic['VD13'] = [0,0]
#         postsynaptic['VD2'] = [0,0]
#         postsynaptic['VD3'] = [0,0]
#         postsynaptic['VD4'] = [0,0]
#         postsynaptic['VD5'] = [0,0]
#         postsynaptic['VD6'] = [0,0]
#         postsynaptic['VD7'] = [0,0]
#         postsynaptic['VD8'] = [0,0]
#         postsynaptic['VD9'] = [0,0]

#global postsynapticNext = copy.deepcopy(postsynaptic)

def motorcontrol():
        global accumright
        global accumleft

        # accumulate left and right muscles and the accumulated values are
        # used to move the left and right motors of the robot
        for pscheck in postsynaptic:
                if pscheck in musDleft or pscheck in musVleft:
                   accumleft += postsynaptic[pscheck][thisState]
                   postsynaptic[pscheck][thisState] = 0                 #Both states have to be set to 0 once the muscle is fired, or
                   #postsynaptic[pscheck][nextState] = 0                 # it will keep returning beyond the threshold within one iteration.
                elif pscheck in musDright or pscheck in musVright:
                   accumright += postsynaptic[pscheck][thisState]
                   postsynaptic[pscheck][thisState] = 0
                   #postsynaptic[pscheck][nextState] = 0
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
        # Each time a set of neurons is stimulated, this method will execute
        # The weighted values are accumulated in the PostSynaptic array
        # Once the accumulation is read, we see what neurons are greater
        # than the threshold and fire the neuron or muscle that has exceeded
        # the threshold
        global thisState
        global nextState
        for ps in postsynaptic:
                if ps[:3] not in muscles and abs(postsynaptic[ps][thisState]) > threshold:
                        fireNeuron(ps)
                        postsynaptic[ps] = [0,0]
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

##CAH EDITS
            worm1 = "/home/pi/GoPiGo/worm1.wav"
            devnull = open("/dev/null","w")
            subprocess.call(["aplay",  worm1],stderr=devnull)

## Original code
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
                    print (thisState)
## CAH EDITS
                    food1 = "/home/pi/GoPiGo/food1.wav"
                    devnull = open("/dev/null","w")
                    subprocess.call(["aplay",  food1],stderr=devnull)
## Original code
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
    for pscheck in postsynaptic:
        print (pscheck,' ',postsynaptic[pscheck][0],' ',postsynaptic[pscheck][1])
