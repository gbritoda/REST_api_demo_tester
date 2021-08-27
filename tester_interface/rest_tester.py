import requests
import json
from urllib.parse import urljoin
from tester_interface.cPrint import cPrint, cprint, cprint_err, cprint_suc, cprint_info
import time
import random

class RestTester():
    
    # HTTP Codes - Non Extensive list
    # Success HTTP codes
    SUC_HTTP_OK =       200
    SUC_HTTP_CREATED =  201
    SUC_HTTP_ACCEPTED = 202
    SUC_HTTP_NO_CONTENT = 204 # When successfully deleted or updated
    # Error HTTP codes
    ERR_HTTP_BAD_REQUEST = 400
    ERR_HTTP_NOT_FOUND = 404
    ERR_HTTP_TIMEOUT = 408
    ERR_HTTP_CONFLICT = 409

    # Tests error codes
    ERR_NONE = 0
    ERR_MISSING_FIELD = -1
    ERR_INVALID_FIELD = -2
    ERR_REQ_FAILED = -3
    ERR_TEST_FAILED = -4
    ERR_UNKNOWN = -100

    status_codes = {
        ERR_NONE: "No errors detected",
        ERR_MISSING_FIELD: "Missing field in response",
        ERR_INVALID_FIELD: "Invalid field in response",
        ERR_REQ_FAILED: "A request failed",
        ERR_TEST_FAILED: "The test failed",
        ERR_UNKNOWN: "Unknown error",

        SUC_HTTP_OK: "Successful HTTP request",
        SUC_HTTP_CREATED: "Request has been fulfilled, created new resource",
        SUC_HTTP_ACCEPTED: "The request has been accepted for processing, but"\
            +" the processing has not been completed",
        SUC_HTTP_NO_CONTENT: "The server successfully processed the request,"\
            +" and is not returning any content",
        
        ERR_HTTP_BAD_REQUEST: "The server cannot or will not process the "\
            + "request due to an apparent client error",
        ERR_HTTP_NOT_FOUND: "The requested resource could not be found",
        ERR_HTTP_TIMEOUT: "The server timed out waiting for the request",
        ERR_HTTP_CONFLICT: "Request could not be processed because of conflict"\
            + " in the current state of the resource"
    }

    # Paths
    API_CATEGORIES = "/api/blog/categories/"
    API_POSTS      = "/api/blog/posts/"

    def __init__(self, config_file):
        with open(config_file, 'r') as _f:
            config = json.load(_f)
        self.base_url = config['base_url']

    ###########################################################################
    # 'Private' functions
    ###########################################################################
    def __dec_status(self, status_code):
        """
        Decodes status response if defined within this class
        """
        ret = self.status_codes.get(status_code)
        if ret == None:
            return "Unknown"
        else:
            return ret

    def __check_request_status(self, req, verbose=True):
        ret = self.ERR_UNKNOWN
        if not req.ok:
            if verbose:
                print(f"HTTP Status Error: {req.status_code} - {self.__dec_status(req.status_code)}")
            ret = req.status_code
        else:
            ret = self.ERR_NONE
        return ret
    
    @staticmethod
    def __is_html_error(status_code):
        "Checks if a status code is between 400-499 - HTML Status error"
        return (status_code//100) == 4

    def __get_category_from_id(self, id, resp):
        """
        Gets the blog category from GET api/blog/categories/ response 
        """
        # Getting ID and position of category in relation to response
        _id_list = [_.get('id') for _ in resp]
        idx = _id_list.index(id)
        return resp[idx]

    def get_categories(self):
        """
        Returns list of blog categories
        
        Returns:
            requests.models.Response: Request object from requests library
        """
        _url = urljoin(self.base_url, self.API_CATEGORIES)
        return requests.get(_url)
    
    def post_categories(self, id=None, name="null"):
        """
        Creates new blog category
        
        Args:
            id (int): Other data types allowed for testing purposes
            name (string): Other data types allowed for testing purposes
        Returns:
            requests.models.Response: Request object from requests library
        """
        _url = urljoin(self.base_url, self.API_CATEGORIES)
        data = {}
        if id != None:
            data['id'] = id
        data['name'] = name

        return requests.post(_url, json=data)
    
    def delete_categories(self, id):
        """
        Deletes blog category

        Args:
            id (int)
        Raises:
            TypeError: If id is not an integer
        Returns:
            requests.models.Response: Request object from requests library
        """
        if type(id) != int:
            raise TypeError("id is of type {0}, must be integer.".format(type(id)))
        _url = urljoin(self.base_url, self.API_CATEGORIES)
        return requests.delete(urljoin(_url, str(id)))
    
    def get_category_by_id(self, id):
        if type(id) != int:
            raise TypeError("id is of type {0}, must be integer.".format(type(id)))
        _url = urljoin(self.base_url, self.API_CATEGORIES)
        return requests.get(urljoin(_url, str(id)))

    def put_category_by_id(self, id, name):
        _url = urljoin(self.base_url, self.API_CATEGORIES)
        _url = urljoin(_url, str(id))
        _data = {
            'name': name
        }
        return requests.put(url=_url, json=_data)

    ###########################################################################
    # Basic Tests
    ###########################################################################
    ###########################################################################
    # Basic functional testing
    def test_blog_categories_GET(self):
        req = self.get_categories()
        cprint_info(f"\nINFO: GET. Status Code is {req.status_code}")
        ret = self.__check_request_status(req)
        if ret != self.ERR_NONE:
            return ret
        
        expected_fields = ['id', 'name']
        for item in req.json():
            for _field in expected_fields:
                if _field not in item:
                    cprint_err(f"ERROR: Missing {_field} in response")
                    ret = self.ERR_MISSING_FIELD
            for _field in item:
                if _field not in expected_fields:
                    cprint_err(f"ERROR: Invalid field: {_field}")
                    ret = self.ERR_INVALID_FIELD
        if ret == self.ERR_NONE:
            print("No missing or invalid fields detected")
        return ret

    def test_blog_categories_POST(self, name, id=None):
        req = self.post_categories(id, name)
        cprint_info(f"\nINFO: POST for category '{name}'. Status Code is {req.status_code}")
        return self.__check_request_status(req)
    
    def test_blog_categories_DELETE(self, id):
        req = self.delete_categories(id)
        cprint_info(f"\nINFO: DELETE for id {id}. Status Code is {req.status_code}")
        return self.__check_request_status(req)

    def test_blog_categories_PUT(self, id, new_name):
        req = self.put_category_by_id(id, new_name)
        cprint_info(f"\nINFO: PUT for id {id}. Status Code is {req.status_code}")
        return self.__check_request_status(req)

    def test_blog_category_id_GET(self, id):
        req = self.get_category_by_id(id)
        cprint_info(f"\nINFO: GET for category id {id}. Status Code is {req.status_code}")
        ret = self.__check_request_status(req)
        return ret
    
    ###########################################################################
    # Basic Positive Tests for blog categories
    def test_blog_categories_post__check_post__delete(self, name, id=None):
        print(f"Posting Category: \"{name}\"")
        req = self.post_categories(id=id, name=name)
        cprint_info(f"\nINFO: POST. Status Code is {req.status_code}")
        ret = self.__check_request_status(req)
        if ret != self.ERR_NONE:
            return ret

        req = self.get_categories()
        cprint_info(f"\nINFO: GET. Status Code is {req.status_code}")
        ret = self.__check_request_status(req)
        if ret != self.ERR_NONE:
            return ret
        # Getting response in JSON format
        resp = req.json()
        # Getting ID and position of posted category in relation to response
        _id_list = [_.get('id') for _ in resp]
        # If id is undefined, it will be the biggest number
        if id == None:
            id = max(_id_list)
        idx = _id_list.index(id)
        # Finally we have the corresponding Posted category
        post_obj = resp[idx]

        if post_obj['name'] != name:
            cprint_err("\nERROR: POSTED category name does not match with category name obtained by GET")
            cprint_err(f"POST: \"{name}\" \n GET: \"{post_obj['name']}\" \n")
            ret = self.ERR_INVALID_FIELD
        
        req = self.delete_categories(id)
        cprint_info(f"\nINFO: DELETE ID {id}. Status Code is {req.status_code}")
        http_ret = self.__check_request_status(req)
        
        # If test succeeded, but DELETE request failed
        if ret == self.ERR_NONE and http_ret != self.ERR_NONE:
            return http_ret
        else:
            return ret

    def test_blog_categories_post__delete__get(self, id, name="Null"):
        print(f"Posting Category: \"{name}\"")
        ret = self.test_blog_categories_POST(id=id, name=name)
        if ret != self.ERR_NONE:
            return ret
        
        print(f"Deleting Category: \"{name}\"")
        ret = self.test_blog_categories_DELETE(id)
        if ret != self.ERR_NONE:
            return ret

        ret = self.test_blog_category_id_GET(id)
        if ret == self.ERR_HTTP_NOT_FOUND:
            cprint_suc(f"ID {id} deleted successfully")
            ret = self.ERR_NONE
        elif ret == self.ERR_NONE:
            cprint_err(f"ID {id} was not deleted")
            ret = self.ERR_REQ_FAILED
        else:
            cprint_err(f"Another error ocurred. {self.status_codes[ret]}")
        
        return ret

    def test_blog_categories_post__put__get__delete(self, id, name, new_name):
        print(f"Posting category with id {id} and name {name}")
        ret = self.test_blog_categories_POST(id=id, name=name)
        if ret != self.ERR_NONE:
            return ret
        
        print(f"Updating Category with id {id} to {new_name}")
        ret = self.test_blog_categories_PUT(id=id, new_name=new_name)
        if ret != self.ERR_NONE:
            return ret
        
        print(f"Getting all categories")
        req = self.get_categories()
        resp = req.json()
        categ = self.__get_category_from_id(id=id, resp=resp)
        
        if (categ['name'] == new_name):
            ret = self.ERR_NONE
        else:
            cprint_err(f"\nERROR: Updated name does not match: {new_name} != {categ['name']}\n")
            ret = self.ERR_INVALID_FIELD

        print(f"Deleting Category id {id}")
        del_ret = self.test_blog_categories_DELETE(id)
        if del_ret != self.ERR_NONE:
            cprint_err(f"\nERROR: Failed to delete blog category with id {id}")

        if ret == self.ERR_NONE and del_ret == self.ERR_NONE:
            cprint_suc(f"Test succesful")
            return self.ERR_NONE
    
    ###########################################################################
    # Basic Negative Tests for blog categories
    def test_blog_categories_post_invalid_id_format(self, id, name="Null"):
        post_ret = self.test_blog_categories_POST(id=id, name=name)
        cprint_info(f"Candidate ID: {id}")
        if self.__is_html_error(post_ret):
            cprint_suc("Request rejected successfully")
            return self.ERR_NONE
        else:
            cprint_err("ERROR: Invalid post request was not rejected")
            return self.ERR_TEST_FAILED
    
    def test_blog_categories_post_invalid_name_format(self, name):
        cprint_info(f"Candidate name: {name}")
        post_ret = self.test_blog_categories_POST(id=None, name=name)
        if self.__is_html_error(post_ret):
            cprint_suc("Request rejected successfully")
            return self.ERR_NONE
        else:
            cprint_err("ERROR: Invalid post request was not rejected")
            return self.ERR_TEST_FAILED

    def test_blog_categories_put_invalid_id_format(self, invalid_id):
        cprint_info(f"Candidate id: {invalid_id}")
        put_ret = self.test_blog_categories_PUT(id=invalid_id, new_name="Null")
        if self.__is_html_error(put_ret):
            cprint_suc("Request rejected successfully")
            return self.ERR_NONE
        else:
            cprint_err("ERROR: Invalid put request was not rejected")
            return self.ERR_TEST_FAILED

    def test_blog_categories_put_invalid_name_format(self, invalid_name):
        # Getting a valid ID for the test
        random.seed(time.time())
        req = self.get_categories()
        ret = self.__check_request_status(req, verbose=False)
        if ret != self.ERR_NONE:
            cprint_err("ERROR: Failed to GET blog categories ID in order to fetch valid id")
            return ret
        
        # Choosing ID at random
        resp = req.json()
        _id_list = [_.get('id') for _ in resp]
        id = random.choice(_id_list)

        print(f"Updating Category with id {id} to {invalid_name}")
        put_ret = self.test_blog_categories_PUT(id=id, new_name=invalid_name)
        if self.__is_html_error(put_ret):
            cprint_suc("Request rejected successfully")
            return self.ERR_NONE
        else:
            cprint_err("ERROR: Invalid put request was not rejected")
            return self.ERR_TEST_FAILED

