import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import customtkinter as ctk
from utils.textEncodingDecoding import encodeText

def createTextEncodingTab(notebook):
    textEncodingTab = ttk.Frame(notebook)
    notebook.add(textEncodingTab, text="Encode Text")