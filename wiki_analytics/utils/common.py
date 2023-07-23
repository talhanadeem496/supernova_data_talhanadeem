from rest_framework.response import Response
from rest_framework import status
import requests
import yaml
import json
import pathlib
from dotenv import dotenv_values
import sys
import traceback
from rest_framework.pagination import PageNumberPagination


def success_response(data={}, message="Success", success=True):
    return Response(
        data={"status": status.HTTP_200_OK, "message": message, "data": data, "success": success},
        content_type='application/json',
        status=status.HTTP_200_OK
    )


def error_response(errors={}, message="Error!", success=False):
    return Response(
        data={"status": status.HTTP_400_BAD_REQUEST, "message": message, "errors": errors, "success": success},
        content_type='application/json',
        status=status.HTTP_400_BAD_REQUEST
    )


def get_error_text():
    # GETTING ERROR
    lines = ''
    ex_type, ex_value, ex_traceback = sys.exc_info()
    if ex_type is None: # ADDING EXCEPTION IN THE CASE OF NO ERROR EXIST
        return 'No Error'
    lines += f'{ex_type.__name__}\n'
    lines += f'{ex_value}\n'

    trace_back = traceback.extract_tb(ex_traceback)

    for trace in trace_back:
        lines += '\n' + '-'*50 + '\n'
        lines += "File : %s\n" % (trace[0])
        lines += "Line : %s\n" % (trace[1])
        lines += "Func.Name : %s\n" % (trace[2])
        lines += "Message : %s\n" % (trace[3])
    return lines


class LoadConfiguration:
    def __init__(self):
        self.env_vars = None
        self.settings = None
        self.configuration = None

    def load_base_path(self):
        return pathlib.Path(__file__).resolve().parent.parent.parent

    def load_env(self):
        return dotenv_values(str(pathlib.Path(self.load_base_path() , '.sviz_env','.env_dev')))

    def load_configuration(self):
        yaml_data = {}
        with open(str(pathlib.Path(self.load_base_path() , 'sviz_configs','configs_dev.yaml')), "r") as stream:
            try:
                yaml_data = yaml.safe_load(stream)
                return yaml_data
            except yaml.YAMLError as exc:
                print(exc)
class CheckRequest:
    def __init__(self, config=None, base_url = None, relative_url = None, 
                 json_string = None, timeout = None, request = None, 
                 content_type = None, method = None, query_params=None,
                 config_query_params_list=None, request_query_params_list = None,
                 page_number = None, page_size = None, token = None):
        self.config = config
        self.base_url = base_url
        self.rel_url = relative_url
        self.json_string = json_string
        self.timeout = timeout
        self.request = request
        self.content_type = content_type
        self.method = method
        self.query_params = query_params
        self.config_query_params_list = config_query_params_list
        self.request_query_params_list = request_query_params_list
        self.page_number = page_number
        self.page_size = page_size
        self.token = token

    def check_get_request(self):
        response = {}
        self.base_url = self.base_url if 'http' in self.base_url else self.config[self.base_url]
        self.rel_url = self.config[self.rel_url]
        self.timeout = self.config[self.timeout]
        self.config_query_params_list = self.config[self.config_query_params_list] if self.config_query_params_list else None
        response = self.check_request()
        return response

    def check_post_request(self):
        response = {}
        self.base_url = self.base_url if 'http' in self.base_url else self.config[self.base_url]
        self.rel_url = self.config[self.rel_url]
        self.timeout = self.config[self.timeout]
        self.config_query_params_list = self.config[self.config_query_params_list] if self.config_query_params_list else None
        response = self.check_request()
        return response

    def get_query_params(self):
        updated_query_params = {}
        # config_query_params_list = self.config['STARTUP_API_QUERY_PARAMETERS']
        # request_query_params_list = list(self.request.query_params.keys())
        if all((self.config_query_params_list, self.request_query_params_list)):
            for qp in self.config_query_params_list:
                if qp in self.request_query_params_list:
                    updated_query_params[qp] = self.query_params[qp]
        return updated_query_params

    def check_request(self):
        response = {}
        try:

            if self.method == 'POST':
                # json_string_temp = {'data': None}
                # json_string_temp['data'] = self.json_string
                # self.json_string = json_string_temp

                headers = {}
                if self.content_type:
                    headers.update({'Content-type':self.content_type})

                if self.page_number:
                    headers.update({'pageNum':self.page_number})

                if self.page_size:
                    headers.update({'pageSize':self.page_size})

                if self.token:
                    headers.update({'token':self.token})

                self.query_params = self.get_query_params()

                # print(self.base_url, self.rel_url, self.json_string, self.timeout, self.request, 
                #     self.content_type, self.method, self.query_params,self.config_query_params_list, self.request_query_params_list)
                response = requests.post(url="".join([self.base_url, self.rel_url]), 
                                        data=json.dumps(self.json_string),
                                        headers=headers,
                                        params = self.query_params,
                                        timeout=tuple((int(self.timeout[0]), int(self.timeout[1]))),
                                        )
                # print(response.json())
                # print("response", response)
                # print("request_method", self.method)
                # print("response_type",type(response))
                # print("response_json_type",type(response.json()))
                return json.dumps(response.json())

            elif self.method == 'GET':
                # print(self.base_url, self.rel_url, self.json_string, self.timeout, self.request, 
                #     self.content_type, self.method, self.query_params,self.config_query_params_list, self.request_query_params_list)
                self.query_params = self.get_query_params()
                response = requests.get(url="".join([self.base_url, self.rel_url]),
                                        params=self.query_params,
                                        headers={'Content-type':self.content_type},
                                        timeout=tuple((int(self.timeout[0]), int(self.timeout[1]))),
                                        )
                # print("response", response)
                # print("request_method", self.method)
                # print("response_type",type(response))
                # print("response_json_type",type(response.json()))
                return json.dumps(response.json())
            else:
            # response.raise_for_status()
                # print("response", response)
                # print("request_method", self.method)
                # print("response_type",type(response))
                # print("response_json_type",type(response.json()))
                return json.dumps(response)
            # Code here will only run if the request is successful
        except requests.exceptions.HTTPError as errh:
            # print(errh)
            response = {}
            response.update(
                {
                    'success': False,
                    'status': 400,
                    'message': str(errh),
                },
            )
            return json.dumps(response)

        except requests.exceptions.ConnectionError as errc:
            # print(errc)
            # # response = errc
            response = {}
            response.update(
                {
                    'success': False,
                    'status': 400,
                    'message': str(errc),
                },
            )
            return json.dumps(response)

        except requests.exceptions.Timeout as errt:
            # print(errt)
            response = {}
            response.update(
                {
                    'success': False,
                    'status': 400,
                    'message': str(errt),
                },
            )
            return json.dumps(response)

        except requests.exceptions.RequestException as err:
            # print(err)
            response = {}
            response.update(
                {
                    'success': False,
                    'status': 400,
                    'message': str(err),
                },
            )
            return json.dumps(response)

