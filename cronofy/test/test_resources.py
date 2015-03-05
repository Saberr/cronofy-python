import json
from unittest import TestCase
from cronofy import Calendar, Event
import cronofy
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

DUMMY_EVENTS = json.loads(
                          '{"pages":'
                          '{"current":1,"total":2,"next_page":"https://api.cronofy.com/v1/events/pages/08a07b034306679e"},'
                          ''
                          '"events":'
                          '[{"calendar_id":"cal_U9uuErStTG@EAAAB_IsAsykA2DBTWqQTf-f0kJw",'
                          '"event_uid":"evt_external_54008b1a4a41730f8d5c6037",'
                          '"summary":"Company Retreat",'
                          '"description":"",'
                          '"start":"2014-09-06",'
                          '"end":"2014-09-08",'
                          '"deleted":false},'
                          ''
                          '{"calendar_id": "cal_U9uuErStTG@EAAAB_IsAsykA2DBTWqQTf-f0kJw",'
                          '"event_uid":"evt_external_54008b1a4a41730f8d5c6038",'
                          '"summary":"Dinner with Laura",'
                          '"description":"",'
                          '"start":"2014-09-13T19:00:00Z",'
                          '"end":"2014-09-13T21:00:00Z",'
                          '"deleted":false,'
                          '"location":{"description":"Pizzeria"}}]}')

DUMMY_OATH_TOKEN = json.loads(
    '{"token_type":"bearer",'
    '"access_token":"P531x88i05Ld2yXHIQ7WjiEyqlmOHsgI",'
    '"expires_in":3600,'
    '"refresh_token":"3gBYG1XamYDUEXUyybbummQWEe5YqPmf",'
    '"scope":"list_calendars create_event delete_event"}'
)


class ResourceTest(TestCase):

    @responses.activate
    def test_calendars_all(self):
        responses.add(responses.GET, 'https://api.cronofy.com/v1/calendars',
                      body=json.dumps(DUMMY_CALENDARS), status=200,
                      content_type='application/json')

        calendars = Calendar.all(access_token="DUMMY")

        self.assertEqual(3, len(calendars))

    @responses.activate
    def test_events_all(self):
        responses.add(responses.GET, 'https://api.cronofy.com/v1/events',
                      body=json.dumps(DUMMY_EVENTS), status=200,
                      content_type='application/json')

        events = Event.all(access_token="DUMMY")

        self.assertEqual(2, len(events))

    @responses.activate
    def test_token_acquire(self):
        responses.add(responses.POST, 'https://api.cronofy.com/oauth/token',
                      body=json.dumps(DUMMY_OATH_TOKEN), status=200,
                      content_type='application/json')

        token =  cronofy.Token.acquire(code="DUMMY_CODE", original_redirect_uri="http://DUMMY_REDIRECT")

        self.assertEqual(token.access_token, "P531x88i05Ld2yXHIQ7WjiEyqlmOHsgI")