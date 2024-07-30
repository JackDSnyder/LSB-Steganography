import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import customtkinter as ctk
from utils.textEncodingDecoding import decodeText

def createTextDecodingTab(tabview):
    textDecodingTab = ctk.CTkFrame(master=tabview.tab("Decode Text"))
    textDecodingTab.pack()