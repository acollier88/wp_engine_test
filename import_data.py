import csv
import os
import codecs
import json
import sys

class Import_CSV(object):

    def __init__(self, input_file, data_directory=None):
        if data_directory:
            self.data_directory = data_directory
        else:
            self.data_directory = os.path.realpath(os.path.dirname(__file__))
        self.input_file = input_file
        self.csv_data = []
        
    def verify_data(self, row, count, verbose, strict):
        skip = False
        account_id = row['account_id']
        account_name = row['account_name']
        first_name = row['first_name']
        created_on = row['created_on']
        if account_id == '':
            skip = True
            if strict >= 2:
                sys.exit('Error: Account ID is empty! Skipping Line {0}'\
                         ' exiting program'.format(count))
            if verbose:
                print('Error: Account ID is empty! Skipping Line {0}'\
                      .format(count))
            return skip
        elif verbose:
            print('Importing Account ID {1} [Line {0}]'\
                  .format(count, account_id))
        
        if account_name == '':
            if strict in [1,2]:
                skip = True
                if verbose:
                    print('Error: Account ID {1}: Account Name is empty'\
                          '! Skipping Line {0}'.format(count, account_id))                
                return skip
            elif strict == 3:
                sys.exit('Error: Account ID {1}: Account Name is '\
                         'empty [Line {0}] exiting program'\
                         .format(count, account_id))
            if verbose:
                print('Warning: Account ID {1}: Account Name is empty'\
                      '! [Line {0}]'.format(count, account_id))
                
        if first_name == '':
            if strict in [1,2]:
                skip = True
                if verbose:
                    print('Error: Account ID {1}: First Name is empty'\
                          '! Skipping Line {0}'.format(count, account_id))                 
                return skip
            elif strict == 3:
                sys.exit('Error: Account ID {1}: First Name is '\
                         'empty [Line {0}] exiting program'\
                         .format(count, account_id))
            if verbose:
                print('Warning: Account ID {1}: First Name is empty!'\
                      ' [Line {0}]'.format(count, account_id))
                
        if created_on == '':
            if strict in [1,2]:
                skip = True
                if verbose:
                    print('Error: Account ID {1}: Created On is empty'\
                          '! Skipping Line {0}'.format(count, account_id))                
                return skip
            elif strict == 3:
                sys.exit('Error: Account ID {1}: Created On is '\
                         'empty [Line {0}] exiting program'\
                         .format(count, account_id))
            if verbose:            
                print('Warning: Account ID {1}: Created On is empty!'\
                      '[Line {0}]'.format(count, account_id))
        return skip

    def import_account_csv(self, verbose=False, strict=3):
        #Strict 0 = Skip Missing Account ID Rows [Default]
        #Strict 1 = Strict 0 + Skip any rows with missing data
        #Strict 2 = Strict 1 + End Import on Missing Account ID
        #Strict 3 = End Import on any missing information
        
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
                skip = self.verify_data(line_dict, count, verbose, strict)
                if not skip:
                    self.csv_data.append(line_dict)
