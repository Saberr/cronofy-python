__author__ = 'nik'


import cronofy

cronofy.client_id = ""
cronofy.client_secret = ""

calendars = cronofy.Calendar.all(access_token="", params=None)
