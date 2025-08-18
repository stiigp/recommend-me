import bcrypt

class Hasher:
    def __init__(self, input):
        self.input = input
    
    def encrypt(self) -> str:
        bytes = self.input.encode('utf-8')
        salt = bcrypt.gensalt()

        res = bcrypt.hashpw(bytes, salt)

        return res.decode('utf-8')