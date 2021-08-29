import pytest
import os
from tester_interface.rest_tester import RestTester
from tester_interface.cPrint import cPrint, cprint, cprint_info
import string
import random
import time

global MAX_CHARS
MAX_CHARS = 79 # Python standard

def print_test_title(test_name):
    title = ' ' + test_name + ' '
    title = title.center(MAX_CHARS, '=')
    title = '\n\n' + title + '\n'
    cPrint.cprint(title, cPrint.YELLOW)

class Test_REST():
    @pytest.fixture(autouse=True)
    def _request_test_interface(self):
        self.Tester = RestTester(os.path.abspath('./config.json'))

# Positive test - Check basic functionality, "happy path"
# Negative test - Problem scenarios, with valid or invalid input
# 'Destructive' test - Attempt to break API

###############################################################################
# Database reset to default
    def test_RESET_DATABASE_TO_DEFAULT(self):
        self.Tester.reset_database_to_default()

###############################################################################
# Positive test
    def test_Blog_categories_GET(self):
        print_test_title("Blog Categories - GET")
        assert self.Tester.test_blog_categories_GET() == self.Tester.ERR_NONE

###############################################################################
# Positive test
    @pytest.mark.parametrize("name",
        [("Category name"),
        ("A category name that is quite longer"),
        ("Category@name-with1symbols.")])
    def test_Blog_categories_post_and_get_and_delete(self, name):
        """
        POST blog category, GET it and check that data is consistent, then DELETE
        Mainly to test POST and GET
        """
        print_test_title("Blog Categories - POST, GET, DELETE")
        assert self.Tester.test_blog_categories_post__check_post__delete(name=name) \
            == self.Tester.ERR_NONE, "Failed in one of the steps. Please check report for more details"

###############################################################################
# 'Destructive' test
    def test_Blog_categories_post_and_get_and_delete_big_payload(self):
        """
        POST blog category, GET it and check that data is consistent, then DELETE
        Mainly to test POST and GET
        """
        print_test_title("Blog Categories - POST, GET, DELETE w/ big payload")
        self.Tester.reset_database_to_default()
        success = True
        _chars = string.ascii_lowercase + string.ascii_uppercase
        pld_size = 100 # Initial payload size
        pld_step = 50  # Size that payload will increase for each test case
        n_test_cases = 5
        n_failed = 0

        for i in range(n_test_cases):
            print("")
            ovrsz_pld = "".join([random.choice(_chars) for i in range(pld_size)])
            cprint_info(f" Testing payload of size {pld_size} ".center(MAX_CHARS, '#'))
            cprint_info(f"\nPayload: {ovrsz_pld}")
            ret = \
                 self.Tester.test_blog_categories_post__check_post__delete(name=ovrsz_pld)
            if ret != self.Tester.ERR_NONE:
                success = False
                n_failed += 1
            pld_size += pld_step
        
        assert success, f"{n_failed}/{n_test_cases} test cases failed, please check the test report"


###############################################################################
# Positive test
    @pytest.mark.parametrize("id,name",
        [(4, "Category name"),
        (5, "A category name that is quite longer"),
        (6, "Category@name-with1symbols.")])
    def test_Blog_categories_post_and_get_by_id_and_delete(self, id, name):
        """
        POST blog category, GET it and check that data is consistent, then DELETE
        Mainly to test POST and GET
        """
        print_test_title("Blog Categories - POST, GET by id, DELETE")
        self.Tester.reset_database_to_default()
        assert self.Tester.test_blog_categories_post__get_by_id__delete(id=id, name=name) \
            == self.Tester.ERR_NONE, "Failed in one of the steps. Please check report for more details"

