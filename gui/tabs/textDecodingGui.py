import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import customtkinter as ctk
from utils.textEncodingDecoding import decodeText

def createTextDecodingTab(notebook):
    textDecodingTab = ttk.Frame(notebook)
    notebook.add(textDecodingTab, text="Decode Text")