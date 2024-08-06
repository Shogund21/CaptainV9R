import tkinter as tk
from tkinter import ttk, scrolledtext


class CareerPortfolioView:
    def __init__(self, parent, shared_memory):
        self.frame = ttk.Frame(parent)
        self.shared_memory = shared_memory

        self.create_widgets()

    def create_widgets(self):
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=60, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Message entry
        self.chat_entry = tk.Entry(self.frame, width=50)
        self.chat_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Send button
        send_button = tk.Button(self.frame, text="Send", command=self.send_chat_message)
        send_button.grid(row=1, column=1, padx=10, pady=5)

        # Configure grid weights
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

    def send_chat_message(self):
        user_input = self.chat_entry.get()
        if user_input:
            self.display_chat_message(f"You: {user_input}")

            # Here you would typically call your AI to process the input
            # For now, we'll just echo the message
            ai_response = f"AI: I received your message: {user_input}"
            self.display_chat_message(ai_response)

            self.chat_entry.delete(0, tk.END)

    def display_chat_message(self, message):
        self.chat_display.insert(tk.END, message + "\n\n")
        self.chat_display.see(tk.END)