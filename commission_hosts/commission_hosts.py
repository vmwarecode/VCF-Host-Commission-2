#Commission hosts
import requests
import json
import sys
import time
import os
sys.path.append(os.path.abspath(__file__ + '/../../'))
from Utils.utils import Utils
import pprint


class ComissionHosts:
    def __init__(self):
        print('Commission Hosts')
        self.utils = Utils(sys.argv)
        self.hostname = sys.argv[1]

    def commission_hosts(self):
        data = self.utils.read_input(os.path.abspath(__file__ +'/../')+'/commission_hosts_spec.json')
        validations_url =  'https://'+self.hostname+'/v1/hosts/validations/commissions'
        response =self.utils.post_request(data,validations_url)
        request_id = response['id']
        
        print ('Validating the input....')
        url = 'https://' + self.hostname+'/v1/hosts/validations/'+request_id
        result = self.utils.poll_on_id(url,False)
        if(result != 'SUCCEEDED'):
            print ('Validation Failed.')
            exit(1)
        
        comission_url = 'https://'+self.hostname+'/v1/hosts'
        response = self.utils.post_request(data,comission_url)
        print ('Commissioning hosts...')
        pprint.pprint(response)
        task_id = response['id']
        task_url = 'https://'+self.hostname+'/v1/tasks/'+task_id
        print ("Host Commission task completed with status:  " + self.utils.poll_on_id(task_url,True) )

if __name__== "__main__":
    ComissionHosts().commission_hosts()

