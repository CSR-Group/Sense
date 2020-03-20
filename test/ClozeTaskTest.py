import unittest
from context import csense


class TestDataSet(unittest.TestCase):
    
    def test_list_int(self):
        """
        Test the format of the dataset
        """
        stories = csense.benchmark.ClozeTask.getDataSet()
        assert(len(stories) == 1571)

if __name__ == '__main__':
    unittest.main()