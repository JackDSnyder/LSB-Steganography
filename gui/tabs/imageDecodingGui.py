import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import customtkinter as ctk
from utils.imageEncodingDecoding import decodeImage

def createImageDecodingTab(notebook):
    ImageDecodingTab = ttk.Frame(notebook)
    notebook.add(ImageDecodingTab, text="Decode Images")