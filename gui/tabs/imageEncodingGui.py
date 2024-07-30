import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import customtkinter as ctk
from utils.imageEncodingDecoding import encodeImage

def createImageEncodingTab(tabview):
    imageEncodingTab = ctk.CTkFrame(master=tabview.tab("Encode Image"))
    imageEncodingTab.pack()