from django.test import SimpleTestCase
from unittest.mock import patch

from ftm import analyze as an

class AnalyzeTests(SimpleTestCase):
    @patch('socket.gethostbyname', return_value='127.0.0.1')
    def test_findservidor_returns_dict(self, mock_gethostbyname):
        result = an.findservidor('example.com', {})
        self.assertIsInstance(result, dict)
        self.assertIn('www', result)

    @patch('ftm.analyze.pythonwhois.get_whois', return_value={'raw': ['data']})
    def test_d_whois_basic(self, mock_whois):
        self.assertEqual(an.d_whois('example.com'), 'data')

