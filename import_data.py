import csv
import os
import codecs
import json

class Import_CSV(object):

    def __init__(self, input_file, data_directory=None):
        if data_directory:
            self.data_directory = data_directory
        else:
            self.data_directory = os.path.realpath(os.path.dirname(__file__))
        self.input_file = input_file
        self.csv_data = []

    def import_account_csv(self, verbose=False):
        if verbose:
            print ''
            print 'Importing from {0}'.format(self.input_file)
        file_location = os.path.join(self.data_directory, self.input_file)
        with codecs.open(file_location, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=',')
            count = 1
            for line in reader:
                count += 1
                account_id = line.get('Account ID','')
                account_name = line.get('Account Name','')
                first_name = line.get('First Name','')
                created_on = line.get('Created On','')
                line_dict = {
                    'account_id' : account_id,
                    'account_name' : account_name,
                    'first_name' : first_name,
                    'created_on' : created_on   
                }
                if verbose:
                    if account_id == '':
                        print('Error: Account ID is empty! Skipping Line {0}'\
                              .format(count))
                    else:
                        print('Importing Account ID {1} [Line {0}]'\
                              .format(count, account_id))
                    if account_name == '':
                        print('Warning: Account ID {1}: Account Name is empty'\
                              '! [Line {0}]'.format(count, account_id))
                    if first_name == '':
                        print('Warning: Account ID {1}: First Name is empty!'\
                              ' [Line {0}]'.format(count, account_id))
                    if account_name == '':
                        print('Warning: Account ID {1}: Created On is empty!'\
                              '[Line {0}]'.format(count, account_id))
                if account_id != '':
                    self.csv_data.append(line_dict)
