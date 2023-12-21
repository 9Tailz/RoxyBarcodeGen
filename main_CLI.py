## Import Libarys

from fileinput import close
import pandas as pd
from barcode import Code128 #Barcode Generator
from barcode.writer import ImageWriter #Uses Pillow to write png
# from os import chdir #Change Dir
import os
import sys

## Def Fuctions

def main():
    TargetFile = os.path.join(os.getcwd(),sys.argv[1])
    TargetFolder = os.path.join(os.getcwd(),sys.argv[2])
    FileName = str(sys.argv[3])
    try:
        os.mkdir(TargetFolder)
    except FileExistsError:
        pass
    os.chdir(TargetFolder)
    print("Loading CSV....")
    varDataFrame  = GetCSV(TargetFile)
    print("Done\n Generating Docs...")
    GenerateDocs(varDataFrame, TargetFolder, FileName)
    print("Done\n Generating Barcodes...")
    GenerateBarcodes(varDataFrame, FileName, options)
    print("Done\n Please check everything is correct")

def GetCSV(TargetFile):
    df = pd.read_csv(TargetFile,header=1,usecols=['Serial Number','Barcode'])
    return df

def GenerateDocs(DataFrame, TargetFolder, FileName):
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


def GenerateBarcodes(DataFrame, FileName, options):
    barcodes = DataFrame['Barcode']
    Serial = DataFrame['Serial Number']
    for index, i in enumerate(barcodes):
        Code128(str(i),ImageWriter()).save(f"{FileName}_{index + 1}",options=options)

## Barcode Writer Options
options = {
    'module_width' : 0.5, # Float, default 0.2
    'module_height' : 30.0, # Float default 15.0
    'font_size' : 10,
    # 'font_path': '/Fonts/Ubuntu-Regular.ttf',
    'quiet_zone' : 2, # Left and right padding default 15.0
    'dpi' : 600, # Image DPI default 300 ImageWriter() only
    }

if __name__ == "__main__":
    main()
