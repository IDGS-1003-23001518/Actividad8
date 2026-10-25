import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "main.py"

def ejecutar_sistema(pedido):
    return subprocess.run(
        [sys.executable, str(MAIN), json.dumps(pedido)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_sistema_pedido_valido():
    pedido = [
        {"nombre": "Teclado", "precio": 350},
        {"nombre": "Mouse", "precio": 150},
    ]

    proceso = ejecutar_sistema(pedido)

    assert proceso.returncode == 0
    assert json.loads(proceso.stdout) == {
        "estado": "ok",
        "cantidad_productos": 2,
        "total": 500.0,
    }


def test_sistema_maneja_exception_y_reporta_error():
    pedido = [{"nombre": "Monitor", "precio": "no-es-numero"}]

    proceso = ejecutar_sistema(pedido)

    assert proceso.returncode == 1
    resultado = json.loads(proceso.stdout)
    assert resultado["estado"] == "error"
    assert "could not convert string to float" in resultado["mensaje"]


def test_sistema_maneja_json_invalido():
    proceso = subprocess.run(
        [sys.executable, str(MAIN), "esto-no-es-json"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert proceso.returncode == 1
    assert json.loads(proceso.stdout) == {
        "estado": "error",
        "mensaje": "El argumento debe contener JSON válido.",
    }
