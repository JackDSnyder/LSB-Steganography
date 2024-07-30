import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import customtkinter as ctk
from utils.imageEncodingDecoding import encodeImage

def createImageEncodingTab(notebook):
    ImageEncodingTab = ttk.Frame(notebook)
    notebook.add(ImageEncodingTab, text="Encode Images")