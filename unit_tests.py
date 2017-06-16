import unittest
import csv
import codecs

from import_data import Import_CSV
from remote_data import Remote_Database
from export_data import Export_CSV

class TestCSVTools(unittest.TestCase):

    def test_import_csv(self):
        expected_result = [{'first_name': 'Lex',
                            'account_id': '12345', 
                            'created_on': '1/12/11',
                            'account_name': 'lexcorp'},
                           {'first_name': 'Victor',
                            'account_id': '8172',
                            'created_on': '11/19/14', 
                            'account_name': 'latveriaembassy'},
                           {'first_name': 'Max',
                            'account_id': '1924',
                            'created_on': '2/29/12', 
                            'account_name': 'brotherhood'}]
        input_csv = Import_CSV('sample.csv')
        input_csv.import_account_csv()
        self.assertEqual(input_csv.csv_data,expected_result)
    
    def test_remote_database(self):
        imported_data = [{'first_name': 'Lex',
                          'account_id': '12345',
                          'created_on': '1/12/11',
                          'account_name': 'lexcorp'},
                         {'first_name': 'Victor',
                          'account_id': '8172',
                          'created_on': '11/19/14',
                          'account_name': 'latveriaembassy'},
                         {'first_name': 'Max',
                          'account_id': '1924',
                          'created_on': '2/29/12',
                          'account_name': 'brotherhood'}]

        expected_result = [{'status': 'good',
                            'first_name': 'Lex',
                            'account_id': '12345',
                            'status_set_on': '2011-01-12',
                            'created_on': '1/12/11',
                            'account_name': 'lexcorp'},
                           {'status': 'closed',
                            'first_name': 'Victor',
                            'account_id': '8172',
                            'status_set_on': '2015-09-01',
                            'created_on': '11/19/14',
                            'account_name': 'latveriaembassy'},
                           {'status': 'fraud',
                            'first_name': 'Max',
                            'account_id': '1924',
                            'status_set_on': '2012-03-01',
                            'created_on': '2/29/12',
                            'account_name': 'brotherhood'}]
        remote_host = Remote_Database('http://interview.wpengine.io')
        updated_list = remote_host.update_information(imported_data)
        self.assertEqual(updated_list, expected_result)
    
    def test_depythonic_keys(self):
        pythonic_dict = {'status': 'good',
                         'first_name': 'Lex',
                         'account_id': '12345',
                         'status_set_on': '2011-01-12',
                         'created_on': '1/12/11',
                         'account_name': 'lexcorp'}

        expected_keys = {'Status': 'good',
                         'First Name': 'Lex',
                         'Account ID': '12345',
                         'Status Set On': '2011-01-12',
                         'Created On': '1/12/11',
                         'Account Name': 'lexcorp'}

        output_csv = Export_CSV('')
        export_format = output_csv.depythonic_keys(pythonic_dict)
        self.assertDictEqual(export_format,expected_keys)

    def delete_extra_data():
        extra_key_dict = {'Status': 'good',
                         'First Name': 'Lex',
                         'Account ID': '12345',
                         'Status Set On': '2011-01-12',
                         'Created On': '1/12/11',
                         'Account Name': 'lexcorp'}
        valid_keys_dict = {'Status': 'good',
                          'First Name': 'Lex',
                          'Account ID': '12345',
                          'Status Set On': '2011-01-12',
                          'Created On': '1/12/11'}
        valid_keys = ['Account ID','First Name','Created On','Status',
                       'Status Set On']

        output_csv = Export_CSV('')
        response = output.delete_extra_data(extra_key_dict, valid_keys)
        self.assertDictEqual(response, valid_keys_dict)

    def test_export_csv(self):
        export_list = [{'Status': 'good',
                        'First Name': 'Lex',
                        'Account ID': '12345',
                        'Status Set On': '2011-01-12',
                        'Created On': '1/12/11'},
                       {'Status': 'closed',
                        'First Name': 'Victor',
                        'Account ID': '8172',
                        'Status Set On': '2015-09-01',
                        'Created On': '11/19/14'},
                       {'Status': 'fraud',
                        'First Name': 'Max',
                        'Account ID': '1924',
                        'Status Set On': '2012-03-01',
                        'Created On': '2/29/12'}]
        output_csv = Export_CSV('test_export.csv')
        output_csv.export_from_list(export_list)
        with codecs.open('test_export.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=',')
            count = 0
            for line in reader:
                self.assertDictEqual(line, export_list[count])
                count += 1
        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCSVTools)
    unittest.TextTestRunner(verbosity=2).run(suite)
