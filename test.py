import pandas as pd
import barcode as bc #Barcode Generator
from barcode.writer import SVGWriter,ImageWriter
from io import BytesIO
import os
from tkinter import filedialog



df = pd.read_csv("2023.csv", header=1,usecols=['Serial Number','Barcode'])
bytesobject = BytesIO()
barcode128 = bc.get_barcode_class('code128')

folder = filedialog.askdirectory()
path = os.get_exec_path(folder)
print(df.head())

options = {
    'module_width' : 0.8,
    'module_height' : 30.0,
    'font_size' : 10,
    # 'font_path': '/Fonts/Ubuntu-Regular.ttf',
    'quiet_zone' : 2,
    'dpi' : 600,
    }

barcoderow = df['Barcode']
serialrow = df['Serial Number']

for x, y in zip(barcoderow,serialrow):
    barcode128(str(x),writer=ImageWriter()).save("file",options=options)
    