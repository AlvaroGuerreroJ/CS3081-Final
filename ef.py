import datetime
from collections import defaultdict
from typing import List, Set, Tuple, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Operacion:
    pass


class Pago(Operacion):
    def __init__(self, recipient, monto, fecha):
        self.recipient = recipient
        self.monto = monto
        self.fecha = fecha


class Recibido(Operacion):
    def __init__(self, fuente, monto, fecha):
        self.fuente = fuente
        self.monto = monto
        self.fecha = fecha


class Cuenta:
    numero: str
    nombre: str
    saldo: float
    contactos: List[str]

    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos


class Operacion:
    numero_destino: str
    fecha: datetime.datetime
    valor: float

    def __init__(self, numero_destino, fecha, valor):
        self.numero_destino: str = numero_destino
        self.fecha: datetime.datetime = fecha
        self.valor: float = valor


class DB(object):
    pass


bd = DB()
bd.cuentas = {
    "21345": Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    "123": Cuenta("123", "Luisa", 400, ["456"]),
    "456": Cuenta("456", "Andrea", 300, ["21345"]),
}
bd.operaciones = defaultdict(list)


# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


@app.get("/billetera/contactos")
def get_contactos(minumero: str):
    if minumero not in bd.cuentas:
        raise HTTPException(status_code=404, detail=f"{minumero} not registered")

    ret = dict()
    for v in bd.cuentas[minumero].contactos:
        if v not in bd.cuentas:
            raise HTTPException(
                status_code=500, detail=f"{v} (contact of {minumero}) is not registered"
            )
        ret[v] = bd.cuentas[v].nombre

    return ret


@app.get("/billetera/pagar")
def transferir(minumero: str, numerodestino: str, valor: float):
    if minumero not in bd.cuentas:
        raise HTTPException(status_code=404, detail=f"{minumero} not registered")
    u: Cuenta = bd.cuentas[minumero]

    if numerodestino not in bd.cuentas:
        raise HTTPException(status_code=404, detail=f"{numerodestino} not registered")
    ud: Cuenta = bd.cuentas[numerodestino]

    if numerodestino not in u.contactos:
        raise HTTPException(
            status_code=400, detail=f"{numerodestino} not a contact of {minumero}"
        )

    if u.saldo < valor:
        raise HTTPException(
            status_code=400, detail=f"{valor} exceeds the available funds ({u.saldo})"
        )

    u.saldo -= valor
    ud.saldo += valor

    dn = datetime.datetime.now()
    bd.operaciones[minumero].append(Pago(numerodestino, valor, dn))
    bd.operaciones[numerodestino].append(Recibido(minumero, valor, dn))

    return {"date": dn}


@app.get("/billetera/historial")
def historial(minumero: str):
    if minumero not in bd.cuentas:
        raise HTTPException(status_code=404, detail=f"{minumero} not registered")
    u: Cuenta = bd.cuentas[minumero]

    operaciones = []
    for o in bd.operaciones[minumero]:
        operaciones.append({**o.__dict__, "tipo": o.__class__.__name__})

    return {"nombre": u.nombre, "saldo": u.saldo, "operaciones": operaciones}

    u: Cuenta = bd.cuentas[minumero]

    if numerodestino not in bd.cuentas:
        raise HTTPException(status_code=404, detail=f"{numerodestino} not registered")
    ud: Cuenta = bd.cuentas[numerodestino]

    if numerodestino not in u.contactos:
        raise HTTPException(
            status_code=400, detail=f"{numerodestino} not a contact of {minumero}"
        )

    if u.saldo < valor:
        raise HTTPException(
            status_code=400, detail=f"{valor} exceeds the available funds ({u.saldo})"
        )

    u.saldo -= valor
    ud.saldo += valor

    dn = datetime.datetime.now()
    bd.operaciones[minumero].append(Pago(numerodestino, valor, dn))
    bd.operaciones[numerodestino].append(Recibido(minumero, valor, dn))

    return dn


@app.get("/mensajeria/enviar")
def enviar_mensaje(mialias: str, aliasdestino: str, texto: str):
    if mialias not in bd:
        raise HTTPException(status_code=404, detail=f"{mialias} not registered")
    u = bd[mialias]

    if aliasdestino not in bd:
        raise HTTPException(status_code=404, detail=f"{aliasdestino} not registered")

    if aliasdestino not in u.contactos:
        raise HTTPException(
            status_code=404, detail=f"{aliasdestino} not a contact of {mialias}"
        )

    fecha = datetime.datetime.now()
    u.mensajes.append(Mensaje(aliasdestino, fecha, texto))
    return fecha


@app.get("/mensajeria/recibidos")
def mensajes_recibidos(mialias: str):
    if mialias not in bd:
        raise HTTPException(status_code=404, detail=f"{mialias} not registered")

    msgs = []
    for un, user in bd.items():
        if mialias in user.contactos:
            for m in user.mensajes:
                if m.alias_destino == mialias:
                    msgs.append((un, m))

    return msgs