###############################################################################
# 'Destructive' test
    def test_Blog_categories_post_and_get_by_id_and_delete_big_payload(self):
        """
        POST blog category, GET it and check that data is consistent, then DELETE
        Mainly to test POST and GET
        """
        print_test_title("Blog Categories - POST, GET by id, DELETE w/ oversized payload")
        self.Tester.reset_database_to_default()
        success = True
        _chars = string.ascii_lowercase + string.ascii_uppercase
        pld_size = 100 # Initial payload size
        pld_step = 50  # Size that payload will increase for each test case
        n_test_cases = 5
        n_failed = 0
        _id = 4 # Initial id, will increase by one with each test case

        for i in range(n_test_cases):
            print("")
            ovrsz_pld = "".join([random.choice(_chars) for i in range(pld_size)])
            cprint_info(f" Testing payload of size {pld_size} ".center(MAX_CHARS, '#'))
            cprint_info(f"\nPayload: {ovrsz_pld}")
            ret = \
                 self.Tester.test_blog_categories_post__get_by_id__delete(id=_id, name=ovrsz_pld)
            if ret != self.Tester.ERR_NONE:
                success = False
                n_failed += 1
            pld_size += pld_step
            _id += 1
        
        assert success, f"{n_failed}/{n_test_cases} test cases failed, please check the test report"

###############################################################################
# Positive test
    @pytest.mark.parametrize("id,name",
        [(4, "Category name"),
        (5, "A category name that is quite longer"),
        (6, "Category@name-with1symbols.")])
    def test_Blog_categories_post__delete__get(self, id, name):
        """
        POST blog category, DELETE it, and use GET by category id to confirm
        it is deleted
        """
        self.Tester.reset_database_to_default()
        print_test_title("Blog Categories - POST, DELETE, GET")
        assert self.Tester.test_blog_categories_post__delete__get(id=id, name=name) \
            == self.Tester.ERR_NONE, "Failed in one of the steps. Please check report for more details"

###############################################################################
# Positive test
    @pytest.mark.parametrize("id,new_name",
        [(4, "Category name"),
        (5, "A category name that is quite longer"),
        (6, "Category@name-with1symbols.")])
    def test_Blog_categories_post__put__get__delete(self, id, new_name):
        """
        POST blog category, PUT to update it, GET to confirm it is updated,
        DELETE
        """
        print_test_title("Blog Categories - POST, PUT, GET, DELETE")
        self.Tester.reset_database_to_default()
        name = "Null"
        assert self.Tester.test_blog_categories_post__put__get__delete(id=id,
            name=name, new_name=new_name) == self.Tester.ERR_NONE,\
                "Failed in one of the steps. Please check report for more details"

###############################################################################
# 'Destructive' test
    def test_Blog_categories_post__put__get__delete_big_payload(self):
        """
        POST blog category, GET it and check that data is consistent, then DELETE
        Mainly to test POST and GET
        """
        print_test_title("Blog Categories - POST, PUT, GET and DELETE w/ oversized payload")
        self.Tester.reset_database_to_default()
        success = True
        _chars = string.ascii_lowercase + string.ascii_uppercase
        pld_size = 100 # Initial payload size
        pld_step = 50  # Size that payload will increase for each test case
        n_test_cases = 5
        n_failed = 0
        _id = 4 # Initial id, will increase by one with each test case

        for i in range(n_test_cases):
            print("")
            ovrsz_pld = "".join([random.choice(_chars) for i in range(pld_size)])
            cprint_info(f" Testing payload of size {pld_size} ".center(MAX_CHARS, '#'))
            cprint_info(f"\nPayload: {ovrsz_pld}")
            ret = \
                 self.Tester.test_blog_categories_post__put__get__delete(id=_id,
                                            name ="Null",new_name=ovrsz_pld)
            if ret != self.Tester.ERR_NONE:
                success = False
                n_failed += 1
            pld_size += pld_step
            _id += 1
        
        assert success, f"{n_failed}/{n_test_cases} test cases failed, please check the test report"

