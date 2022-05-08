from hashlib import new
from events_db import Events_DB

class TestEventsList:
    testObj = None

    def setup(self):
        self.testObj = Events_DB()
        self.testObj.deleteAllEventsExceptOne()

    def teardown(self):
        self.testObj.deleteAllEventsExceptOne()

    def test_not_nill(self):
        assert self.testObj is not None

    def test_get(self):
        results = self.testObj.getAllEvents()
        print(results['events'])
        assert results['events'][0]['id'] == 1
        assert len(results['events']) == 1

    def test_get_one_event(self):
        results = self.testObj.getEventByID(1, "")
        print(results)
        assert results['id'] == 1

    def test_add_event(self):
        data = {
            'title': "Test Title",
            'event_time': "Test Event Time",
            'description': "Test Description",
            'location': "Test Location"
        }
        new_event = self.testObj.addEvent(data)
        print(new_event)
        assert new_event['title'] == "Test Title"
        assert new_event['event_time'] == "Test Event Time"
        assert new_event['description'] == "Test Description"
        assert new_event['location'] == "Test Location"

    def test_delete_event_by_id(self):
        data = {
            'title': "Test Title",
            'event_time': "Test Event Time",
            'description': "Test Description",
            'location': "Test Location"
        }
        count_before_adding_record = self.testObj.countEvents()
        print(count_before_adding_record)

        new_event = self.testObj.addEvent(data)
        print(new_event)
        count_after_adding_record = self.testObj.countEvents()
        assert count_before_adding_record + 1 == count_after_adding_record

        id = new_event['id']
        assert id > 1

        self.testObj.deleteEventByID(id)
        count_after_deleting_record = self.testObj.countEvents()
        assert count_before_adding_record == count_after_deleting_record