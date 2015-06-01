import urllib
import cronofy


class Util():

    def __init__(self):
        pass

    @classmethod
    def get_authorisation_url(cls, redirect_uri, scope="list_calendars read_events read_account", state="state"):
        return "%s/oauth/authorize?response_type=code&" \
               "client_id=%s&" \
               "redirect_uri=%s" \
               "&scope=%s&" \
               "state=%s" % (cronofy.app_base, cronofy.client_id, urllib.quote_plus(redirect_uri), urllib.quote_plus(scope), urllib.quote_plus(state))