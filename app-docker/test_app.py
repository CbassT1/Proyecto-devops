import pytest
from app import app

@pytest.fixture
def client():
    # Configuramos la app en modo de prueba
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_route(client):
    """Prueba de Integracion: Verifica que la ruta principal devuelva HTTP 200 y el texto correcto"""
    response = client.get('/')
    
    # Se valida que el servidor responda con exito 
    assert response.status_code == 200
    
    # Validamos que el mensaje esperado este en la respuesta
    assert b"Soluciones Tecnologicas del Futuro" in response.data