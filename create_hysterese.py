# -*- coding: utf-8 -*-
"""
create_hysterese.py -   Creates hysteresis loop and csv-file out of OOMMF
                        data tables.
Created on Sun May 23 16:02:03 2021
@author: Niklas Pantschitz - 2022
niklas.pantschitz@gmx.de
reliable on: pandas, matplotlib, tkinter
last update: 08.02.2022

This program asks the user to select various OOMMF odt data tables
First it changes the format to csv and creates a pandas DataFrame. Based on
this a hysteresis loop is created using matplotlib.
There also is the chance to save the dataframe to a csv file making it
possible to access it via Excel.
"""


import pandas as pd
import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog as fd

pd.options.mode.chained_assignment = None


LST_PATHS = []
# The program is realiable on the following columns:
COLUMNS = [
    "Iteration",
    "Field Updates",
    "Sim Time",
    "Time Step",
    "Step Size",
    "Bx",
    "By",
    "Bz",
    "B",
    "|m x h|",
    "Mx/Ms",
    "My/Ms",
    "Mz/Ms",
    "Total Energy",
    "Exchange Energy",
    "Anisotropy Energy",
    "Demag Energy",
    "Zeeman Energy",
    "Max Angle",
]


# =============================================================================
# Functions
# =============================================================================


def read_odt(path: str):
    """Read in .odt-files as a txt-file

    Loops through every line of the .odt-file adding each line
    to a list. Deleting unnecessary rows. Then creates a dataframe
    out of the list of lists.

    Args:
        path [str]: path of the file

    Returns:
        df_data [pd.DataFrame]: According dataframe
    """
    # read odt file
    f = open(path, "r")
    data = []
    for line in f:
        data.append(line)
    f.close()
    # modify data
    del data[0:5]
    del data[-1]

    # create pd DataFrame
    tmp = 0
    for ele in data:
        # split each list of row-data by spaces into a list of lists
        data[tmp] = data[tmp].split()
        tmp += 1
    df_data = pd.DataFrame(data=data, columns=COLUMNS)

    return df_data


def modify_data(df: pd.DataFrame):
    """Changes needed columns to float64 datatype

    Args:
        df [pd.DataFrame]: Dataframe which should be modified

    Returns:
        data [pd.DataFrame]: Modified dataframe
    """
    data = df.iloc[:, 10:12]
    data["Mx/Ms"] = data["Mx/Ms"].astype("float64")
    data["My/Ms"] = data["My/Ms"].astype("float64")
    return data


def get_angle(title: str):
    """Gets angle of the simulation data for further adjustments.

    Name of the file must have a specific format: "..._angle_Grad.odt" or
    "..._angle_deg.odt".
    The angle must be surrounded by underscores. No further underscores
    must be in the name of the file.

    Args:
        title (str): Name of the file

    Returns:
        angle (int): Angle of the files simulation
    """
    tmp = title.split("_")
    if tmp[-1] == "Grad.odt" or tmp[-1] == "deg.odt":
        angle = int(tmp[-2])
    else:
        angle = 0

    return angle


def get_data(df: pd.DataFrame, angle: int):
    """Creates a dataframe with all the needed data to create a png.

    Extracts needed columns from the main dataframe. Changes format and
    values to create the according hysteresis loop.

    Args:
        df (pd.DataFrame): DataFrame which should be processed.
        angle (int): Angle of the simulation.

    Returns:
        h_frame (pd.DataFrame): DataFrame containing all the needed data.
    """
    h_columns = ["Bx", "By", "B", "M_longitudinal", "M_transversal"]
    h_data = modify_data(df)
    h_frame = pd.DataFrame(columns=h_columns)

    df.Bx = df.Bx.astype(float)
    df.By = df.By.astype(float)

    h_frame.Bx = df.Bx
    h_frame.By = df.By

    h_frame["M_longitudinal"] = -h_data["Mx/Ms"] * math.cos(
        math.radians(angle)
    ) - h_data["My/Ms"] * math.sin(math.radians(angle))
    h_frame["M_transversal"] = -h_data["Mx/Ms"] * math.sin(
        math.radians(angle)
    ) + h_data["My/Ms"] * math.cos(math.radians(angle))
    return h_frame


