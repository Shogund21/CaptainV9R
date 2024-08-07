import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


class ResumeWindow:
    def __init__(self, parent, shared_memory):
        self.window = tk.Toplevel(parent)
        self.window.title("Resume Editor")
        self.window.geometry("800x600")
        self.shared_memory = shared_memory

        self.llm = ChatOpenAI(temperature=0.7)
        self.resume_analysis_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["resume", "job_description"],
                template="""
                Analyze the following resume in the context of the given job description. 
                Provide feedback on the resume's strengths and areas for improvement, 
                specifically tailored to the job requirements:

                Resume:
                {resume}

                Job Description:
                {job_description}

                Please provide your analysis and suggestions for improvement:
                """
            )
        )

        self.create_widgets()

    def create_widgets(self):
        # Resume text area
        self.resume_text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=70, height=20)
        self.resume_text.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        if self.shared_memory.resume_content:
            self.resume_text.insert(tk.END, self.shared_memory.resume_content)

        # Buttons
        save_button = ttk.Button(self.window, text="Save Resume", command=self.save_resume)
        save_button.grid(row=1, column=0, padx=5, pady=5)

        analyze_button = ttk.Button(self.window, text="Analyze Resume", command=self.analyze_resume)
        analyze_button.grid(row=1, column=1, padx=5, pady=5)

        tailor_button = ttk.Button(self.window, text="Tailor Resume", command=self.tailor_resume)
        tailor_button.grid(row=1, column=2, padx=5, pady=5)

        close_button = ttk.Button(self.window, text="Close", command=self.window.destroy)
        close_button.grid(row=1, column=3, padx=5, pady=5)

        # Configure grid weights
        self.window.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.window.grid_rowconfigure(0, weight=1)

    def save_resume(self):
        content = self.resume_text.get("1.0", tk.END).strip()
        self.shared_memory.update_resume(content)
        messagebox.showinfo("Success", "Resume saved successfully!")

    def analyze_resume(self):
        content = self.resume_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Please enter a resume before analyzing.")
            return

        job_id = self.select_job_id()
        if not job_id:
            return

        job_description = self.shared_memory.get_job_description(job_id)
        if not job_description:
            messagebox.showwarning("Warning", "No job description found for the selected job.")
            return

        try:
            analysis = self.resume_analysis_chain.run(resume=content, job_description=job_description)
            self.show_analysis(analysis)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during analysis: {str(e)}")

    def tailor_resume(self):
        content = self.resume_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Please enter a resume before tailoring.")
            return

        job_id = self.select_job_id()
        if not job_id:
            return

        job_description = self.shared_memory.get_job_description(job_id)
        if not job_description:
            messagebox.showwarning("Warning", "No job description found for the selected job.")
            return

        try:
            tailoring_prompt = PromptTemplate(
                input_variables=["resume", "job_description"],
                template="""
                Tailor the following resume for the given job description. 
                Highlight relevant skills and experiences, and adjust the content to better match the job requirements. 
                Maintain the original structure and keep important information:

                Resume:
                {resume}

                Job Description:
                {job_description}

                Tailored Resume:
                """
            )
            tailoring_chain = LLMChain(llm=self.llm, prompt=tailoring_prompt)
            tailored_resume = tailoring_chain.run(resume=content, job_description=job_description)

            self.show_tailored_resume(tailored_resume)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while tailoring the resume: {str(e)}")

    def show_tailored_resume(self, tailored_resume):
        tailored_window = tk.Toplevel(self.window)
        tailored_window.title("Tailored Resume")
        tailored_window.geometry("600x400")

        tailored_text = scrolledtext.ScrolledText(tailored_window, wrap=tk.WORD, width=70, height=20)
        tailored_text.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        tailored_text.insert(tk.END, tailored_resume)

        close_button = ttk.Button(tailored_window, text="Close", command=tailored_window.destroy)
        close_button.pack(pady=10)

    def show_analysis(self, analysis):
        analysis_window = tk.Toplevel(self.window)
        analysis_window.title("Resume Analysis")
        analysis_window.geometry("500x400")

        analysis_text = scrolledtext.ScrolledText(analysis_window, wrap=tk.WORD, width=60, height=20)
        analysis_text.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        analysis_text.insert(tk.END, analysis)
        analysis_text.config(state=tk.DISABLED)

        close_button = ttk.Button(analysis_window, text="Close", command=analysis_window.destroy)
        close_button.pack(pady=10)

    def select_job_id(self):
        job_ids = list(self.shared_memory.job_descriptions.keys())
        if not job_ids:
            messagebox.showwarning("Warning", "No job descriptions available. Please add job applications first.")
            return None

        job_id_window = tk.Toplevel(self.window)
        job_id_window.title("Select Job")
        job_id_window.geometry("300x200")

        job_id_var = tk.StringVar(job_id_window)
        job_id_var.set(job_ids[0])  # Set default value

        job_id_menu = ttk.Combobox(job_id_window, textvariable=job_id_var, values=job_ids)
        job_id_menu.pack(pady=20)

        def on_select():
            job_id_window.destroy()

        select_button = ttk.Button(job_id_window, text="Select", command=on_select)
        select_button.pack(pady=10)

        job_id_window.wait_window()  # Wait for the window to be closed
        return job_id_var.get()
