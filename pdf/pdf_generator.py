from fpdf import FPDF
from reportlab.lib.pagesizes import A4
import textwrap

import tkinter as tk
from tkinter import font as TkFont 

import math

import configparser

class PdfGenerator():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("settings/config.ini")

        settings = self.config["PDF Generator Settings"]

        self.pdf_name = settings.get('pdf_name')
        
        self.width, self.height = A4
        self.fontsize_pt = settings.getint('font_size')
        
        tk.Frame().destroy()
        font = TkFont.Font(family="Arial", size=self.fontsize_pt)
        char_length = font.measure("a")
        dpi = settings.getint('dpi')
        self.char_length_pt = char_length * 72 / dpi

        self.width_chars = math.ceil(self.width / self.char_length_pt)
        margin_bottom_pt = 10

        self.pdf = FPDF(orientation='P', unit="pt", format=A4)
        self.pdf.set_auto_page_break(auto=True, margin=margin_bottom_pt)
        self.pdf.add_page()
        self.pdf.set_font(family="Arial", size=self.fontsize_pt)

        self.txt_file_name = settings.get('txt_name')
        self.txt_file = open(self.txt_file_name, "w")

    def add_text(self, text: str):
        self.txt_file.write(text)

    def save_pdf(self):
        self.txt_file.close()
        with open(self.txt_file_name, "r") as file:
            for line in file:
                wrapped_lines = textwrap.wrap(line, width=self.width_chars)

                if len(wrapped_lines) == 0:
                    self.pdf.ln()

                for wrap in wrapped_lines:
                    self.pdf.cell(w=0, h=self.fontsize_pt, txt=wrap, ln=1)
        
        self.pdf.output(self.pdf_name)