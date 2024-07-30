import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import customtkinter as ctk
from utils.textEncodingDecoding import encodeText

def createTextEncodingTab(tabview):
    textEncodingTab = ctk.CTkFrame(master=tabview.tab("Encode Text"))
    textEncodingTab.pack()

    l1 = ctk.CTkLabel(master=textEncodingTab, text="Hello")
    l1.pack()