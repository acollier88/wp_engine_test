import csv
import os
import codecs
import json
import requests

class Export_CSV(object):

    def __init__(self, output_file, data_directory=None):
        if data_directory:
            self.data_directory = data_directory
        else:
            self.data_directory = os.path.realpath(os.path.dirname(__file__))
        self.output_file = output_file
        self.csv_data = []

    def depythonic_keys(self, pythonic_dict):
        return {k.replace('_',' ').title().replace('Id','ID'):v \
                for k,v in pythonic_dict.iteritems()}
    def delete_extra_data(self, existing_dict, valid_keys):
        return {k:v for k,v in existing_dict.iteritems() if k in valid_keys}
    def export_from_list(self, export_data, verbose=False):
        field_names = ['Account ID','First Name','Created On','Status',
                       'Status Set On']
        if verbose:
            print ''
            print 'Exporting to {0}'.format(self.output_file)
        with open(self.output_file,'wb') as fout:
            writer = csv.DictWriter(fout, delimiter=',', fieldnames=field_names)
            writer.writeheader()
            for row in export_data:
                data = self.depythonic_keys(row)
                data = self.delete_extra_data(data, field_names)
                if verbose:
                    print 'Writing {0} to csv'.format(data)
                writer.writerow(data)
