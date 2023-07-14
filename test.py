import math
from urllib.parse import quote_plus

from fastapi.testclient import TestClient

from ef import app

client = TestClient(app)


def test_get_contacts():
    r = client.get("billetera/contactos?minumero={}".format(quote_plus("21345")))
    assert r.status_code == 200


def test_get_contacts_not_existing_number():
    r = client.get("billetera/contactos?minumero={}".format(quote_plus("999")))
    assert r.status_code == 404


def test_pay_missing_target():
    r = client.get(
        "billetera/pagar?minumero={}&valor={}".format(quote_plus("21345"), 100)
    )
    assert r.status_code == 422


def test_pay_available_exceeded():
    r = client.get(
        "billetera/pagar?minumero={}&numerodestino={}&valor={}".format(
            quote_plus("21345"), quote_plus("123"), 999_999
        )
    )
    assert r.status_code == 400


def test_pay_nonexisting_source():
    r = client.get(
        "billetera/pagar?minumero={}&numerodestino={}&valor={}".format(
            quote_plus("11223344"), quote_plus("123"), 100
        )
    )
    assert r.status_code == 404


def test_pay_target_not_contact():
    r = client.get(
        "billetera/pagar?minumero={}&numerodestino={}&valor={}".format(
            quote_plus("123"), quote_plus("21345"), 100
        )
    )
    assert r.status_code == 400


def test_pay_successful():
    rc = client.get("billetera/historial?minumero={}".format(quote_plus("21345")))
    s1 = rc.json()["saldo"]

    r = client.get(
        "billetera/pagar?minumero={}&numerodestino={}&valor={}".format(
            quote_plus("21345"), quote_plus("123"), 100
        )
    )
    assert r.status_code == 200

    rc = client.get("billetera/historial?minumero={}".format(quote_plus("21345")))
    s2 = rc.json()["saldo"]

    assert math.isclose(s1 - s2, 100)


def test_pay_successful2():
    rc = client.get("billetera/historial?minumero={}".format(quote_plus("456")))
    s1 = rc.json()["saldo"]

    r = client.get(
        "billetera/pagar?minumero={}&numerodestino={}&valor={}".format(
            quote_plus("123"), quote_plus("456"), 20
        )
    )
    assert r.status_code == 200

    rc = client.get("billetera/historial?minumero={}".format(quote_plus("456")))
    s2 = rc.json()["saldo"]

    assert math.isclose(s2 - s1, 20)


def test_get_history():
    r = client.get("billetera/historial?minumero={}".format(quote_plus("21345")))
    rj = r.json()

    assert r.status_code == 200
    assert rj["nombre"] == "Arnaldo"
