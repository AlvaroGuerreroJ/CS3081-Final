import math
from urllib.parse import quote_plus

from fastapi.testclient import TestClient

from ef import app

client = TestClient(app)


def test_get_contacts():
    # Probar obtener contactos de número
    r = client.get("billetera/contactos?minumero={}".format(quote_plus("21345")))
    assert r.status_code == 200
    assert r.json() == {"123": "Luisa", "456": "Andrea"}


def test_get_contacts_not_existing_number():
    # Probar obtener contactos de número no registrado
    r = client.get("billetera/contactos?minumero={}".format(quote_plus("999")))
    assert r.status_code == 404


def test_pay_missing_target():
    # Probar intentar pagar sin especificar un numerodestino
    r = client.get(
        "billetera/pagar?minumero={}&valor={}".format(quote_plus("21345"), 100)
    )
    assert r.status_code == 422


def test_pay_available_exceeded():
    # Probar intentar pagar excediendo el monto disponible
    r = client.get(
        "billetera/pagar?minumero={}&numerodestino={}&valor={}".format(
            quote_plus("21345"), quote_plus("123"), 999_999
        )
    )
    assert r.status_code == 400


def test_pay_nonexisting_source():
    # Probar intentar pagar especificando `minumero` no registrado
    r = client.get(
        "billetera/pagar?minumero={}&numerodestino={}&valor={}".format(
            quote_plus("11223344"), quote_plus("123"), 100
        )
    )
    assert r.status_code == 404


def test_pay_target_not_contact():
    # Probar intentar pagar a número que no es contacto
    r = client.get(
        "billetera/pagar?minumero={}&numerodestino={}&valor={}".format(
            quote_plus("123"), quote_plus("21345"), 100
        )
    )
    assert r.status_code == 400


def test_pay_successful():
    # Pago exitoso
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
    # Pago exitoso 2
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
    # Obtener historial de número
    r = client.get("billetera/historial?minumero={}".format(quote_plus("21345")))
    rj = r.json()

    assert rj['saldo'] == 100
    assert rj["nombre"] == "Arnaldo"
