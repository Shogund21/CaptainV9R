import tkinter as tk
from tkinter import ttk, scrolledtext
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

class CaptainQuartersView:
    def __init__(self, parent, shared_memory):
        self.frame = ttk.Frame(parent)
        self.shared_memory = shared_memory
        self.create_widgets()

    def create_widgets(self):
        # Advice display area
        self.advice_display = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=60, height=20)
        self.advice_display.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure grid weights
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

    def display_message(self, message):
        self.advice_display.insert(tk.END, message + "\n\n")
        self.advice_display.see(tk.END)

    def create_widgets(self):
        self.advice_display = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=60, height=20)
        self.advice_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.question_entry = tk.Entry(self.frame, width=50)
        self.question_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ask_button = ttk.Button(self.frame, text="Ask for Advice", command=self.ask_for_advice)
        ask_button.grid(row=1, column=1, padx=10, pady=5)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

    def ask_for_advice(self):
        question = self.question_entry.get()
        if question:
            self.display_message(f"You: {question}")
            response = self.get_ai_response(question)
            self.display_message(f"Captain AI: {response}")
            self.question_entry.delete(0, tk.END)

    def get_ai_response(self, question):
        try:
            context = f"Resume: {self.shared_memory.resume_content}\n"
            context += f"Job Descriptions: {self.shared_memory.get_all_job_descriptions()}\n"
            context += f"Question: {question}"

            # Get response from AI
            response = self.conversation.predict(input=context)
            return response
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"