###############################################################################
# Negative test 
    def test_Blog_categories_get_by_invalid_id(self):
        """
        Tests GET with multiple non integer ids and also with ids that don't
        exist
        """
        print_test_title("Blog categories - GET with invalid id")
        random.seed(time.time())
        n_test_cases = 200
        n_failed = 0
        success = True
        # Resetting database to default so ids are known
        self.Tester.reset_database_to_default()

        # Non existing ids
        cprint_info("Testing non existing ids")
        known_ids = set(self.Tester.default_categories.keys())
        possible_ids = list(set(range(n_test_cases//2)) - known_ids)
        for _id in possible_ids:
            if self.Tester.test_blog_categories_get_invalid_id(_id) != self.Tester.ERR_NONE:
                success = False
                n_failed += 1
        
        # Non integer ids
        _chars = string.ascii_lowercase + string.ascii_uppercase
        for i in range(n_test_cases//2):
            print("")
            id_len = random.randint(1,5) # Random length between 1 and 5
            candidate_id = "".join([random.choice(_chars) for i in range(id_len)])
            ret = \
                self.Tester.test_blog_categories_get_invalid_id(candidate_id)
            if ret != self.Tester.ERR_NONE:
                success = False
                n_failed += 1
        
        assert success, f"{n_failed}/{n_test_cases} test cases failed, please check the test report"

###############################################################################
# Negative test 
    def test_Blog_categories_post_invalid_id_format(self):
        """
        Tests POST with multiple non integer ids and checks if they are rejected
        """
        print_test_title("Blog Categories - POST Invalid id format")
        random.seed(time.time())
        n_test_cases = 100
        # Generating random junk of strings with no digits
        _chars = string.ascii_lowercase + string.ascii_uppercase
        _chars = _chars.replace(':','')
        success = True
        n_failed = 0
        self.Tester.reset_database_to_default()

        for i in range(n_test_cases):
            print("")
            id_len = random.randint(1,5) # Random length between 1 and 5
            candidate_id = "".join([random.choice(_chars) for i in range(id_len)])
            ret = \
                self.Tester.test_blog_categories_post_invalid_id_format(candidate_id)
            if ret != self.Tester.ERR_NONE:
                success = False
                n_failed += 1
        assert success, f"{n_failed}/{n_test_cases} test cases failed, please check the test report"

###############################################################################
# Negative test 
    def test_Blog_categories_post_invalid_name_format(self):
        """
        Tests POST with invalid data types and checks if they are rejected
        """
        print_test_title("Blog Categories - POST Invalid name format")
        random.seed(time.time())
        n_test_cases = 50
        success = True
        n_failed = 0
        self.Tester.reset_database_to_default()

        # Integers
        cprint_info("Testing random integers")
        for i in range(n_test_cases//2):
            print("")
            invalid_name = random.randint(0, 100)
            ret = \
                self.Tester.test_blog_categories_post_invalid_name_format(invalid_name)
            if ret != self.Tester.ERR_NONE:
                sucess = False
        
        # Floats
        cprint_info("Testing random float numbers")
        for i in range(n_test_cases//2):
            print("")
            invalid_name = random.random() * 100
            ret = \
                self.Tester.test_blog_categories_post_invalid_name_format(invalid_name)
            if ret != self.Tester.ERR_NONE:
                sucess = False
                n_failed += 1
        
        assert success, f"{n_failed}/{n_test_cases} test cases failed, please check report"
        
###############################################################################
# Negative test 
    def test_Blog_categories_put_invalid_id_format(self):
        """
        Tests PUT with multiple non integer ids and checks if they are rejected
        Also with non existing ids
        """
        print_test_title("Blog Categories - PUT Invalid id format")
        random.seed(time.time())
        n_test_cases = 200
        # Generating random junk of strings with no digits
        _chars = string.ascii_lowercase + string.ascii_uppercase
        _chars = _chars.replace(':','')
        success = True
        n_failed = 0

        # Resetting database to default so ids are known
        self.Tester.reset_database_to_default()

        # Non existing ids
        cprint_info("Testing non existing ids")
        known_ids = set(self.Tester.default_categories.keys())
        possible_ids = list(set(range(n_test_cases//2)) - known_ids)
        for _id in possible_ids:
            if self.Tester.test_blog_categories_put_invalid_id_format(_id) != self.Tester.ERR_NONE:
                success = False
                n_failed += 1

        # Non integer ids
        for i in range(n_test_cases//2):
            print("")
            id_len = random.randint(1,5) # Random length between 1 and 5
            candidate_id = "".join([random.choice(_chars) for i in range(id_len)])
            ret = \
                self.Tester.test_blog_categories_put_invalid_id_format(candidate_id)
            if ret != self.Tester.ERR_NONE:
                success = False
                n_failed += 1
        assert success, f"{n_failed}/{n_test_cases} test cases failed, please check the test report"

###############################################################################
# Negative test 
    def test_Blog_categories_put_invalid_name_format(self):
        """
        Tests PUT with invalid data types and checks if they are rejected
        """
        print_test_title("Blog Categories - PUT Invalid name format")
        random.seed(time.time())
        n_test_cases = 50
        success = True
        n_failed = 0
        self.Tester.reset_database_to_default()

        # Integers
        cprint_info("Testing random integers")
        for i in range(n_test_cases//2):
            print("")
            invalid_name = random.randint(0, 100)
            ret = \
                self.Tester.test_blog_categories_put_invalid_name_format(invalid_name)
            if ret != self.Tester.ERR_NONE:
                sucess = False
        
        # Floats
        cprint_info("Testing random float numbers")
        for i in range(n_test_cases//2):
            print("")
            invalid_name = random.random() * 100
            ret = \
                self.Tester.test_blog_categories_put_invalid_name_format(invalid_name)
            if ret != self.Tester.ERR_NONE:
                sucess = False
                n_failed += 1
        
        assert success, f"{n_failed}/{n_test_cases} test cases failed, please check report"

###############################################################################
# Negative test
    def test_Blog_categories_delete_invalid_id_format(self):
        """
        Tests DELETE with multiple non integer ids and checks if they are rejected
        Also check non existing ids
        """
        print_test_title("Blog Categories - DELETE Invalid id format")
        random.seed(time.time())
        n_test_cases = 100
        # Generating random junk of strings with no digits
        _chars = string.ascii_lowercase + string.ascii_uppercase
        _chars = _chars.replace(':','')
        success = True
        n_failed = 0

        # Resetting database to default so ids are known
        self.Tester.reset_database_to_default()

        # Non existing ids
        cprint_info("Testing non existing ids")
        known_ids = set(self.Tester.default_categories.keys())
        possible_ids = list(set(range(n_test_cases//2)) - known_ids)
        for _id in possible_ids:
            print("")
            if self.Tester.test_blog_categories_delete_invalid_id(_id) != self.Tester.ERR_NONE:
                success = False
                n_failed += 1

        for i in range(n_test_cases):
            print("")
            id_len = random.randint(1,5) # Random length between 1 and 5
            candidate_id = "".join([random.choice(_chars) for i in range(id_len)])
            ret = \
                self.Tester.test_blog_categories_delete_invalid_id(candidate_id)
            if ret != self.Tester.ERR_NONE:
                success = False
                n_failed += 1
        assert success, f"{n_failed}/{n_test_cases} test cases failed, please check the test report"


###############################################################################
# Basic Positive Tests for blog posts
# Only checking some information. No testing of actual CRUD functions

    def test_Blog_post_GET(self):
        """
        Changes the values of per_page and page and checks if it's consistent
        """
        print_test_title("Blog posts - GET")
        n_test_cases = 100
        random.seed(time.time())
        n_failed = 0
        success = True
        self.Tester.reset_database_to_default()
        
        for i in range(n_test_cases):
            page = random.randint(1,50)
            per_page = random.randint(1,50)

            ret = self.Tester.test_blog_post_GET(page=page, per_page=per_page)
            if ret != self.Tester.ERR_NONE:
                success = False
                n_failed += 1
        
        assert success, f"{n_failed}/{n_test_cases} test cases failed, please check report"

