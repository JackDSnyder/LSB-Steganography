import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import customtkinter as ctk
from utils.imageEncodingDecoding import decodeImage

def createImageDecodingTab(tabview):
    imageDecodingTab = ctk.CTkFrame(master=tabview.tab("Encode Image"))
    imageDecodingTab.pack()
