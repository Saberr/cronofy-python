import json
from unittest import TestCase
from cronofy import Calendar
import responses

DUMMY_CALENDARS = json.loads(
    '{"calendars":'
    '[{"provider_name":"google",'
    '"profile_name":"someone@somewhere.com",'
    '"calendar_id":"cal_id_1",'
    '"calendar_name":"Calendar 1",'
    '"calendar_readonly":false,'
    '"calendar_deleted":false},'

    '{"provider_name":"google",'
    '"profile_name":"someone@somewhere.com",'
    '"calendar_id":"cal_id_2",'
    '"calendar_name":"CAlendar 2",'
    '"calendar_readonly":false,'
    '"calendar_deleted":false},'

    '{"provider_name":"google",'
    '"profile_name":"someone@somewhere.com",'
    '"calendar_id":"cal_id_3",'
    '"calendar_name":"Calendar 3",'
    '"calendar_readonly":false,'
    '"calendar_deleted":false}]}')


class ResourceTest(TestCase):

    @responses.activate
    def test_calendars_all(self):
        responses.add(responses.GET, 'https://api.cronofy.com/v1/calendars',
                      body=json.dumps(DUMMY_CALENDARS), status=200,
                      content_type='application/json')

        calendars = Calendar.all(access_token="DUMMY")

        self.assertEqual(3, len(calendars))