def get_paths():
    """Reads in file paths unsing tkinters fd.askopenfilenames() function and
    saves them in a global list
    """
    status.config(background="red", text="Loading Data")
    global LST_PATHS
    LST_PATHS = fd.askopenfilenames()
    status.config(background="green", text="Ready")
    return


def create_png():
    """Creates a png file of the Hysteresis-loop

    Plots the data provided by get_data() using matplotlib.
    Two lines are being plotted, longitudinal and transversal.
    """
    status.config(background="red", text="Creating pngs")
    save_path = fd.askdirectory(initialdir="/", title="Select Folder")

    for ele in LST_PATHS:
        # get file name from path
        name = ele.split("/")[-1]

        df = read_odt(ele)

        angle = get_angle(ele)
        print("Angle: ", angle)

        h_frame = get_data(df, angle)

        # angle x-axis adaption
        if angle != 0 and angle != 180:
            h_frame.Bx = h_frame.Bx / (-math.cos(math.radians(angle)))

        # if Bx 1st == 0 --> By
        if int(h_frame.Bx[0]) == 0:
            h_frame.Bx = h_frame.By

        series_long = h_frame["M_longitudinal"]
        series_trans = h_frame["M_transversal"]

        # create matplotlib plot
        plt.figure()
        plt.plot(h_frame.Bx, series_long, label="M_long", color="red")
        plt.plot(h_frame.Bx, series_trans, label="M_trans", color="blue")
        plt.legend()
        plt.title(name)
        plt.xlabel("H / mT")
        plt.ylabel("M / Msat")
        plt.axhline(0, lw=0.4, color="black")
        plt.axvline(0, lw=0.4, color="black")
        plt.savefig(save_path + "/" + name + ".png", dpi=300)
        plt.close()
    status.config(background="green", text="Ready")
    return


def create_csv():
    """Asks the user to select a folder to save the csv-files to and
    saves the data accordingly using the input name.
    """
    status.config(background="red", text="Creating CSVs")
    # ask for folder
    save_path = fd.askdirectory(initialdir="/", title="Select Folder")

    # handle each file
    for ele in LST_PATHS:
        # get name from path
        name = ele.split("/")[-1]

        df = read_odt(ele)

        # save as csv
        df.to_csv(save_path + "/" + name + ".csv", index=False)
        status.config(background="green", text="Ready")
    return


# =============================================================================
# Tkinter setup
# =============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hysteresis-Loop")
    root.geometry("250x240")

    # Set up Buttons
    bttn_load = tk.Button(
        root, text="Load", command=get_paths, width=15, font=("bold 10")
    )
    bttn_png = tk.Button(
        root, text="To png", command=create_png, width=15, font=("bold 10")
    )
    bttn_csv = tk.Button(
        root, text="To csv", command=create_csv, width=15, font=("bold 10")
    )
    bttn_exit = tk.Button(
        root, text="Exit", command=root.destroy, width=28, font=("bold 10")
    )

    title = tk.Label(root, text="Creating a png/csv file of odt by OOMMF")
    options = tk.Label(root, text="Options:", font="bold 10 underline")
    global status
    status = tk.Label(root, text="Ready", background="green")

    # Set up Labels
    label_status = tk.Label(root, text="Status: ")
    label_load = tk.Label(root, text="Load odt files:")
    label_png = tk.Label(root, text="Create png files:")
    label_csv = tk.Label(root, text="Create csv files:")

    # Place everything into GUI
    bttn_load.grid(row=2, column=1, pady=5)
    bttn_png.grid(row=3, column=1, pady=5)
    bttn_csv.grid(row=4, column=1, pady=5)
    bttn_exit.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    label_load.grid(row=2, column=0)
    label_png.grid(row=3, column=0)
    label_csv.grid(row=4, column=0)
    title.grid(row=0, column=0, columnspan=2, pady=7)
    options.grid(row=1, column=0)
    status.grid(row=5, column=1, pady=5)
    label_status.grid(row=5, column=0)

    root.mainloop()
