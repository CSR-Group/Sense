import unittest
import context
from csense.benchmark import cloze_task


class TestDataSet(unittest.TestCase):
    
    def test_list_int(self):
        """
        Test the format of the dataset
        """
        stories = cloze_task.getDataSet()
        assert(len(stories) == 1571)

if __name__ == '__main__':
    unittest.main()