from events import  EventsList

class TestEventsList:
    testObj = EventsList()

    def test_not_nill(self):
        assert self.testObj is not None

    def test_get(self):
        results = self.testObj.get()
        print(results['events'])
        assert results['events'][0]['id'] == 1





