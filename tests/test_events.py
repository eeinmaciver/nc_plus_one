def test_get_events_returns_200(client):
    response = client.get("/api/events")
    assert response.status_code == 200

def test_get_events_returns_list(client):
    response = client.get("/api/events")
    event_dict = response.json()
    assert isinstance(event_dict["events"], list) == True

def test_get_events_in_order_of_event_id(client):
    response = client.get("/api/events")
    event_dict = response.json()
    event_list = event_dict["events"]
    assert event_dict["events"] != event_list[::-1]
    assert event_dict["events"] == event_list

def test_get_event_id_returns_200(client):
    response = client.get("/api/events/1")
    assert response.status_code == 200

def test_get_event_id_returns_object_with_event_key(client):
    response = client.get("/api/events/2")
    event_dict = response.json()
    assert isinstance(event_dict, dict)
    assert "event" in event_dict

def test_event_id_does_not_find_any_event_returns_404(client):
    response = client.get("/api/events/999")
    assert response.status_code == 404
    assert response.json()["error"] == "Event not found"

def test_event_id_is_valid_integer_return_400_if_not(client):
    response = client.get("/api/events/abc")
    print(response.status_code, response.json())
    assert response.status_code == 400
    assert response.json()["error"] == "ID is not a valid integer"