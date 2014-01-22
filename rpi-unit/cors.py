from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from six import string_types

AccessControlAllowOrigin = 'Access-Control-Allow-Origin'

def cross_origin(origins='*', methods=['GET','HEAD','POST','OPTIONS','PUT'],
           headers=None, supports_credentials=False, max_age=None, 
           send_wildcard=True, always_send=True, automatic_options=False):
    methods = methods or ['GET','HEAD','POST','OPTIONS','PUT']
    methods = ', '.join(sorted(x.upper() for x in methods))

    if headers is not None and not isinstance(headers, string_types):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origins, string_types):
        origins = ', '.join(origins)
    wildcard = origins == '*'

    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if not 'Origin' in request.headers and not always_send:
                return make_response(f(*args, **kwargs))

            elif not wildcard and not always_send and not request.headers.get('Origin', '') in origins:
                return make_response(f(*args, **kwargs))

            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))

            h = resp.headers

            if wildcard:
                if send_wildcard:
                    h[AccessControlAllowOrigin] = origins
                else:
                    h[AccessControlAllowOrigin] = request.headers.get('Origin', '*')
            else:
                h[AccessControlAllowOrigin] = request.headers.get('Origin')


            h['Access-Control-Allow-Methods'] = methods
            if max_age:
                h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.required_methods = ['OPTIONS']
        f.provide_automatic_options = automatic_options 

        return update_wrapper(wrapped_function, f)
    return decorator