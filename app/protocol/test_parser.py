import unittest
from app.protocol.parser import Array, BulkString, ParsingError

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

class TestEncodeArray(unittest.TestCase):
    def test_encode_empty_array(self):
        empty_data = []
        empty_encoded_data = Array.encode(empty_data)
        self.assertEqual(empty_encoded_data, "*0\r\n")

    def test_encode_array_with_strings(self):
        data = ["Hello", "World"]
        encoded_data = Array.encode(data)
        self.assertEqual(encoded_data, "*2\r\n$5\r\nHello\r\n$5\r\nWorld\r\n")

    @unittest.skip("not supported yet")
    def test_encode_array_with_integers(self):
        # not supported yet
        data = [1, 2, 3]
        encoded_data = Array.encode(data)
        self.assertEqual(encoded_data, "*3\r\n$1\r\n1\r\n$1\r\n2\r\n$1\r\n3\r\n")


class TestDecodeArray(unittest.TestCase):
    def test_decode_empty_array(self):
        encoded_data = "*0\r\n"
        decoded_data = Array.decode(encoded_data)
        self.assertEqual(decoded_data, [])

    def test_decode_array_with_strings(self):
        encoded_data = "*2\r\n$5\r\nHello\r\n$5\r\nWorld\r\n"
        decoded_data = Array.decode(encoded_data)
        self.assertEqual(decoded_data, ["Hello", "World"])

    def test_decode_array_with_integers(self):
        encoded_data = "*3\r\n$1\r\n1\r\n$1\r\n2\r\n$1\r\n3\r\n"
        decoded_data = Array.decode(encoded_data)
        self.assertEqual(decoded_data, ['1', '2', '3'])


