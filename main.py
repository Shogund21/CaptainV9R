import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
import os

from shared_memory import SharedMemory
from resume_window import ResumeWindow
from career_portfolio_view import CareerPortfolioView
from voyage_log_view import VoyageLogView
from captain_quarters_view import CaptainQuartersView

load_dotenv()

class MainWindow:
    def __init__(self, shared_memory):
        self.root = tk.Tk()
        self.root.title("CAPTAIN - Career Advancement Platform AI Navigator")
        self.root.geometry("800x600")
        self.shared_memory = shared_memory

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.career_portfolio = CareerPortfolioView(self.notebook, self.shared_memory)
        self.notebook.add(self.career_portfolio.frame, text='Career Portfolio')

        self.voyage_log = VoyageLogView(self.notebook, self.shared_memory)
        self.notebook.add(self.voyage_log.frame, text='Voyage Log')

        self.captain_quarters = CaptainQuartersView(self.notebook, self.shared_memory)
        self.notebook.add(self.captain_quarters.frame, text="Captain's Quarters")

        self.resume_button = tk.Button(self.root, text="Open Resume Editor", command=self.show_resume_editor)
        self.resume_button.pack(pady=10)

    def show_resume_editor(self):
        ResumeWindow(self.root, self.shared_memory)

    def run(self):
        self.root.mainloop()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set in .env file")
        return

    shared_memory = SharedMemory()
    app = MainWindow(shared_memory)
    app.run()

if __name__ == "__main__":
    main()
