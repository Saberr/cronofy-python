import json
import sys
import urllib
import cronofy
import requests


def convert_to_cronofy_object(resp, type):
    types = {'calendar': Calendar}

    if isinstance(resp, list):
        return [convert_to_cronofy_object(i,type) for i in resp]
    elif isinstance(resp, dict) and not isinstance(resp, CronofyObject):
        resp = resp.copy()
        klass_name = type
        if isinstance(klass_name, basestring):
            klass = types.get(klass_name, CronofyObject)
        else:
            klass = CronofyObject
        return klass.construct_from(resp)
    else:
        return resp

class CronofyObject(dict):
    def __init__(self, client_id=None, client_secret=None, **params):
        super(CronofyObject, self).__init__()

        object.__setattr__(self, 'client_id', client_id)
        object.__setattr__(self, 'client_secret', client_secret)

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(CronofyObject, self).__setattr__(k, v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError, err:
            raise AttributeError(*err.args)

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string. "
                "We interpret empty strings as None in requests."
                "You may set %s.%s = None to delete the property" % (
                    k, str(self), k))

        super(CronofyObject, self).__setitem__(k, v)

        # Allows for unpickling in Python 3.x
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()

        self._unsaved_values.add(k)

    def __getitem__(self, k):
        return super(CronofyObject, self).__getitem__(k)


    def __delitem__(self, k):
        raise TypeError(
            "You cannot delete attributes on a CronofyObject. "
            "To unset a property, set it to None.")

    def request(self, method, url, params=None, headers=None):
        if params is None:
            params = self._retrieve_params

        #TODO: do the request

        return {}

    @classmethod
    def construct_from(cls, values):
        instance = cls(values.get('id'))
        instance.refresh_from(values)
        return instance

    def refresh_from(self, values):
        for k, v in values.iteritems():
            super(CronofyObject, self).__setitem__(
                k, convert_to_cronofy_object(v, k))

    def __repr__(self):
        ident_parts = [type(self).__name__]

        if isinstance(self.get('object'), basestring):
            ident_parts.append(self.get('object'))

        if isinstance(self.get('id'), basestring):
            ident_parts.append('id=%s' % (self.get('id'),))

        unicode_repr = '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        return json.dumps(self, sort_keys=True, indent=2)


class APIResource(CronofyObject):

    @classmethod
    def class_name(cls):
        if cls == APIResource:
            raise NotImplementedError(
                'APIResource is an abstract class.  You should perform '
                'actions on its subclasses')
        return str(urllib.quote_plus(cls.__name__.lower()))



class ListableAPIResource(APIResource):

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "/v1/%ss" % (cls_name,)

    @classmethod
    def all(cls, access_token, **params):
        #TODO: put request part in a method in superclass?
        #TODO: add params as querystring items?
        #TODO: wrap HTTP errors and throw our own
        response = requests.get("%s%s" % (cronofy.api_base, cls.class_url(),), headers={'content-type': 'application/json',
                                                                                        'authorization': 'Bearer %s' % access_token})

        if response.status_code == requests.codes.ok:
            items = response.json()["%ss" % cls.class_name().lower()]

            #TODO: add the following of pagination?
            return convert_to_cronofy_object(items, cls.class_name().lower())
        else:
            raise CronofyError("Something is wrong", response.text, response.status_code)



# API objects
class Calendar(ListableAPIResource):
    pass



# Exceptions
class CronofyError(Exception):

    def __init__(self, message=None, http_body=None, http_status=None,
                 json_body=None):
        super(CronofyError, self).__init__(message)

        if http_body and hasattr(http_body, 'decode'):
            try:
                http_body = http_body.decode('utf-8')
            except:
                http_body = ('<Could not decode body as utf-8>')

        self.http_body = http_body

        self.http_status = http_status
        self.json_body = json_body

