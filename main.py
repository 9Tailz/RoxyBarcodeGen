# import cmd
from fileinput import close
import pandas as pd
import barcode as bc #Barcode Generator
from barcode.writer import ImageWriter
from os import chdir #Change Dir
from tkinter import HORIZONTAL, simpledialog,filedialog
import PySimpleGUI as sg
import os

barcode128 = bc.get_barcode_class('code128')

def GetFolder():
    FolderName = filedialog.askdirectory()
    return FolderName

def GetFile():
    FileName = filedialog.askopenfile()
    return FileName

def GetCSV(TargetFile,TargetFolder):
    df = pd.read_csv(TargetFile,header=1,usecols=['Serial Number','Barcode'])
    return df

def GenerateDocs(DataFrame):
    df = pd.DataFrame()
    barcodes = DataFrame['Barcode']
    Serial = DataFrame['Serial Number']
    df['Barcode'] = barcodes
    df.reset_index()
    df["@image"] = df.apply(lambda row: f"{TargetFolder}\{FileName}_{row.name + 1}.png", axis=1)
    df.to_csv("IMPORT ME.csv", index=False)
    with open('BarcodesRAW.txt', 'w') as f:
        for i in barcodes:
            f.write(str(i) + "\n")
    close()
    

def GenBarcodesNew(DataFrame):
    barcodes = DataFrame['Barcode']
    Serial = DataFrame['Serial Number']
    for index, i in enumerate(barcodes):
        barcode128(str(i),ImageWriter()).save(f"{FileName}_{index + 1}",options=options)



options = {
    'module_width' : 0.5,
    'module_height' : 30.0,
    'font_size' : 10,
    # 'font_path': '/Fonts/Ubuntu-Regular.ttf',
    'quiet_zone' : 2,
    'dpi' : 600,
    }

sg.theme('Reds')

layout = [
    [sg.Text('Generator')],
    [sg.Text('Output Name'),sg.InputText(key='-INPUT-')],
    [sg.Push(),sg.Button('Select Folder',key='-FOLDERBTN-'),sg.Button('Select File',key='-FILEBTN-'),sg.Button('Generate',key='-STARTBTN-'),sg.Push()]
]
varwindow = sg.Window('TestGUI', layout)
while True:
    event, values = varwindow.read()
    if event == sg.WIN_CLOSED:
        break

    if event == '-FILEBTN-':
       TargetFile = GetFile()

    if event == '-FOLDERBTN-':
       TargetFolder = GetFolder()

    if event == '-STARTBTN-':
        if  values['-INPUT-'] == "":
            sg.popup('Please Enter a File Name')
            continue
        vari = 0
        FileName = values['-INPUT-']
        chdir(TargetFolder)
        varDataFrame = GetCSV(TargetFile,TargetFolder)
        GenerateDocs(varDataFrame)
        GenBarcodesNew(varDataFrame)
        sg.popup('Finished')