import csv
import os
import codecs
import json
import requests

class Remote_Database(object):

    def __init__(self, base_url):
        self.base_url = base_url
        self.get_account_url = self.base_url + '/v1/accounts/{account_id}'

    def update_information(self, existing_data, verbose=False):
        updated_data = []
        if verbose: 
            print ''
            print 'Updating'
        for user in existing_data:
            account_url = str(self.get_account_url).replace('{account_id}',
                                                            user['account_id'])
            timeout = False
            try:
                r = requests.get(account_url, timeout=10)
                response = r.json()
            except requests.exceptions.Timeout:
                timeout = True
                if verbose:
                    print 'Timeout occurred connecting to {0}'.format(account_url)
                response = {'detail': 'Not found.'}
            except:
                timeout = True
                if verbose:
                    print 'Unexpected error occurred parsing {0}'.format(account_url)
                response = {'detail': 'Not found.'}
        
            if response.get('detail') == 'Not found.':
                if verbose and not timeout:
                    print 'Account {0} has no details on the server'.format(user['account_id'])
                user.update({'status':'','status_set_on':''})
                updated_data.append(user)
            else:
                updates = {
                    'status' : str(response.get('status','')),
                    'status_set_on' : str(response.get('created_on',''))
                } #Forcing Non-Unicode Values for Consistency
                if verbose:
                    print 'Updates for Account {0}: {1}'.format(user['account_id'], updates)
                user.update(updates)
                updated_data.append(user)
        return updated_data
