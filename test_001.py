import pytest
import os
from tester_interface.rest_tester import RestTester
from tester_interface.cPrint import cPrint, cprint

def print_test_title(test_name):
    MAX_CHARS = 79 # Python standard
    title = ' ' + test_name + ' '
    title = title.center(MAX_CHARS, '=')
    title = '\n\n' + title + '\n'
    cPrint.cprint(title, cPrint.YELLOW)

class Test_REST():
    @pytest.fixture(autouse=True)
    def _request_test_interface(self):
        self.Tester = RestTester(os.path.abspath('./config.json'))

#TBD add a test to set up the REST api if not already up
###############################################################################
    def test_Blog_categories_GET(self):
        print_test_title("Blog Categories - GET")
        assert self.Tester.test_blog_categories_GET() == self.Tester.ERR_NONE

###############################################################################
    @pytest.mark.parametrize("name",
        [("test description"),
        ("longer test description"),
        ("even longer test description")])
    def test_Blog_categories_post_and_get_and_delete(self, name):
        """
        POST blog category, GET it and check that data is consistent, then DELETE
        Mainly to test POST and GET
        """
        print_test_title("Blog Categories - POST, GET, DELETE")
        assert self.Tester.test_blog_categories_post__check_post__delete(name=name) \
            == self.Tester.ERR_NONE, "Failed in one of the steps. Please check report for more details"

###############################################################################
    @pytest.mark.parametrize("id,name",
        [(4, "test description"),
        (5, "longer test description"),
        (6, "even longer test description")])
    def test_Blog_categories_post__delete__get(self, id, name):
        """
        POST blog category, DELETE it, and use GET by category id to confirm
        it is deleted
        """
        print_test_title("Blog Categories - POST, DELETE, GET")
        assert self.Tester.test_blog_categories_post__delete__get(id=id, name=name) \
            == self.Tester.ERR_NONE, "Failed in one of the steps. Please check report for more details"

###############################################################################
    @pytest.mark.parametrize("id,new_name",
        [(4, "test description"),
        (5, "longer test description"),
        (6, "even longer test description")])
    def test_Blog_categories_post__put__get__delete(self, id, new_name):
        """
        POST blog category, PUT to update it, GET to confirm it is updated,
        DELETE
        """
        print_test_title("Blog Categories - POST, PUT, GET, DELETE")
        name = "Null"
        assert self.Tester.test_blog_categories_post__put__get__delete(id=id,
            name=name, new_name=new_name) == self.Tester.ERR_NONE,\
                "Failed in one of the steps. Please check report for more details"

###############################################################################


