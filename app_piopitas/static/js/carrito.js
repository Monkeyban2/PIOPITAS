document.addEventListener('DOMContentLoaded', () => {
    const botonesAnadir = document.querySelectorAll('.añadir_carrito');
    const contenedorCarrito = document.querySelector('#carrito-contenido');
    const contenedorTotal = document.querySelector('.carrito__total');
    const botonCheckout = document.querySelector('.carrito__checkout');
    const seccionCarrito = document.querySelector('#carrito');

    const csrfToken = seccionCarrito ? seccionCarrito.dataset.csrf : null;
    const estaLogueado = seccionCarrito ? seccionCarrito.dataset.logueado === '1' : false;
    const urlPedido = seccionCarrito ? seccionCarrito.dataset.urlPedido : null;
    const urlLogin = seccionCarrito ? seccionCarrito.dataset.urlLogin : null;

    let carrito = [];

    function obtenerContenedorNotificaciones() {
        let contenedor = document.querySelector('#notificaciones');
        if (!contenedor) {
            contenedor = document.createElement('div');
            contenedor.id = 'notificaciones';
            document.body.appendChild(contenedor);
        }
        return contenedor;
    }

    function mostrarNotificacion(mensaje, tipo = 'info', duracion = 3200) {
        const contenedor = obtenerContenedorNotificaciones();

        const aviso = document.createElement('div');
        aviso.className = `notificacion notificacion--${tipo}`;
        aviso.textContent = mensaje;

        contenedor.appendChild(aviso);

        requestAnimationFrame(() => aviso.classList.add('notificacion--visible'));

        setTimeout(() => {
            aviso.classList.remove('notificacion--visible');
            aviso.addEventListener('transitionend', () => aviso.remove(), { once: true });
        }, duracion);

        return new Promise((resolve) => setTimeout(resolve, Math.min(duracion, 1400)));
    }

    function agregarAlCarrito(e) {
        const boton = e.target;

        const productoInfo = {
            id: boton.getAttribute('data-id'),
            nombre: boton.getAttribute('data-nombre').replace(/_/g, ' '),
            precio: parseFloat(boton.getAttribute('data-precio')),
            cantidad: 1
        };

        const existe = carrito.some(item => item.id === productoInfo.id);

        if (existe) {
            carrito = carrito.map(item => {
                if (item.id === productoInfo.id) {
                    item.cantidad++;
                    return item;
                } else {
                    return item;
                }
            });
        } else {
            carrito.push(productoInfo);
        }

        actualizarCarritoHTML();
    }

    function actualizarCarritoHTML() {
        contenedorCarrito.innerHTML = '';

        if (carrito.length === 0) {
            contenedorCarrito.innerHTML = '<p class="carrito__vacio">Tu carrito está vacío.</p>';
            contenedorTotal.textContent = 'Total: $0';
            return;
        }

        let total = 0;

        carrito.forEach(item => {
            const itemTotal = item.precio * item.cantidad;
            total += itemTotal;

            const divProducto = document.createElement('div');
            divProducto.classList.add('carrito__item-layout');
            divProducto.style.display = 'flex';
            divProducto.style.justifyContent = 'space-between';
            divProducto.style.alignItems = 'center';
            divProducto.style.marginBottom = '10px';

            divProducto.innerHTML = `
                <div class="carrito__item-info">
                    <p style="margin: 0; font-weight: bold; text-transform: capitalize;">${item.nombre}</p>
                    <small>${item.cantidad} x $${item.precio.toLocaleString('es-CO')}</small>
                </div>
                <div class="carrito__item-acciones" style="display: flex; gap: 10px; align-items: center;">
                    <span style="font-weight: bold;">$${itemTotal.toLocaleString('es-CO')}</span>
                    <button class="btn-eliminar" data-id="${item.id}" style="background: #dc3545; color: white; border: none; padding: 2px 8px; cursor: pointer; border-radius: 3px;">X</button>
                </div>
            `;

            contenedorCarrito.appendChild(divProducto);
        });

        contenedorTotal.textContent = `Total: $${total.toLocaleString('es-CO')}`;

        asignarEventosEliminar();
    }

    function asignarEventosEliminar() {
        const botonesEliminar = document.querySelectorAll('.btn-eliminar');
        botonesEliminar.forEach(boton => {
            boton.onclick = (e) => {
                const idEliminar = e.target.getAttribute('data-id');
                carrito = carrito.filter(item => item.id !== idEliminar);
                actualizarCarritoHTML();
            };
        });
    }

    async function procesarPedido() {
        if (carrito.length === 0) {
            mostrarNotificacion('Tu carrito está vacío.', 'error');
            return;
        }

        if (!estaLogueado) {
            await mostrarNotificacion('Debes iniciar sesión para poder pagar tu pedido.', 'info');
            window.location.href = urlLogin || 'inicioS';
            return;
        }

        botonCheckout.disabled = true;
        botonCheckout.textContent = 'Procesando...';

        try {
            const respuesta = await fetch(urlPedido, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    items: carrito.map(item => ({ id: item.id, cantidad: item.cantidad }))
                })
            });

            const data = await respuesta.json();

            if (respuesta.ok && data.ok) {
                await mostrarNotificacion(`¡Gracias por tu orden! Tu pedido #${data.pedido_id} fue registrado.`, 'exito');
                carrito = [];
                actualizarCarritoHTML();
                window.location.reload();
            } else {
                mostrarNotificacion(data.error || 'No se pudo procesar el pedido. Intenta de nuevo.', 'error');
            }
        } catch (error) {
            mostrarNotificacion('Ocurrió un error al conectar con el servidor. Intenta de nuevo.', 'error');
        } finally {
            botonCheckout.disabled = false;
            botonCheckout.textContent = 'Proceder al pago';
        }
    }

    botonesAnadir.forEach(boton => {
        boton.addEventListener('click', agregarAlCarrito);
    });

    botonCheckout.addEventListener('click', procesarPedido);
});
