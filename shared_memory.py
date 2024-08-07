from langchain.memory import ConversationBufferMemory

class SharedMemory:
    def __init__(self):
        self.resume_content = ""
        self.job_descriptions = {}  # Dictionary to store multiple job descriptions
        self.conversation_memory = ConversationBufferMemory()

    def update_resume(self, content):
        self.resume_content = content

    def add_job_description(self, job_id, content):
        self.job_descriptions[job_id] = content

    def get_job_description(self, job_id):
        return self.job_descriptions.get(job_id, "")

    def get_all_job_descriptions(self):
        return self.job_descriptions

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
        self.conversation_memory.save_context(
            {"human_input": human_input},
            {"ai_output": ai_output}
        )

    def get_conversation_history(self):
        return self.conversation_memory.load_memory_variables({})

    def clear_conversation_history(self):
        self.conversation_memory.clear()

    def get_resume(self):
        return self.resume_content