class ShowList_StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'per_page'
    max_page_size = 250
    page_query_param = 'page_no'

    # page_query_param = 'page_number'
    def get_from(self):
        return int((self.page.paginator.per_page * self.page.number) - self.page.paginator.per_page + 1)

    def get_to(self):
        return self.get_from() + int(len(self.page.object_list)) - 1

    def get_paginated_response(self, data):
        response = {}
        response["queryset"] = data
        response["pagination"] = {}
        response["pagination"]["page_no"] = self.page.number
        response["pagination"]["count"] = self.page.paginator.count
        response["pagination"]["total_pages"] = self.page.paginator.num_pages
        response["pagination"]["next"] = self.get_next_link()
        response["pagination"]["previous"] = self.get_previous_link()
        response["pagination"]["per_page"] = self.page.paginator.per_page
        response["pagination"]["from"] = self.get_from()
        response["pagination"]["to"] = self.get_to()
        return response


from django.core.mail import EmailMessage
from django.core.mail import send_mail
import string
import threading


def date_handler(date):
    if date == 'N/A':
        date = '1857-05-10'
    else:
        date = datetime.strptime(date, '%m-%d-%Y')
        date = date.strftime('%Y-%m-%d')
    return date

def date_handler_reverse(date):
    if date:
        val = str(date)
        # print(val)
        val = val.split('-')
        # print(val)
        val = "-".join(("-".join((val[1],val[2])), val[0]))
        # print(val)
        return val
    else:
        date = '1857-05-10'

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)
class Util:
    @staticmethod
    def send_email(data):
        
        # send_mail(
        #     subject=data['email_subject'],
        #     message=data['email_body'],
        #     from_email='talha.practice.496@gmail.com',
        #     recipient_list=['talhanadeem496@gmail.com']
        # )
        
        email = EmailMessage(subject=data['email_subject'],
                             body=data['email_body'],
                            #  to=[data['to_email']])
                             to=data['to_email'],
                             )
        email.content_subtype = 'html'
        # EmailThread(email).start()
        email.send(fail_silently=False)
        print('Email sent to:', data['to_email'])
        # print('Here')
        
    @staticmethod
    def password_generator(length):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        number = string.digits
        symbol = string.punctuation
        all = lower + upper + number + symbol
        password = "".join(random.sample(all, length))
        return password

    @staticmethod
    def dictionary_handler(dict_data_employee, validated_data):
        temp_dict = {}
        print('Before---', dict_data_employee)
        for k, v in dict_data_employee.items():
            if v in validated_data.keys() and validated_data[v]['response'] and validated_data[v]['response'] != 'N/A':
                temp_dict[k] = validated_data[v]['response']
        print('After---', temp_dict)
        return temp_dict

if __name__ == '__main__':
    check_config = CheckRequest(config=LoadConfiguration().load_configuration()).check_post_request()