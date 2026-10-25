import json
import sys

def calcular_total(precios):
    """Calcula el total y captura errores de datos."""
    try:
        if not isinstance(precios, list):
            raise TypeError("Los precios deben enviarse en una lista.")
        if not precios:
            raise ValueError("La lista de precios no puede estar vacía.")

        precios_numericos = [float(precio) for precio in precios]
        if any(precio < 0 for precio in precios_numericos):
            raise ValueError("Los precios no pueden ser negativos.")

        return {"estado": "ok", "total": round(sum(precios_numericos), 2)}
    except (TypeError, ValueError) as error:
        return {"estado": "error", "mensaje": str(error)}


def procesar_pedido(productos):
    """Valida un pedido e integra el cálculo del total."""
    try:
        if not isinstance(productos, list):
            raise TypeError("El pedido debe enviarse como una lista.")
        if not productos:
            raise ValueError("El pedido no puede estar vacío.")

        precios = []
        for producto in productos:
            if not isinstance(producto, dict):
                raise TypeError("Cada producto debe ser un objeto.")
            if "precio" not in producto:
                raise KeyError("precio")
            precios.append(producto["precio"])

        resultado = calcular_total(precios)
        if resultado["estado"] == "error":
            return resultado

        return {
            "estado": "ok",
            "cantidad_productos": len(productos),
            "total": resultado["total"],
        }
    except (TypeError, ValueError, KeyError) as error:
        return {"estado": "error", "mensaje": str(error)}


def main():
    """Punto de entrada para ejecutar el sistema desde la terminal."""
    if len(sys.argv) > 1:
        try:
            pedido = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            resultado = {
                "estado": "error",
                "mensaje": "El argumento debe contener JSON válido.",
            }
            print(json.dumps(resultado, ensure_ascii=False))
            return 1
    else:
        pedido = [
            {"nombre": "Teclado", "precio": 350},
            {"nombre": "Mouse", "precio": 150},
        ]

    resultado = procesar_pedido(pedido)
    print(json.dumps(resultado, ensure_ascii=False))
    return 0 if resultado["estado"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
