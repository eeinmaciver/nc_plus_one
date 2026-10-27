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

def test_get_event_id_returns_200(client):
    response = client.get("/events/1")
    assert response.status_code == 200

def test_get_event_id_returns_object_with_event_key(client):
    response = client.get("/events/2")
    event_dict = response.json()
    result = {
        'event_id': 2,
        'title': 'Intro to Machine Learning Workshop',
        'description': 'Hands-on workshop covering perceptrons, neural networks, and classifiers '
        'using NumPy and PyTorch.',
        'starts_at': '2026-06-25T10:00:00+01:00',
        'ends_at': '2026-06-25T13:00:00+01:00',
        'name': 'Online – Zoom',
        'address': None,
        'capacity': 500,
        'created_at': '2026-10-27T10:37:19.219261+00:00',
    }
    assert event_dict["event"] == result

def test_event_id_does_not_find_any_event_returns_404(client):
    response = client.get("/events/999")
    assert response.status_code == 404
    assert response.json()["error"] == "Event not found"

def test_event_id_is_valid_integer_return_400_if_not(client):
    response = client.get("/events/abc")
    print(response.status_code, response.json())
    assert response.status_code == 400
    assert response.json()["error"] == "ID is not a valid integer"