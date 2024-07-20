CRLF = "\r\n"

class ParsingError(Exception):
    pass

class BulkString:
    @classmethod
    def encode(cls, data):
        return f"${len(data)}\r\n{data}\r\n"
    
    @classmethod
    def decode(self, data):
        length, data = self._parse(data)
        return data
        

    @classmethod
    def _parse(self, data):
        if not data.startswith("$"):
            raise ParsingError("No $ at the beginning")
        
        if data == "$-1\r\n":
            return 0, None
        
        parts = data.split(CRLF)
        if len(parts) != 3:
            raise ParsingError("Invalid number of \\r\\n symbols")

        length, data, _ = parts

        try:
            length = int(length)
        except ValueError:
            raise ParsingError("Invalid length format")

        if len(data) != int(length):
            raise ParsingError("Length does not match data length")
        
        return length, data
        


