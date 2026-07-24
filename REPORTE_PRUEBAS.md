# Reporte de Ejecución de Pruebas — Piopitas

## 1. Alcance

Pruebas unitarias del backend (Django) del proyecto Piopitas: modelos, registro,
inicio de sesión (cliente/administrador), creación de pedidos (descuento de stock)
y recuperación de contraseña.

Total de casos de prueba: **25**, distribuidos así:

| Archivo | Casos | Qué cubre |
|---|---|---|
| `test_models.py` | 8 | `Producto.disponible`, `Categoria.slug`, `Pedido.siguiente_estado`, `ItemPedido.subtotal` |
| `test_registro.py` | 4 | Registro de clientes (válido, email/documento duplicado, contraseña débil) |
| `test_login.py` | 5 | Login de cliente y administrador (válido, inválido, cruce de roles) |
| `test_pedidos.py` | 6 | Creación de pedidos, descuento de stock, stock insuficiente, autenticación |
| `test_admin_panel.py` | 5 | Control de acceso al panel, eliminar producto con/sin pedidos asociados |
| `test_password_reset.py` | 2 | Envío de correo de recuperación (con mock), correo no registrado |

## 2. Cómo se ejecutaron

```
pip install -r requirements-dev.txt
coverage run manage.py test app_piopitas.tests -v 2
coverage report -m
coverage html
```

## 3. Resultados de ejecución

> ⚠️ Completar esta sección pegando la salida real de tu terminal después de correr
> los comandos de arriba. Aquí va el resumen que imprime Django al final
> (algo como `Ran 25 tests in 2.145s` y `OK`, o el detalle de qué falló).

```
(pega aquí la salida de: coverage run manage.py test app_piopitas.tests -v 2)
```

## 4. Cobertura de código

> ⚠️ Completar con la salida de `coverage report -m`.

```
(pega aquí la salida de: coverage report -m)
```

| Módulo | % cobertura esperado |
|---|---|
| `models.py` | Alto (toda la lógica de negocio tiene prueba directa) |
| `forms.py` | Alto (validaciones de registro cubiertas) |
| `views.py` | Medio-alto (login, registro, pedidos y panel admin cubiertos; algunas vistas de solo-lectura sin prueba propia) |

## 5. Registro de defectos encontrados durante el desarrollo

| ID | Defecto | Dónde se encontró | Severidad | Corrección |
|---|---|---|---|---|
| DEF-01 | El campo de contraseña del login tenía `name="username"` duplicado en vez de `name="password"` | `registration/login.html` | Crítica | Se corrigió el atributo `name` del input |
| DEF-02 | El formulario de registro no tenía `method`, `action` ni `{% csrf_token %}` | `registro.html` | Crítica | Se conectó el formulario al backend con `RegistroClienteForm` |
| DEF-03 | El menú mostraba productos fijos en HTML, no venían de la base de datos | `menu.html` | Mayor | Se reemplazó por un `{% for %}` sobre `Categoria`/`Producto` |
| DEF-04 | El carrito no afectaba la base de datos al pagar (solo mostraba una alerta) | `carrito.js` | Mayor | Se conectó a `POST /pedido/crear`, que descuenta stock en una transacción atómica |
| DEF-05 | Ruta al CSS del admin rota (`administrador.cs` + `s` suelto) | `administrador_productos.html` | Menor | Se corrigió la ruta del `{% static %}` |
| DEF-06 | Eliminar un producto con pedidos asociados rompería la base de datos (FK protegida) | `views.py` | Mayor | Se maneja `ProtectedError`: desactiva el producto en vez de borrarlo (cubierto por `test_eliminar_producto_con_pedidos_asociados...`) |

## 6. Criterios de salida

- [ ] 100% de los 25 casos de prueba pasan (`OK` en la salida de Django)
- [ ] Cobertura de `models.py`, `forms.py` y `views.py` revisada
- [ ] Sin defectos críticos o mayores abiertos

## 7. Firma

Preparado por: _______________ Fecha: _______________
