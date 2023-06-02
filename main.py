# import cmd
from fileinput import close
import pandas as pd
import barcode as bc #Barcode Generator
from barcode.writer import ImageWriter #Uses Pillow to write png
from os import chdir #Change Dir
from tkinter import HORIZONTAL, simpledialog,filedialog # File and Folder Prompts to Set working directory
import PySimpleGUI as sg #Python Simple GUI

# Set Barcode Class 'Code128'
barcode128 = bc.get_barcode_class('code128')

# Define Functions ---->
# TODO:
# Update Target Folder/File Strings in GUI on return

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
    df['Serial'] = DataFrame['Serial Number']
    df.to_csv("IMPORT ME.csv", index=False)
    with open('BarcodesRAW.txt', 'w') as f:
        for i in barcodes:
            f.write(str(i) + "\n")
    close()


def GenerateBarcodes(DataFrame):
    barcodes = DataFrame['Barcode']
    Serial = DataFrame['Serial Number']
    for index, i in enumerate(barcodes):
        barcode128(str(i),ImageWriter()).save(f"{FileName}_{index + 1}",options=options)

#<------

# Barcode Writer Options
options = {
    'module_width' : 0.5, # Float, default 0.2
    'module_height' : 30.0, # Float default 15.0
    'font_size' : 10,
    # 'font_path': '/Fonts/Ubuntu-Regular.ttf',
    'quiet_zone' : 2, # Left and right padding default 15.0
    'dpi' : 600, # Image DPI default 300 ImageWriter() only
    }

sg.theme('Reds')

# Simple GUI Layout using nested Lists
layout = [
    [sg.Text('Generator')],
    [sg.Text('Output Name'),sg.InputText(key='-INPUT-')],
    [sg.Push(),sg.Button('Select Folder',key='-FOLDERBTN-'),sg.Button('Select File',key='-FILEBTN-'),sg.Button('Generate',key='-STARTBTN-'),sg.Push()],
    [sg.Text('Target Folder: --',key="FOLDERSTRING")],
    [sg.Text('Target File: -- ',key="FILESTRING")]
]

# Spawn Window and apply GUI Layout and skin
varwindow = sg.Window('TestGUI', layout)
while True:
    event, values = varwindow.read()
    if event == sg.WIN_CLOSED:
        break

    if event == '-FILEBTN-':
        TargetFile = GetFile()
        varwindow['FILESTRING'].Update(f'Target File: {TargetFile}')

    if event == '-FOLDERBTN-':
        TargetFolder = GetFolder()
        varwindow['FOLDERSTRING'].Update(f'Target Folder: {TargetFolder}')

    if event == '-STARTBTN-':
        if  values['-INPUT-'] == "":
            sg.popup('Please Enter a File Name')
            continue
        vari = 0
        FileName = values['-INPUT-']
        # TO DO: 
        # Implament Threading
        # Implament Progress bar
        chdir(TargetFolder)
        varDataFrame = GetCSV(TargetFile,TargetFolder)
        GenerateDocs(varDataFrame)
        GenerateBarcodes(varDataFrame)
        sg.popup(f'Finished \n Output Location: {TargetFolder}')