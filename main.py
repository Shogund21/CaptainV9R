import tkinter as tk
from tkinter import ttk
from career_portfolio_view import CareerPortfolioView
from voyage_log_view import VoyageLogView
from captain_quarters_view import CaptainQuartersView
from resume_window import ResumeWindow
from shared_memory import SharedMemory
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CAPTAIN - Career Advancement Platform AI Navigator")
        self.root.geometry("800x600")
        self.shared_memory = SharedMemory()

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

        self.add_captain_ai_to_tabs()

    def add_captain_ai_to_tabs(self):
        for tab in [self.career_portfolio, self.voyage_log, self.captain_quarters]:
            captain_frame = ttk.Frame(tab.frame)
            captain_frame.grid(row=100, column=0, columnspan=4, sticky='ew')

            self.captain_input = tk.Entry(captain_frame)
            self.captain_input.grid(row=0, column=0, sticky='ew')

            send_button = ttk.Button(captain_frame, text="Ask Captain", command=lambda t=tab: self.ask_captain(t))
            send_button.grid(row=0, column=1)

            captain_frame.grid_columnconfigure(0, weight=1)

    def ask_captain(self, tab):
        user_input = self.captain_input.get()
        if user_input:
            response = self.get_ai_response(user_input)
            tab.display_message(f"You: {user_input}")
            tab.display_message(f"Captain: {response}")
            self.captain_input.delete(0, tk.END)

    def get_ai_response(self, user_input):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Captain AI, a helpful career advisor."},
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    def show_resume_editor(self):
        ResumeWindow(self.root, self.shared_memory)

    def run(self):
        self.root.mainloop()

def main():
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()