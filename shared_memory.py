from langchain.memory import ConversationBufferMemory

class SharedMemory:
    def __init__(self):
        self.resume_content = ""
        self.job_descriptions = {}  # Dictionary to store multiple job descriptions
        self.conversation_memory = ConversationBufferMemory()

    def update_resume(self, content):
        self.resume_content = content
        self.log_action("Resume updated")

    def add_job_description(self, job_id, content):
        self.job_descriptions[job_id] = content
        self.log_action(f"Job description added for job ID: {job_id}")

    def get_job_description(self, job_id):
        return self.job_descriptions.get(job_id, "")

    def log_action(self, action):
        self.conversation_memory.save_context(
            {"human_input": action},
            {"ai_output": "Acknowledged"}
        )

    def get_memory(self):
        return {
            "resume": self.resume_content,
            "job_descriptions": self.job_descriptions,
            "conversation": self.conversation_memory.load_memory_variables({})
        }


    def add_to_conversation(self, human_input, ai_output):
        """Add a conversation exchange to the memory."""
        self.conversation_memory.save_context(
            {"human_input": human_input},
            {"ai_output": ai_output}
        )

    def get_conversation_history(self):
        """Get the conversation history."""
        return self.conversation_memory.load_memory_variables({})

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_memory.clear()

    def get_resume(self):
        """Get the current resume content."""
        return self.resume_content
