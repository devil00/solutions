import unittest
import csv
import random
from conference import Conference

class TestConference(unittest.TestCase):
    def setUp(self):
        self.file1 = "test_file.csv"

        self.file2 = "./test_data/test2.csv"
        self.file3 = "./test_data/test3.csv"

        self._create_csv_file(self.file2)
        self._create_csv_file(self.file3)

    def _create_csv_file(self, file_path):
        with open(file_path, "wb") as file0:
            csvwriter = csv.writer(file0, quotechar='|',
                                   quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(['name', 'duration', 'cost'])
            for i in xrange(1, 30):
                csvwriter.writerow(["p{}".format(i), random.randrange(1, 8),
                              random.randrange(1, 200)])

    def _get_input_data(self, file_path):
        presenters = []
        with open(file_path, "r") as c_file:
            csvfile = csv.DictReader(c_file)
            for pinfo in csvfile:
                presenters.append(pinfo)
        return presenters
        
    def test1_arrange_conference(self):
        conf = Conference(3, 8, self.file1)
        (conf_presenters, calculated_cost) = conf.arrange_conf()
        input_data = self._get_input_data(self.file1)
        for conf_presenter in conf_presenters:
            actual_cost = sum([int(d['cost']) for d in input_data
                               if d['name'] in conf_presenter])
            self.assertEqual(actual_cost, calculated_cost)

    def test2_arrange_conference(self):
        conf = Conference(3, 8, self.file2)
        (conf_presenters, calculated_cost) = conf.arrange_conf()
        input_data = self._get_input_data(self.file2)
        for conf_presenter in conf_presenters:
            actual_cost = sum([int(d['cost']) for d in input_data
                               if d['name'] in conf_presenter])
            self.assertEqual(actual_cost, calculated_cost)

    def test3_arrange_conference(self):
        conf = Conference(3, 8, self.file3)
        (conf_presenters, calculated_cost) = conf.arrange_conf()
        input_data = self._get_input_data(self.file3)
        for conf_presenter in conf_presenters:
            actual_cost = sum([int(d['cost']) for d in input_data
                               if d['name'] in conf_presenter])
            self.assertEqual(actual_cost, calculated_cost)


    def tearDown(self):
        pass
        """
        import os
        os.remove(self.file2)
        os.remove(self.file3)
        """

if __name__ == "__main__" :
    unittest.main()

