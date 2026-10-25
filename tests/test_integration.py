from main import procesar_pedido


def test_integracion_pedido_valido():
    pedido = [
        {"nombre": "Teclado", "precio": 350},
        {"nombre": "Mouse", "precio": 150},
    ]

    resultado = procesar_pedido(pedido)

    assert resultado == {
        "estado": "ok",
        "cantidad_productos": 2,
        "total": 500.0,
    }


def test_integracion_captura_exception_por_precio_no_numerico():
    pedido = [{"nombre": "Monitor", "precio": "no-es-numero"}]

    resultado = procesar_pedido(pedido)

    assert resultado["estado"] == "error"
    assert "could not convert string to float" in resultado["mensaje"]


def test_integracion_captura_exception_por_precio_ausente():
    pedido = [{"nombre": "Monitor"}]

    resultado = procesar_pedido(pedido)

    assert resultado["estado"] == "error"
    assert "precio" in resultado["mensaje"]
