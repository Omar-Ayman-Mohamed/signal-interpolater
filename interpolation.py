# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 17:20:17 2022

@author: wario
"""

import pandas as pd
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from tkinter import *
from tkinter import ttk
from scipy import signal
from scipy import interpolate
from sympy import S, symbols, printing
from numpy import transpose
import math
import time as delay
import threading
window = tk.Tk()
window.title('Interpolation & CurveFitting')
window.geometry("1200x675")
window.configure(bg='#00A0A0')
global time
global final_amplitude
global DividedTime
global Dividedamplitude
global InterpolatedTime
global InterpolatedAmplitude
InterpolatedTime=[]
InterpolatedAmplitude=[]
global flag
flag=1
global MapFlag
MapFlag=0
global yinvflag
yinvflag=0
def DividingChunks(Amplitude,Time):
    ChunksNumber= ChuncksSlider.get()
    NewTime =  ChunkArrayFunction(Time, ChunksNumber,OverlapSlider.get())
    NewAmplitude= ChunkArrayFunction(Amplitude, ChunksNumber,OverlapSlider.get())
    return NewAmplitude,NewTime
    
def PolynomialInterpolation(Time,Amplitude,Order,originaltime):
    global InterpolatedTime
    global InterpolatedAmplitude
    pol = np.polyfit(Time,Amplitude,Order)  
    NewTime = np.linspace(min(Time),max(Time))
    NewAmplitude = np.polyval(pol,NewTime)
    ClippedTime=NewTime[0:int((len(NewTime)-1)*(ClipSignal.get()/100))]
    ClippedAmplitude=NewAmplitude[0:int((len(NewTime)-1)*(ClipSignal.get()/100))]
    ExtrapolatedAmplitude=np.polyfit(ClippedTime,ClippedAmplitude,Order)
    ExtrapolatedAmplitude=np.polyval(ExtrapolatedAmplitude,originaltime)
    #ExtrapolatedAmplitude=interpolate.interp1d(ClippedTime, ClippedAmplitude, fill_value='extrapolate')
    SignalAx.plot(originaltime,ExtrapolatedAmplitude,'--')  
    InterpolatedTime=np.concatenate((InterpolatedTime,Time))
    InterpolatedAmplitude=np.concatenate((InterpolatedAmplitude,ExtrapolatedAmplitude))
    
# =============================================================================
#     ClippedAmpFromReal=Amplitude[0:int((len(NewTime)-1)*(ClipSignal.get()/100))]
#     ClippedTimeFromReal=Time[0:int((len(NewTime)-1)*(ClipSignal.get()/100))]
#     polextra = np.polyfit(ClippedTimeFromReal,ClippedAmpFromReal,Order)  
#     NewTimeextra = np.linspace(min(ClippedTimeFromReal),max(ClippedTimeFromReal))
#     NewAmplitudeextra = np.polyval(polextra,NewTimeextra)
#     ExtrapolatedAmplitudeextra=np.polyfit(NewTimeextra,NewAmplitudeextra,Order)
#     ExtrapolatedAmplitudeextra=np.polyval(NewAmplitudeextra,Time)
#     SignalAx.plot(Time,ExtrapolatedAmplitudeextra)  
# =============================================================================


    SignalFigure.canvas.draw_idle()

def openFile():
    global time
    global final_amplitude
    filepath = filedialog.askopenfilename(filetypes= (("csv files",".csv"),("all files",".*")))
    openFile.filepath = filepath
    file = open(filepath,'r')
    loaded_data = pd.read_csv( openFile.filepath)
    time = loaded_data["time_sec"] 
    final_amplitude = loaded_data["amplitude"]
    SignalAx.plot(time,final_amplitude)
    SignalFigure.canvas.draw_idle()    
    file.close()

def ChuncksUI(self):
    global time
    global final_amplitude
    global DividedTime
    global Dividedamplitude
    ChuncksNum=ChuncksSlider.get()
    ChunkIndices = []
    for Index in range(1, ChuncksNum+1):
        ChunkIndex = "Chunk{}".format(Index)
        ChunkIndices.append(ChunkIndex)
    ChunkCB['values'] = ChunkIndices
    
def polyinterpolate():
    global OrderInt
    global order1error
    global order2error
    global order3error
    global InterpolatedTime
    global InterpolatedAmplitude
    global DividedTime 
    global Dividedamplitude
    InterpolatedTime=[]
    InterpolatedAmplitude=[]
    order1error=[]
    order2error=[]
    order3error=[]
    Order=InterpolatingOrderCB1.get()
    if (Order== "1stOrder"):
        OrderInt=1
    elif(Order== "2ndOrder"):
        OrderInt=2
    elif(Order== "3rdOrder"):
        OrderInt=3
    elif(Order== "4thOrder"):
        OrderInt=4
    elif(Order== "5thOrder"):
        OrderInt=5
    elif(Order== "6thOrder"):
        OrderInt=6
    elif(Order== "7thOrder"):
        OrderInt=7
    elif(Order== "8thOrder"):
        OrderInt=8
    elif(Order== "9thOrder"):
        OrderInt=9
    elif(Order== "10thOrder"):
        OrderInt=10        
    SignalAx.clear()
    SignalAx.plot(time,final_amplitude)
    SignalAx.grid()
    ErrorAx.clear()
    DividedTime, Dividedamplitude=DividingChunks(time[0:int((len(time)-1)*(ClipSignal.get()/100))],final_amplitude[0:int((len(time)-1)*(ClipSignal.get()/100))])
    for i in range(0,len(Dividedamplitude)):
        PolynomialInterpolation(DividedTime[i],Dividedamplitude[i],OrderInt,time)
    SignalAx.set_ylim(min(final_amplitude),max(final_amplitude))
    error=calculate_error(time,final_amplitude,InterpolatedTime,InterpolatedAmplitude)
    ErrorAx.clear()
    ErrorAxymin,ErrorAxymax=ErrorAx.get_ylim()
    ErrorAxymid=(ErrorAxymin+ErrorAxymax)/2
    ErrorAxxmin,ErrorAxxmax=ErrorAx.get_xlim()
    ErrorAxxmid=(ErrorAxxmin+ErrorAxxmax)/2
    ErrorAx.text(ErrorAxxmid, ErrorAxymid, str(np.round(error,4))+"%", fontsize=10,fontstyle='oblique',ha='center', va='center')
    ErrorFigure.canvas.draw_idle()
    SignalAx.canvas.draw_idle()

    EquationAx.clear()
    EquationFigure.canvas.draw_idle()

    
def WriteEquation(self):
    EquationAx.clear()
    ChosenChunk=ChunkCB.get()
    ChosenChunk = "".join(i for i in ChosenChunk if i in "012345678910")
    DividedTime, Dividedamplitude=DividingChunks(time,final_amplitude)
    Order=InterpolatingOrderCB1.get()
    if (Order== "1stOrder"):
        OrderInt=1
    elif(Order== "2ndOrder"):
        OrderInt=2
    elif(Order== "3rdOrder"):
        OrderInt=3
    elif(Order== "4thOrder"):
        OrderInt=4
    elif(Order== "5thOrder"):
        OrderInt=5
    elif(Order== "6thOrder"):
        OrderInt=6
    elif(Order== "7thOrder"):
        OrderInt=7
    elif(Order== "8thOrder"):
        OrderInt=8
    elif(Order== "9thOrder"):
        OrderInt=9
    elif(Order== "10thOrder"):
        OrderInt=10     
    for i in range(0,len(Dividedamplitude)):
        if (int(ChosenChunk)==int(i)+1):
            pol = np.polyfit(DividedTime[i],Dividedamplitude[i],OrderInt)
            x = symbols("x")
            poly = sum(S("{:6.2f}".format(v))*x**i for i, v in enumerate(pol[::-1]))
            eq_latex = printing.latex(poly)
            eq_latex="$"+eq_latex+"$"
            EquationAxymin,EquationAxymax=EquationAx.get_ylim()
            EquationAxymid=(EquationAxymin+EquationAxymax)/2
            EquationAxxmin,EquationAxxmax=EquationAx.get_xlim()
            EquationAxxmid=(EquationAxxmin+EquationAxxmax)/2
            EquationAx.text(EquationAxxmid, EquationAxymid, eq_latex, fontsize=8,fontstyle='oblique',ha='center', va='center')
            EquationFigure.canvas.draw_idle()
def DividingChunksforerror(Amplitude,Time,ChuncksNumber):
    NewTime =  np.array_split(Time, ChuncksNumber)
    NewAmplitude= np.array_split(Amplitude, ChuncksNumber)
    return NewAmplitude,NewTime

def ErrorCalculate(original_x,original_y,inter_x,inter_y):
    error_x = []
    error_y = []
    for i in range(0,len(inter_x)):
        XValue=IndexToValue(inter_x,i)    
        OriginalIndex= ValueToIndex(original_x,XValue) 
        global falg
        if falg == True :
            errory = original_y[OriginalIndex] - inter_y[i]
            error_y.append(errory)
        elif falg == False :
            break
    errorsquare=np.square(error_y)
    errorsum=sum(errorsquare)
    msd=errorsum/ len(error_y)
    rmsd=math.sqrt(msd)
    return (rmsd)    
    
def ChunkArrayFunction(array,chunknum,OverlapPercent):
    Chunked2dArray=[]
    if chunknum!=1:
        x=-1000
        chunksize=int(len(array)/chunknum)
        OverlapValue=int( (OverlapPercent/100) * chunksize )
        i=0
        while True:  
            Chunked2dArray.append([])
            for j in range(0,chunksize):
                if i !=0:
                    Chunked2dArray[i].append(array[(i*chunksize-(OverlapValue*i))+j])
                    x= array[(i*chunksize-(OverlapValue*i))+j]
                else:
                    Chunked2dArray[i].append(array[i*chunksize+j])
            if i!=0:
                index=np.where(array == x)
                if (len(array)-index[0][0]+OverlapValue<=chunksize):
                    break
            i+=1
        return(Chunked2dArray)
    else: 
        Chunked2dArray.append(array)
        return(Chunked2dArray)

def ChunkSignal(Time,Amplitude,chunknum,OverlapPercent):
    ChunkedTime2D =  ChunkArrayFunction(Time,chunknum,OverlapPercent)
    ChunkedAmplitude2D= ChunkArrayFunction(Amplitude, chunknum,OverlapPercent)
    return ChunkedTime2D, ChunkedAmplitude2D

def PolynomialInterpolationForMap(ChunkedTime2D, ChunkedAmplitude2D,InterpolationOrder):#returns 1d array containing the concatenation of all chunks
    InterpolatedTimeforError=[]
    InterpolatedAmplitudeforError=[]
    for chunkcounter in range(0,len(ChunkedTime2D)):
        BestFitForChunk = np.polyfit( ChunkedTime2D[chunkcounter], ChunkedAmplitude2D[chunkcounter], InterpolationOrder )  
        NewTimeforerror = np.linspace( min(ChunkedTime2D[chunkcounter]), max(ChunkedTime2D[chunkcounter]) )
        NewAmplitudeforerror = np.polyval(BestFitForChunk, ChunkedTime2D[chunkcounter])
        InterpolatedTimeforError=np.concatenate((InterpolatedTimeforError,ChunkedTime2D[chunkcounter]))
        InterpolatedAmplitudeforError=np.concatenate((InterpolatedAmplitudeforError,NewAmplitudeforerror))
    return InterpolatedTimeforError,InterpolatedAmplitudeforError

def ErrorMapCalculateSingleCase(OriginalTime1D,OriginalAmplitude1D,ChunksNumber,OverlapPercent,InterpolationOrder):
    ChunkedTime2D, ChunkedAmplitude2D=ChunkSignal(OriginalTime1D,OriginalAmplitude1D,ChunksNumber,OverlapPercent)
    InterpolatedTime1D,InterpolatedAmplitude1D=PolynomialInterpolationForMap(ChunkedTime2D, ChunkedAmplitude2D,InterpolationOrder)
    ErrorPercent=ErrorCalculate(OriginalTime1D,OriginalAmplitude1D,InterpolatedTime1D,InterpolatedAmplitude1D)  
    return ErrorPercent

def ErrorMapRowColumn(OriginalTime1D,OriginalAmplitude1D,MapXAxis,MapYAxis):
    global MapFlag
    global ConstantParameterSlider
    ChunksIndex=0
    OverlapIndex=1
    InterpolationOrderIndex=2
    parameters2D=[]
    parameters2D.append(np.arange(1,21,1))
    parameters2D.append(np.arange(0,51,5))
    parameters2D.append(np.arange(1,11,1))  
    XAxIndex= SetAxForMap(MapXAxis)
    YAxIndex= SetAxForMap(MapYAxis) 
    ChunksCounter=np.where(parameters2D[ChunksIndex] == ConstantParameterSlider.get())
    OverlapCounter=np.where(parameters2D[OverlapIndex] == ConstantParameterSlider.get())
    InterpolationCounter=np.where(parameters2D[InterpolationOrderIndex] == ConstantParameterSlider.get())
    ErrorforMap2D=[]
    progressbarstep=(1/len(parameters2D[YAxIndex]))*100
    progressbarvalue=0
    for YAxCounter in range(0,len(parameters2D[YAxIndex])):
        if MapFlag==0:
            break
        ErrorforMap2D.append([])
        for XAxCounter in range(0,len(parameters2D[XAxIndex])):
            ChunksCounter,OverlapCounter,InterpolationCounter=SetChangeable(XAxIndex,XAxCounter,ChunksCounter,OverlapCounter,InterpolationCounter)
            ChunksCounter,OverlapCounter,InterpolationCounter=SetChangeable(YAxIndex,YAxCounter,ChunksCounter,OverlapCounter,InterpolationCounter)
            ErrorSingleCase=ErrorMapCalculateSingleCase(OriginalTime1D,OriginalAmplitude1D,parameters2D[ChunksIndex][ChunksCounter],parameters2D[OverlapIndex][OverlapCounter],parameters2D[InterpolationOrderIndex][InterpolationCounter])
            ErrorforMap2D[YAxCounter].append(ErrorSingleCase)
        progressbarvalue+=progressbarstep
        Progress.set(progressbarvalue)
    return ErrorforMap2D
        
def ShowMap():
    global MapFlag
    global time
    global final_amplitude
    global yinvflag
    if( MapX.get()!=MapY.get() and MapX.get()!="Map X-Axis.." and MapY.get()!="Map Y-Axis.."):
        GenerateMap.pack_forget()
        CancelMap.pack(side=BOTTOM)
        ProgressBar.pack(side=TOP)
        ErrorforMap2D=ErrorMapRowColumn(time,final_amplitude,MapX.get(),MapY.get())
        XIndex=SetAxForMap(MapX.get())
        YIndex=SetAxForMap(MapY.get())
        if (XIndex==0):
            XMAX=20
        elif (XIndex==1):
            XMAX=25
        elif (XIndex==2):
            XMAX=10
        if (YIndex==0):
            YMAX=20
        elif (YIndex==1):
            YMAX=25
        elif (YIndex==2):
            YMAX=10
            
        if MapFlag==1:
            MapAx.clear()
            cMap=MapAx.imshow(ErrorforMap2D[::-1], interpolation='spline16',extent=[0,XMAX,0,YMAX],aspect=0.5*XMAX/YMAX)
            MapFigure.subplots_adjust(right=0.9)
            cbar_ax = MapFigure.add_axes([0.88, 0.15, 0.04, 0.7])
            cbar_ax.clear()
            MapFigure.colorbar(cMap, cax=cbar_ax)
            MapAx.axis('on')
# =============================================================================
#             plt.xticks(fontsize=6)
#             plt.yticks(fontsize=6)
# =============================================================================
            #MapAx.set_ylim(MapAx.get_ylim()[::-1])
            MapAx.set_xlabel(MapX.get(),fontsize=10)
            MapAx.set_ylabel(MapY.get(),fontsize=10)
        MapFigure.canvas.draw_idle()
        ProgressBar.pack_forget()
        CancelMap.pack_forget()
        GenerateMap.pack(side=BOTTOM)
        
def SetChangeable(Index,Counter,ChunksCounter,OverlapCounter,InterpolationCounter):
    if Index==0:
        ChunksCounter=Counter
    elif Index==1:
        OverlapCounter=Counter   
    elif Index==2:
        InterpolationCounter=Counter
    return ChunksCounter,OverlapCounter,InterpolationCounter
        
def SetAxForMap(StringInput):
    if (StringInput== "Number Of Chunks"):
        ParameterIndex=0
    elif (StringInput=="Chunks Overlapping"):  
        ParameterIndex=1
    elif (StringInput== "Interpolation Order"):
        ParameterIndex=2
    return ParameterIndex
    
def PolynomialInterpolationforerror(Timeforerror,Amplitudeforerror,Order,ChosenChunk,loopnumber):
    global InterpolatedTimeforerror
    global InterpolatedAmplitudeforerror
    polforerror = np.polyfit(Timeforerror,Amplitudeforerror,Order)  
    NewTimeforerror = np.linspace(min(Timeforerror),max(Timeforerror))
    NewAmplitudeforerror = np.polyval(polforerror,NewTimeforerror)
    InterpolatedTimeforerror=np.concatenate((InterpolatedTime,NewTimeforerror))
    InterpolatedAmplitudeforerror=np.concatenate((InterpolatedAmplitude,NewAmplitudeforerror))
   
def Range(lst):
    return max(lst) - min(lst)

def GenerateError():
    global MapFlag
    while (True):
        delay.sleep(1)
        if MapFlag==1:
            ShowMap()
            MapFlag=0            
threading.Thread(target=GenerateError).start()           
            
def generateButton():
    global MapFlag 
    MapFlag=1
    threading.Thread(target=GenerateError).join      
    
def cancelButton():
    global MapFlag 
    MapFlag=0
    threading.Thread(target=GenerateError).join
    
def Cancel():
    global flag
    flag=0
    threading.Thread(target=GenerateError).join
    
def IndexToValue(Signal,Index):
    return Signal[Index]

def ValueToIndex(Signal,Value):
    Index=np.searchsorted(Signal, Value)
    return Index

global error_x
global error_y
falg = True

def calculate_error(original_x,original_y,inter_x,inter_y):
    error_x = []
    error_y = []
    for i in range(0,len(inter_x)):
        XValue=IndexToValue(inter_x,i)    
        OriginalIndex= ValueToIndex(original_x,XValue) 
        global falg
        if falg == True :
            errory = original_y[OriginalIndex] - inter_y[i]
            error_y.append(errory)
        elif falg == False :
            break
    errorsquare=np.square(error_y)
    errorsum=sum(errorsquare)
    msd=errorsum/ len(error_y)
    rmsd=math.sqrt(msd)
    nrmsd=rmsd
    return(nrmsd*100)
    
def interpolatingcb(self):
    InterpolatingOrderCB1['values'] = ('1stOrder','2ndOrder','3rdOrder','4thOrder','5thOrder','6thOrder','7thOrder','8thOrder','9thOrder','10thOrder')

def SetConstant(self):
    MapX['values'] = ('Number Of Chunks','Interpolation Order','Chunks Overlapping')
    MapY['values'] = ('Number Of Chunks','Interpolation Order','Chunks Overlapping')
    global ConstantParameterSlider
    ChunksIndex=0
    OverlapIndex=1
    InterpolationOrderIndex=2
    parameters2Dforconstant=[]
    parameters2Dforconstant.append(np.arange(1,21,1))
    parameters2Dforconstant.append(np.arange(0,26,5))
    parameters2Dforconstant.append(np.arange(1,11,1))  
    ConstantParameterSlider = Scale(ConstantParameterFrame,from_=0,to =0,label="Constant Parameter",resolution=0,orient =HORIZONTAL,length=200,bg='#00A0A0',highlightbackground='#00A0A0',highlightcolor='#00A0A0',troughcolor='white',activebackground='#00CCCC')
    ConstantParameterSlider.grid(row=1,column=0)
    if ( MapX.get()!="Map X-Axis.." and MapY.get()!="Map Y-Axis.." and MapY.get()!=MapX.get()):
        xmap=SetAxForMap(MapX.get())
        ymap=SetAxForMap(MapY.get())
        for mapindex in range(0,3):
            if (xmap!=mapindex and ymap!=mapindex):
                Constant=mapindex   
                if Constant==ChunksIndex:
                    Label="NumberOfChunks"
                elif Constant==OverlapIndex:
                    Label="Overlap %"
                elif Constant==InterpolationOrderIndex:
                    Label="InterpolationOrder"
                sliderstep=(parameters2Dforconstant[Constant][1]-parameters2Dforconstant[Constant][0])
                ConstantParameterSlider = Scale(ConstantParameterFrame,from_=min(parameters2Dforconstant[Constant]),to =max(parameters2Dforconstant[Constant]),resolution=sliderstep,orient =HORIZONTAL,length=200,label=Label,font=('Helvetica', 10, 'bold'),bg='#00A0A0',highlightbackground='#00A0A0',highlightcolor='#00A0A0',troughcolor='white',activebackground='#00CCCC')
                ConstantParameterSlider.grid(row=1,column=0)
    
TabStyle = ttk.Style()
TabStyle.configure('My.TButton', foreground = '#00A0A0')
TabStyle.configure('My.TFrame', background = '#00A0A0',foreground = '#00A0A0')
tabControl = ttk.Notebook(window)  
InterpolationTab = ttk.Frame(tabControl,style = 'My.TFrame')
ErrorMapTab = ttk.Frame(tabControl,style = 'My.TFrame')
tabControl.add(InterpolationTab,text=f'{"Interpolation": ^190s}')
tabControl.add(ErrorMapTab, text=f'{"Error Map": ^190s}')
tabControl.pack(expand=True,fill= 'both')
ToolBarFrame= tk.Frame(InterpolationTab,bg='#00A0A0',width=1200, height=50)
ToolBarFrame.pack(side =TOP)
OpenSignal= tk.Button ( ToolBarFrame,height=2, text="Open Signal",activebackground='#00CCCC',bg='#00A0A0' ,relief=GROOVE,font=('Helvetica', 10, 'bold'),command =openFile)
OpenSignal.place(x=25, y=7, width=100, height=35)
ChunkCB=ttk.Combobox(ToolBarFrame,width=15,height=40,font=('Helvetica', 10, 'bold'))
ChunkCB['values'] = ["Choose Chunk.."]
ChunkCB.bind("<<ComboboxSelected>>",WriteEquation)
ChunkCB.current(0)
ChunkCB.place(x=240, y=20, width=135, height=30)
EquationFrame= tk.Frame(InterpolationTab,bg='#00A0A0')
EquationFrame.pack(side =TOP)
EquationLabel=tk.Label(EquationFrame,text = "Equation",bg='#00A0A0',relief=GROOVE,font=('Helvetica', 14, 'bold'))
EquationLabel.grid(row=0,column=0)
EquationFigure=plt.figure(figsize=(5, 1))
EquationFigure.patch.set_facecolor('#00A0A0')
EquationAx=EquationFigure.add_subplot()
EquationAx.get_xaxis().set_visible(False)
EquationAx.get_yaxis().set_visible(False)
EquationCanvas = FigureCanvasTkAgg(EquationFigure,master =EquationFrame) 
EquationCanvas.get_tk_widget().grid(row=0,column=1)
ErrorLabel=tk.Label(EquationFrame,text = "Error",bg='#00A0A0',relief=GROOVE,font=('Helvetica', 14, 'bold'))
ErrorLabel.grid(row=0,column=2)
ErrorFigure=plt.figure(figsize=(3, 1))
ErrorFigure.patch.set_facecolor('#00A0A0')
ErrorAx=ErrorFigure.add_subplot()
ErrorAx.get_xaxis().set_visible(False)
ErrorAx.get_yaxis().set_visible(False)
ErrorCanvas = FigureCanvasTkAgg(ErrorFigure,master =EquationFrame) 
ErrorCanvas.get_tk_widget().grid(row=0,column=3)
SignalFigure=plt.figure(figsize=(1,1),dpi=150)
SignalFigure.patch.set_facecolor('#00A0A0')
SignalAx=SignalFigure.add_subplot(1, 1, 1)
SignalAx.grid()
SignalCanvas = FigureCanvasTkAgg(SignalFigure,master =InterpolationTab) 
SignalCanvas.get_tk_widget().pack(expand=True,fill='both')
SignalFigure.patch.set_facecolor('#00A0A0')
SliderFrame= tk.Frame(InterpolationTab,bg='#00A0A0')
SliderFrame.pack(side =BOTTOM)
CBFrame= tk.Frame(InterpolationTab,bg='#00A0A0')
CBFrame.pack(side =BOTTOM)
ChuncksSlider = Scale(SliderFrame,from_=1,to =20,orient =HORIZONTAL,length=250,label="Number of Chunks",relief=GROOVE,font=('Helvetica', 10, 'bold'),bg='#00A0A0',highlightbackground='#00A0A0',highlightcolor='#00A0A0',troughcolor='white',activebackground='#00CCCC',command=ChuncksUI)
ChuncksSlider.grid(row = 0, column = 0)
ChuncksSlider.set(1)
InterpolatingOrderCB1=ttk.Combobox(CBFrame,width=15,height=60,font=('Helvetica', 12, 'bold'))
InterpolatingOrderCB1.bind("<<ComboboxSelected>>", interpolatingcb)
InterpolatingOrderCB1['values'] = ('Chunk1 Order..','1stOrder','2ndOrder','3rdOrder','4thOrder','5thOrder','6thOrder','7thOrder','8thOrder','9thOrder','10thOrder')
InterpolatingOrderCB1.current(0)
InterpolatingOrderCB1.pack(side=LEFT)
InterpolateButton=tk.Button ( CBFrame,height=1,padx=8,text="Interpolate",activebackground='#00CCCC',bg='#00A0A0' ,relief=GROOVE,font=('Helvetica', 10, 'bold'),command =polyinterpolate)
InterpolateButton.pack(side=RIGHT)
ClipSignalFrame= tk.Frame(InterpolationTab,bg='#00A0A0')
ClipSignalFrame.pack(side =BOTTOM)
ClipSignal = Scale(ClipSignalFrame,from_=10,to =100,orient =HORIZONTAL,length=400,label="Clip Signal %",relief=GROOVE,font=('Helvetica', 10, 'bold'),bg='#00A0A0',highlightbackground='#00A0A0',highlightcolor='#00A0A0',troughcolor='white',activebackground='#00CCCC',resolution=10)
ClipSignal.grid(row = 0, column =1,pady=25)
OverlapSlider = Scale(ClipSignalFrame,from_=0,to =25,orient =HORIZONTAL,length=400,label="Overlap %",relief=GROOVE,font=('Helvetica', 10, 'bold'),bg='#00A0A0',highlightbackground='#00A0A0',highlightcolor='#00A0A0',troughcolor='white',activebackground='#00CCCC',resolution=5)
OverlapSlider.grid(row = 0, column = 0,pady=0) 
MapControlsFrame= tk.Frame(ErrorMapTab,bg='#00A0A0')
MapControlsFrame.pack(side=BOTTOM,pady=10)
GenerateMap= tk.Button ( MapControlsFrame,height=2, text="Generate Error Map",activebackground='#00CCCC',bg='#00A0A0' ,relief=GROOVE,command=generateButton,font=('Helvetica', 14, 'bold'))
GenerateMap.pack(side=BOTTOM)
CancelMap= tk.Button ( MapControlsFrame,height=2 , text="Cancel Error Map",activebackground='#00CCCC',bg='#00A0A0' ,relief=GROOVE,command=cancelButton,font=('Helvetica', 14, 'bold'))
Progress= tk.IntVar()
ProgressBar = ttk.Progressbar(MapControlsFrame, orient=HORIZONTAL, length=180,variable=Progress)
MapAxisFrame= tk.Frame(ErrorMapTab,bg='#00A0A0')
MapAxisFrame.pack(side=TOP)
MapXLabel=tk.Label(MapAxisFrame,text = "X-axis",bg='#00A0A0',relief=GROOVE,font=('Helvetica', 14, 'bold'))
MapXLabel.grid(row=0,column=0,padx=50)
MapYLabel=tk.Label(MapAxisFrame,text = "Y-axis",bg='#00A0A0',relief=GROOVE,font=('Helvetica', 14, 'bold'))
MapYLabel.grid(row=0,column=1,padx=50)

MapX=ttk.Combobox(MapAxisFrame,width=18,height=40,font=('Helvetica', 14, 'bold'))
MapX['values'] = ('Map X-Axis..','Number Of Chunks','Interpolation Order','Chunks Overlapping')
MapX.bind("<<ComboboxSelected>>", SetConstant)
MapX.current(0)
MapX.grid(row=1,column=0,padx=50,pady=25)
MapY=ttk.Combobox(MapAxisFrame,width=18,height=40,font=('Helvetica', 14, 'bold'))
MapY['values'] = ('Map Y-Axis..','Number Of Chunks','Interpolation Order','Chunks Overlapping')
MapY.bind("<<ComboboxSelected>>", SetConstant)
MapY.current(0)
MapY.grid(row=1,column=1,padx=50,pady=25)
ConstantParameterFrame= tk.Frame(ErrorMapTab,bg='#00A0A0')
ConstantParameterFrame.pack(side=TOP)
ConstantParameterSlider = Scale(ConstantParameterFrame,from_=0,to =0,label="Constant Parameter",resolution=0,orient =HORIZONTAL,length=200,bg='#00A0A0',highlightbackground='#00A0A0',highlightcolor='#00A0A0',troughcolor='white',activebackground='#00CCCC')
ConstantParameterSlider.grid(row=1,column=0)
MapFrame= tk.Frame(ErrorMapTab,bg='#00A0A0')
MapFrame.pack(side =TOP)
MapFigure = plt.Figure(figsize=(8,7))
MapAx = MapFigure.add_subplot(111)
MapAx.axis('off')
MapFigure.patch.set_facecolor('#00A0A0')
MapCanvas = FigureCanvasTkAgg(MapFigure,master =ErrorMapTab) 
MapCanvas.get_tk_widget().pack(expand=True,fill='both')
MapFigure.patch.set_facecolor('#00A0A0')
ChunkNum=ChuncksSlider.get()
ChunkArray = []
for x in range(1, ChunkNum+1):
    String = "Chunk{}".format(x)
    ChunkArray.append(String)
window.mainloop()