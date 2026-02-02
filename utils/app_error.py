from pydantic import BaseModel

class AppError(BaseModel):
    error_code: str
    user_message: str
    timestamp: str

class AppErrorWrapper(Exception):
    def __init__(self, error_code, user_message):
        self.error_code = error_code
        self.user_message = user_message
        # FIX: Call parent constructor so str(e) works
        super().__init__(user_message)
    
    def __str__(self):
        return self.user_message
