import unittest
from app.parser import BulkString, ParsingError

class TestEncodeBulkString(unittest.TestCase):
    def test_encode_string(self):
        data = "Hello, World!"
        encoded_data = BulkString.encode(data)
        self.assertEqual(encoded_data, "$13\r\nHello, World!\r\n")

    def test_encode_empty_string(self):
        empty_data = ""
        empty_encoded_data = BulkString.encode(empty_data)
        self.assertEqual(empty_encoded_data, "$0\r\n\r\n")

    def test_encode_null(self):
        null_data = None
        null_encoded_data = BulkString.encode(null_data)
        self.assertEqual(null_encoded_data, "$-1\r\n")

class TestDecodeBulkString(unittest.TestCase):
    def test_decode_string(self):
        encoded_data = "$13\r\nHello, World!\r\n"
        decoded_data = BulkString.decode(encoded_data)
        self.assertEqual(decoded_data, "Hello, World!")

    def test_decode_empty_string(self):
        empty_encoded_data = "$0\r\n\r\n"
        empty_decoded_data = BulkString.decode(empty_encoded_data)
        self.assertEqual(empty_decoded_data, "")

    def test_decode_null(self):
        null_encoded_data = "$-1\r\n"
        null_decoded_data = BulkString.decode(null_encoded_data)
        self.assertIsNone(null_decoded_data)

    def test_invalid_format_missing_CRLF(self):
        # Missing CRLF at the end
        invalid_data = "$5\r\nHello"  
        with self.assertRaises(ParsingError):
            BulkString._parse(invalid_data)
        
    def test_invalid_format_missing_dollar(self):
        # Missing $ at the beginning
        invalid_data = "5\r\nHello\r\n"
        with self.assertRaises(ParsingError):
            BulkString._parse(invalid_data)
    
    def test_invalid_format_invalid_length(self):
        # Invalid length format
        invalid_data = "$a\r\nHello\r\n"
        with self.assertRaises(ParsingError):
            BulkString._parse(invalid_data)

if __name__ == "__main__":
    unittest.main()