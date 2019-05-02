from labkey import utils

# The mocks in the tests expect a request only to be made to the appropriate action.
# This flag disables the CSRF check built into ServerContext.make_request() so the tests
# get consistent results.
utils.DISABLE_CSRF_CHECK = True
