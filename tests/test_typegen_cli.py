import unittest
import subprocess

class TypegenUnitTest(unittest.TestCase):
    
    def setUp(self):
        self.tests = {
            'fish': ['poetry', 'run', 'typegen', '-f', 'tests/fish_obj', '-v', 'fish', '-t', 'FishType']
        }   
        
    def test_typegen_cli(self):
        result = subprocess.run(self.tests['fish'])
        self.assertEqual(result.returncode, 0) 
        return result.returncode
    
    

