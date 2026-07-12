from collections import defaultdict


class ConversationMemory:
    def __init__(self):
        self.store = defaultdict(list)

    def get_history(self, session_id: str) -> str:
        history = self.store[session_id]

        if not history:
            return "No previous conversation."

        formatted = []

        for message in history:
            formatted.append(
                f"{message['role'].capitalize()}: {message['content']}"
            )

        return "\n".join(formatted)

    def add_message(self, session_id: str, role: str, content: str):
        self.store[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def clear(self, session_id: str):
        self.store[session_id] = []


memory = ConversationMemory()