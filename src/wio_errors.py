"""
Posible wio E5 errors
"""

class Wioe5InvalidParameterError(Exception):
    def __init__(self,message = 'parameter is invalid' ) -> None:
        self.message =  message
        super().__init__(self.message)

class Wioe5CommandUnkownError(Exception):
    def __init__(self,message = 'Command unkown' ) -> None:
        self.message =  message
        super().__init__(self.message)

class Wioe5WrongFormatError(Exception):
    def __init__(self,message = 'Command is in wrong format' ) -> None:
        self.message =  message
        super().__init__(self.message)

class Wioe5CommandUnavailableError(Exception):
    def __init__(self,message = 'Command is unavailable in current mode (check with \"AT+MODE")' ) -> None:
        self.message =  message
        super().__init__(self.message)

class Wioe5ExcessParametersError(Exception):
    def __init__(self,message = 'Too Many parameters. LoraWAN modem support max 15 parameters' ) -> None:
        self.message =  message
        super().__init__(self.message)

class Wioe5LenghtError(Exception):
    def __init__(self,message = 'Length command is too long (exceed 528 bytes)' ) -> None:
        self.message =  message
        super().__init__(self.message)

class Wioe5TimeoutError(Exception):
    def __init__(self,message = 'Receive end symbol timeout, command must end with \\n' ) -> None:
        self.message =  message
        super().__init__(self.message)

class Wioe5InvalidCharError(Exception):
    def __init__(self,message = 'Invalid Character received' ) -> None:
        self.message =  message
        super().__init__(self.message)

class Wioe5Error(Exception):
    def __init__(self,message = 'Either -21, -22 or -23' ) -> None:
        self.message =  message
        super().__init__(self.message)

def wioError(answer : bytes):
    index = answer.find(b'ERROR')
    if index == -1:
        return

    code = answer[index+6:answer.find(b')')]

    if code == b'-1':
        raise Wioe5InvalidParameterError
    elif code == b'-10':
        raise Wioe5CommandUnkownError
    elif code == b'-11':
        raise Wioe5WrongFormatError
    elif code == b'-12':
        raise Wioe5CommandUnavailableError
    elif code == b'-20':
        raise Wioe5ExcessParametersError
    elif code == b'-21':
        raise Wioe5LenghtError
    elif code == b'-22':
        raise Wioe5TimeoutError
    elif code == b'-23':
        raise Wioe5InvalidCharError
    elif code == b'-24':
        raise Wioe5Error