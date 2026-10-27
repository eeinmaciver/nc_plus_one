def test_get_events_returns_200(client):
    response = client.get("/events")
    assert response.status_code == 200

def test_get_events_returns_list(client):
    response = client.get("/events")
    event_dict = response.json()
    assert isinstance(event_dict["events"], list) == True

def test_get_events_in_order_of_event_id(client):
    response = client.get("/events")
    event_dict = response.json()
    event_list = event_dict["events"]
    assert event_dict["events"] != event_list[::-1]
    assert event_dict["events"] == event_list