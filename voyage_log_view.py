import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class VoyageLogView:
    def __init__(self, parent, shared_memory):
        self.frame = ttk.Frame(parent)
        self.shared_memory = shared_memory
        self.applications = []  # List to store job applications
        self.status_options = ["Applied", "Under Review", "Interview Scheduled", "Offer Received"]

        self.create_widgets()

    def create_widgets(self):
        # Job Applications List
        self.tree = ttk.Treeview(self.frame, columns=('Company', 'Position', 'Date Applied', 'Status'), show='headings')
        self.tree.heading('Company', text='Company')
        self.tree.heading('Position', text='Position')
        self.tree.heading('Date Applied', text='Date Applied')
        self.tree.heading('Status', text='Status')
        self.tree.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=4, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Buttons
        add_button = ttk.Button(self.frame, text='Add Application', command=self.add_application)
        add_button.grid(row=1, column=0, padx=5, pady=5)

        update_button = ttk.Button(self.frame, text='Update Status', command=self.update_status)
        update_button.grid(row=1, column=1, padx=5, pady=5)

        delete_button = ttk.Button(self.frame, text='Delete Application', command=self.delete_application)
        delete_button.grid(row=1, column=2, padx=5, pady=5)

        view_button = ttk.Button(self.frame, text='View Details', command=self.view_details)
        view_button.grid(row=1, column=3, padx=5, pady=5)

        # Configure grid weights
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

    def add_application(self):
        company = simpledialog.askstring("Input", "Enter company name:")
        if company:
            position = simpledialog.askstring("Input", "Enter position:")
            if position:
                date = simpledialog.askstring("Input", "Enter date applied (YYYY-MM-DD):")
                if date:
                    status = self.get_status()
                    if status:
                        job_id = f"{company}_{position}_{date}"  # Create a unique job ID
                        job_description = simpledialog.askstring("Input", "Enter job description:")
                        if job_description:
                            self.shared_memory.add_job_description(job_id, job_description)
                            self.tree.insert('', tk.END, values=(company, position, date, status))
                            self.applications.append({
                                'job_id': job_id,
                                'company': company,
                                'position': position,
                                'date': date,
                                'status': status
                            })
                            self.shared_memory.log_action(f"Added application for {position} at {company}")

    def update_status(self):
        selected_item = self.tree.selection()
        if selected_item:
            new_status = self.get_status()
            if new_status:
                self.tree.item(selected_item, values=(self.tree.item(selected_item)['values'][0],
                                                      self.tree.item(selected_item)['values'][1],
                                                      self.tree.item(selected_item)['values'][2],
                                                      new_status))
                # Update the status in the applications list
                index = self.tree.index(selected_item)
                self.applications[index]['status'] = new_status
                self.shared_memory.log_action(f"Updated status for {self.applications[index]['position']} at {self.applications[index]['company']} to {new_status}")

    def delete_application(self):
        selected_item = self.tree.selection()
        if selected_item:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this application?"):
                index = self.tree.index(selected_item)
                deleted_app = self.applications.pop(index)
                self.tree.delete(selected_item)
                self.shared_memory.log_action(f"Deleted application for {deleted_app['position']} at {deleted_app['company']}")

    def view_details(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            app = self.applications[index]
            job_description = self.shared_memory.get_job_description(app['job_id'])
            details = f"Company: {app['company']}\n"
            details += f"Position: {app['position']}\n"
            details += f"Date Applied: {app['date']}\n"
            details += f"Status: {app['status']}\n"
            details += f"Job Description: {job_description}"
            messagebox.showinfo("Application Details", details)

    def get_status(self):
        status_window = tk.Toplevel(self.frame)
        status_window.title("Select Status")
        status_var = tk.StringVar(status_window)
        status_var.set(self.status_options[0])  # Set default value

        for status in self.status_options:
            rb = ttk.Radiobutton(status_window, text=status, variable=status_var, value=status)
            rb.pack(anchor=tk.W, padx=5, pady=5)

        def on_ok():
            status_window.destroy()

        ok_button = ttk.Button(status_window, text="OK", command=on_ok)
        ok_button.pack(pady=10)

        status_window.wait_window()  # Wait for the window to be closed
        return status_var.get()
