from typing import Literal

class Message:
    def __init__(self, role: Literal["user", "assistant", "system"], content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content
        }

