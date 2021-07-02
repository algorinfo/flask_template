import json


def test_hello(flaskclient):

    rv = flaskclient.get("/")
    jdata = json.loads(rv.data)
    assert jdata["msg"] == "Hi there!"
