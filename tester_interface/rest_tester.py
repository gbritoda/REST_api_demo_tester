import requests
import json
from urllib.parse import urljoin
from tester_interface.cPrint import cPrint, cprint, cprint_err, cprint_suc, cprint_info
import time
import random
from shutil import copyfile
import os
from math import ceil

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
    ERR_WRONG_STATUS = -5
    ERR_UNKNOWN = -100

    status_codes = {
        ERR_NONE: "No errors detected",
        ERR_MISSING_FIELD: "Missing field in response",
        ERR_INVALID_FIELD: "Invalid field in response",
        ERR_REQ_FAILED: "A request failed",
        ERR_TEST_FAILED: "The test failed",
        ERR_WRONG_STATUS: "Returned wrong status code",
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

    # Default categories and their ids
    default_categories = {
        #ID : Category
        1: "Sci-Fi",
        2: "Politics",
        3: "Tech"
    }

    # Paths
    API_CATEGORIES = "/api/blog/categories/"
    API_POSTS      = "/api/blog/posts/"
    
    MAX_CHARS = 79 # Python standard
    
    def __init__(self, config_file):
        with open(config_file, 'r') as _f:
            config = json.load(_f)
        self.base_url = config['base_url']
        self.default_db = config['default_db_path']
        self.db_path    = config['database_path']

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
            name (str): Other data types allowed for testing purposes
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
        Returns:
            requests.models.Response: Request object from requests library
        """
        _url = urljoin(self.base_url, self.API_CATEGORIES)
        return requests.delete(urljoin(_url, str(id)))
    
    def get_category_by_id(self, id):
        _url = urljoin(self.base_url, self.API_CATEGORIES)
        return requests.get(urljoin(_url, str(id)))

    def put_category_by_id(self, id, name):
        _url = urljoin(self.base_url, self.API_CATEGORIES)
        _url = urljoin(_url, str(id))
        _data = {
            'name': name
        }
        return requests.put(url=_url, json=_data)
    
    def get_blog_posts(self, params=None):
        """
        Returns list of blog posts
        
        Returns:
            requests.models.Response: Request object from requests library
        """
        _url = urljoin(self.base_url, self.API_POSTS)
        return requests.get(_url, params=params)
    
    def post_blog_posts(self, payload):
        """
        Creates new blog post
        
        Args:
            payload (dict)
        Returns:
            requests.models.Response: Request object from requests library
        """
        _url = urljoin(self.base_url, self.API_CATEGORIES)
        return requests.post(_url, json=payload)
    
    def delete_blog_post(self, id):
        """
        Deletes blog post

        Args:
            id (int)
        Returns:
            requests.models.Response: Request object from requests library
        """
        _url = urljoin(self.base_url, self.API_CATEGORIES)
        return requests.delete(urljoin(_url, str(id)))

    ###########################################################################
    # Basic Tests
    ###########################################################################
    def reset_database_to_default(self):
        """
        Copies default database to the path of the database being used by the
        API
        """
        _src = os.path.abspath(self.default_db)
        _dst = os.path.abspath(self.db_path)
        copyfile(_src, _dst)
    ###########################################################################
    # Basic functional testing
    def test_blog_categories_GET(self):
        req = self.get_categories()
        cprint_info(f"INFO: GET. Status Code is {req.status_code}")
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
        cprint_info(f"INFO: POST for category '{name}'. Status Code is {req.status_code}")
        return self.__check_request_status(req)
    
    def test_blog_categories_DELETE(self, id):
        req = self.delete_categories(id)
        cprint_info(f"INFO: DELETE for id {id}. Status Code is {req.status_code}")
        return self.__check_request_status(req)

    def test_blog_categories_PUT(self, id, new_name):
        req = self.put_category_by_id(id, new_name)
        cprint_info(f"INFO: PUT for id {id}. Status Code is {req.status_code}")
        return self.__check_request_status(req)

    def test_blog_category_id_GET(self, id):
        req = self.get_category_by_id(id)
        cprint_info(f"INFO: GET for category id {id}. Status Code is {req.status_code}")
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

    def test_blog_categories_post__get_by_id__delete(self, id, name):
        print(f"Posting Category: \"{name}\"")
        req = self.post_categories(id=id, name=name)
        cprint_info(f"\nINFO: POST. Status Code is {req.status_code}")
        ret = self.__check_request_status(req)
        if ret != self.ERR_NONE:
            return ret

        req = self.get_category_by_id(id)
        cprint_info(f"\nINFO: GET. Status Code is {req.status_code}")
        ret = self.__check_request_status(req)
        if ret != self.ERR_NONE:
            return ret
        resp = req.json()

        if resp['name'] != name:
            cprint_err("\nERROR: POSTED category name does not match with category name obtained by GET")
            cprint_err(f"POST: \"{name}\" \n GET: \"{resp['name']}\" \n")
            ret = self.ERR_INVALID_FIELD
        if resp['id'] != id:
            cprint_err("\nERROR: POSTED category id does not match with category id obtained by GET")
            cprint_err(f"POST: \"{id}\" \n GET: \"{resp['id']}\" \n")
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

    def test_blog_categories_get_invalid_id(self, invalid_id):
        get_ret = self.test_blog_category_id_GET(invalid_id)
        cprint_info(f"Candidate id: {invalid_id}".center(self.MAX_CHARS, '#'))
        if (get_ret == self.ERR_HTTP_BAD_REQUEST) or (get_ret == self.ERR_HTTP_NOT_FOUND):
            cprint_suc(f"Invalid id {invalid_id} rejected successfully\n")
            return self.ERR_NONE
        elif self.__is_html_error(get_ret):
            cprint_err("ERROR: Request rejected but with wrong status code.\n")
            return self.ERR_WRONG_STATUS
        elif (get_ret == self.ERR_NONE):
            cprint_err("ERROR: Request was not rejected\n")
            return self.ERR_WRONG_STATUS
        else:
            cprint_err(f"ERROR: {self.__dec_status(get_ret)}")
            return self.get_ret

    def test_blog_categories_post_invalid_id_format(self, id, name="Null"):
        post_ret = self.test_blog_categories_POST(id=id, name=name)
        cprint_info(f"Candidate id: {id}".center(self.MAX_CHARS, '#'))
        if self.__is_html_error(post_ret):
            cprint_suc("Request rejected successfully")
            return self.ERR_NONE
        else:
            cprint_err("ERROR: Invalid post request was not rejected")
            return self.ERR_TEST_FAILED
    
    def test_blog_categories_post_invalid_name_format(self, name):
        cprint_info(f"Candidate name: {name}".center(self.MAX_CHARS, '#'))
        post_ret = self.test_blog_categories_POST(id=None, name=name)
        if self.__is_html_error(post_ret):
            cprint_suc("Request rejected successfully")
            return self.ERR_NONE
        else:
            cprint_err("ERROR: Invalid post request was not rejected")
            return self.ERR_TEST_FAILED

    def test_blog_categories_put_invalid_id_format(self, invalid_id):
        cprint_info(f"Candidate id: {invalid_id}".center(self.MAX_CHARS, '#'))
        put_ret = self.test_blog_categories_PUT(id=invalid_id, new_name="Null")

        if (put_ret == self.ERR_HTTP_BAD_REQUEST) or (put_ret == self.ERR_HTTP_NOT_FOUND):
            cprint_suc(f"Invalid id {invalid_id} rejected successfully\n")
            return self.ERR_NONE
        elif self.__is_html_error(put_ret):
            cprint_err("ERROR: Request rejected but with wrong status code.\n")
            return self.ERR_WRONG_STATUS
        elif (put_ret == self.ERR_NONE):
            cprint_err("ERROR: Request was not rejected\n")
            return self.ERR_WRONG_STATUS
        else:
            cprint_err(f"ERROR: {self.__dec_status(put_ret)}\n")
            return self.put_ret

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
    
    def test_blog_categories_delete_invalid_id(self, invalid_id):
        del_ret = self.test_blog_categories_DELETE(invalid_id)

        if (del_ret == self.ERR_HTTP_BAD_REQUEST) or (del_ret == self.ERR_HTTP_NOT_FOUND):
            cprint_suc(f"Invalid id {invalid_id} rejected successfully\n")
            return self.ERR_NONE
        elif self.__is_html_error(del_ret):
            cprint_err("ERROR: Request rejected but with wrong status code.\n")
            return self.ERR_WRONG_STATUS
        elif (del_ret == self.ERR_NONE):
            cprint_err("ERROR: Request was not rejected\n")
            return self.ERR_WRONG_STATUS
        else:
            cprint_err(f"ERROR: {self.__dec_status(del_ret)}")
            return self.del_ret
    


    ###########################################################################
    # Basic Positive Tests for blog posts
    # CRUD functions of blog posts not needed to be tested
    def test_blog_post_GET(self, page=1, per_page=10):

        self.reset_database_to_default()
        ret = self.ERR_NONE
        params = {}
        params['page'] = int(page)
        params['per_page'] = int(per_page)
        req = self.get_blog_posts(params)
        ret = self.__check_request_status(req)
        if ret != self.ERR_NONE:
            return ret
        resp = req.json()
            
        if resp['page'] != page:
            ret = self.ERR_INVALID_FIELD
            cprint_err(f"ERROR: Invalid 'page' field. Should be {page}, is {resp['page']}")
        if resp['per_page'] != per_page:
            ret = self.ERR_INVALID_FIELD
            cprint_err(f"ERROR: Invalid 'per_page' field. Should be {per_page}, is {resp['per_page']}")
        if resp['per_page']*resp['pages'] < resp['total']:
            ret = self.ERR_INVALID_FIELD
            cprint_err("ERROR: Post number calculations are off.")
            cprint_err(f"Total amount of bigger than can be shown (per_page*pages)")
        if resp['pages'] != ceil(resp['total']/resp['per_page']):
            ret = self.ERR_INVALID_FIELD
            cprint_err("ERROR: Pages calculations are off.")
            cprint_err(f"Total amount is {resp['pages']}")
            cprint_err(f"Should be {resp['total']/resp['per_page']}")
            cprint_err(f"Considering: Total={resp['total']}, per_page={resp['per_page']}")
        return ret

