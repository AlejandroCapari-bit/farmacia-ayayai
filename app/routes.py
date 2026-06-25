from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Usuario
from io import BytesIO

bp = Blueprint('main', __name__)

# ==================== PÁGINA PRINCIPAL ====================
@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

# ==================== AUTENTICACIÓN ====================
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Bienvenido {user.username}', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('main.login'))

# ==================== DASHBOARD ====================
@bp.route('/dashboard')
@login_required
def dashboard():
    from app.models import Medicamento, Venta, Cliente
    total_medicamentos = Medicamento.query.count()
    total_clientes = Cliente.query.count()
    total_ventas = Venta.query.count()
    stock_bajo = Medicamento.query.filter(Medicamento.stock <= Medicamento.stock_minimo).count()
    
    return render_template('dashboard.html', 
                         total_medicamentos=total_medicamentos,
                         total_clientes=total_clientes,
                         total_ventas=total_ventas,
                         stock_bajo=stock_bajo)

# ==================== CRUD MEDICAMENTOS ====================
@bp.route('/medicamentos')
@login_required
def medicamentos_listar():
    from app.models import Medicamento
    medicamentos = Medicamento.query.all()
    return render_template('medicamentos/listar.html', medicamentos=medicamentos)

@bp.route('/medicamentos/crear', methods=['GET', 'POST'])
@login_required
def medicamentos_crear():
    from app.models import Medicamento, Categoria, Proveedor
    categorias = Categoria.query.all()
    proveedores = Proveedor.query.all()
    
    if request.method == 'POST':
        medicamento = Medicamento(
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock']),
            stock_minimo=int(request.form['stock_minimo']),
            categoria_id=int(request.form['categoria_id']),
            proveedor_id=int(request.form['proveedor_id'])
        )
        db.session.add(medicamento)
        db.session.commit()
        flash('Medicamento creado exitosamente', 'success')
        return redirect(url_for('main.medicamentos_listar'))
    
    return render_template('medicamentos/crear.html', categorias=categorias, proveedores=proveedores)

@bp.route('/medicamentos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def medicamentos_editar(id):
    from app.models import Medicamento, Categoria, Proveedor
    medicamento = Medicamento.query.get_or_404(id)
    categorias = Categoria.query.all()
    proveedores = Proveedor.query.all()
    
    if request.method == 'POST':
        medicamento.nombre = request.form['nombre']
        medicamento.descripcion = request.form['descripcion']
        medicamento.precio = float(request.form['precio'])
        medicamento.stock = int(request.form['stock'])
        medicamento.stock_minimo = int(request.form['stock_minimo'])
        medicamento.categoria_id = int(request.form['categoria_id'])
        medicamento.proveedor_id = int(request.form['proveedor_id'])
        db.session.commit()
        flash('Medicamento actualizado', 'success')
        return redirect(url_for('main.medicamentos_listar'))
    
    return render_template('medicamentos/editar.html', medicamento=medicamento, categorias=categorias, proveedores=proveedores)

@bp.route('/medicamentos/eliminar/<int:id>')
@login_required
def medicamentos_eliminar(id):
    from app.models import Medicamento
    medicamento = Medicamento.query.get_or_404(id)
    db.session.delete(medicamento)
    db.session.commit()
    flash('Medicamento eliminado', 'success')
    return redirect(url_for('main.medicamentos_listar'))

# ==================== CRUD CATEGORIAS ====================
@bp.route('/categorias')
@login_required
def categorias_listar():
    from app.models import Categoria
    categorias = Categoria.query.all()
    return render_template('categorias/listar.html', categorias=categorias)

@bp.route('/categorias/crear', methods=['GET', 'POST'])
@login_required
def categorias_crear():
    if request.method == 'POST':
        from app.models import Categoria
        categoria = Categoria(nombre=request.form['nombre'])
        db.session.add(categoria)
        db.session.commit()
        flash('Categoría creada', 'success')
        return redirect(url_for('main.categorias_listar'))
    return render_template('categorias/crear.html')

@bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def categorias_editar(id):
    from app.models import Categoria
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        categoria.nombre = request.form['nombre']
        db.session.commit()
        flash('Categoría actualizada', 'success')
        return redirect(url_for('main.categorias_listar'))
    return render_template('categorias/editar.html', categoria=categoria)

@bp.route('/categorias/eliminar/<int:id>')
@login_required
def categorias_eliminar(id):
    from app.models import Categoria
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada', 'success')
    return redirect(url_for('main.categorias_listar'))

# ==================== CRUD PROVEEDORES ====================
@bp.route('/proveedores')
@login_required
def proveedores_listar():
    from app.models import Proveedor
    proveedores = Proveedor.query.all()
    return render_template('proveedores/listar.html', proveedores=proveedores)

@bp.route('/proveedores/crear', methods=['GET', 'POST'])
@login_required
def proveedores_crear():
    if request.method == 'POST':
        from app.models import Proveedor
        proveedor = Proveedor(
            nombre=request.form['nombre'],
            telefono=request.form['telefono'],
            email=request.form['email'],
            direccion=request.form['direccion']
        )
        db.session.add(proveedor)
        db.session.commit()
        flash('Proveedor creado', 'success')
        return redirect(url_for('main.proveedores_listar'))
    return render_template('proveedores/crear.html')

@bp.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def proveedores_editar(id):
    from app.models import Proveedor
    proveedor = Proveedor.query.get_or_404(id)
    if request.method == 'POST':
        proveedor.nombre = request.form['nombre']
        proveedor.telefono = request.form['telefono']
        proveedor.email = request.form['email']
        proveedor.direccion = request.form['direccion']
        db.session.commit()
        flash('Proveedor actualizado', 'success')
        return redirect(url_for('main.proveedores_listar'))
    return render_template('proveedores/editar.html', proveedor=proveedor)

@bp.route('/proveedores/eliminar/<int:id>')
@login_required
def proveedores_eliminar(id):
    from app.models import Proveedor
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash('Proveedor eliminado', 'success')
    return redirect(url_for('main.proveedores_listar'))

# ==================== CRUD CLIENTES ====================
@bp.route('/clientes')
@login_required
def clientes_listar():
    from app.models import Cliente
    clientes = Cliente.query.all()
    return render_template('clientes/listar.html', clientes=clientes)

@bp.route('/clientes/crear', methods=['GET', 'POST'])
@login_required
def clientes_crear():
    if request.method == 'POST':
        from app.models import Cliente
        cliente = Cliente(
            nombre=request.form['nombre'],
            telefono=request.form['telefono'],
            email=request.form['email'],
            direccion=request.form['direccion']
        )
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente creado', 'success')
        return redirect(url_for('main.clientes_listar'))
    return render_template('clientes/crear.html')

@bp.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def clientes_editar(id):
    from app.models import Cliente
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.telefono = request.form['telefono']
        cliente.email = request.form['email']
        cliente.direccion = request.form['direccion']
        db.session.commit()
        flash('Cliente actualizado', 'success')
        return redirect(url_for('main.clientes_listar'))
    return render_template('clientes/editar.html', cliente=cliente)

@bp.route('/clientes/eliminar/<int:id>')
@login_required
def clientes_eliminar(id):
    from app.models import Cliente
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente eliminado', 'success')
    return redirect(url_for('main.clientes_listar'))

# ==================== CRUD VENTAS ====================
@bp.route('/ventas')
@login_required
def ventas_listar():
    from app.models import Venta
    ventas = Venta.query.all()
    return render_template('ventas/listar.html', ventas=ventas)

@bp.route('/ventas/crear', methods=['GET', 'POST'])
@login_required
def ventas_crear():
    from app.models import Medicamento, Cliente
    medicamentos = Medicamento.query.all()
    clientes = Cliente.query.all()
    
    if request.method == 'POST':
        from app.models import Venta, DetalleVenta
        cliente_id = int(request.form['cliente_id'])
        usuario_id = current_user.id
        total = 0
        detalles = []
        
        for key in request.form:
            if key.startswith('cantidad_'):
                medicamento_id = int(key.split('_')[1])
                cantidad = int(request.form[key])
                if cantidad > 0:
                    medicamento = Medicamento.query.get(medicamento_id)
                    subtotal = cantidad * medicamento.precio
                    total += subtotal
                    detalles.append({
                        'medicamento_id': medicamento_id,
                        'cantidad': cantidad,
                        'precio_unitario': medicamento.precio,
                        'subtotal': subtotal
                    })
                    medicamento.stock -= cantidad
        
        if total > 0:
            venta = Venta(
                total=total,
                cliente_id=cliente_id,
                usuario_id=usuario_id
            )
            db.session.add(venta)
            db.session.flush()
            
            for d in detalles:
                detalle = DetalleVenta(
                    venta_id=venta.id,
                    medicamento_id=d['medicamento_id'],
                    cantidad=d['cantidad'],
                    precio_unitario=d['precio_unitario'],
                    subtotal=d['subtotal']
                )
                db.session.add(detalle)
            
            db.session.commit()
            flash(f'Venta registrada - Total: Bs. {total:.2f}', 'success')
            return redirect(url_for('main.ventas_listar'))
        else:
            flash('Seleccione al menos un medicamento', 'warning')
    
    return render_template('ventas/crear.html', medicamentos=medicamentos, clientes=clientes)

@bp.route('/ventas/eliminar/<int:id>')
@login_required
def ventas_eliminar(id):
    from app.models import Venta
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    flash('Venta eliminada', 'success')
    return redirect(url_for('main.ventas_listar'))

# ==================== GENERAR FACTURA PDF ====================
@bp.route('/factura/<int:venta_id>')
@login_required
def generar_factura(venta_id):
    from app.models import Venta
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib.utils import ImageReader
    from io import BytesIO
    import os
    
    venta = Venta.query.get_or_404(venta_id)
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # ============ ENCABEZADO ============
    c.setFont("Helvetica-Bold", 20)
    c.drawString(2*cm, height - 2*cm, "FARMACIA AYAYAI")
    
    c.setFont("Helvetica", 10)
    c.drawString(2*cm, height - 2.8*cm, "Tu farmacia de confianza · NIT: 123456-7")
    
    # Línea separadora
    c.line(2*cm, height - 3.2*cm, width - 2*cm, height - 3.2*cm)
    
    # ============ DATOS DE LA FACTURA ============
    c.setFont("Helvetica-Bold", 14)
    c.drawString(width - 6*cm, height - 2*cm, "FACTURA")
    c.setFont("Helvetica", 10)
    c.drawString(width - 6*cm, height - 2.8*cm, f"N° #{venta.id}")
    
    # ============ INFORMACIÓN DEL CLIENTE ============
    y = height - 4.5*cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, y, "DATOS DEL CLIENTE")
    y -= 0.6*cm
    c.setFont("Helvetica", 10)
    c.drawString(2*cm, y, f"Cliente: {venta.cliente.nombre}")
    y -= 0.5*cm
    c.drawString(2*cm, y, f"Teléfono: {venta.cliente.telefono or '—'}")
    y -= 0.5*cm
    c.drawString(2*cm, y, f"Email: {venta.cliente.email or '—'}")
    y -= 0.5*cm
    c.drawString(2*cm, y, f"Fecha: {venta.fecha.strftime('%d/%m/%Y %H:%M')}")
    
    # ============ TABLA DE PRODUCTOS ============
    y = height - 9*cm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2*cm, y, "PRODUCTO")
    c.drawString(10*cm, y, "CANT.")
    c.drawString(13*cm, y, "PRECIO")
    c.drawString(17*cm, y, "SUBTOTAL")
    y -= 0.4*cm
    c.line(2*cm, y, width - 2*cm, y)
    y -= 0.5*cm
    
    c.setFont("Helvetica", 9)
    total = 0
    for detalle in venta.detalles:
        # Recortar nombre si es muy largo
        nombre = detalle.medicamento.nombre[:25] + "..." if len(detalle.medicamento.nombre) > 25 else detalle.medicamento.nombre
        c.drawString(2*cm, y, nombre)
        c.drawString(10*cm, y, str(detalle.cantidad))
        c.drawString(13*cm, y, f"Bs. {detalle.precio_unitario:.2f}")
        c.drawString(17*cm, y, f"Bs. {detalle.subtotal:.2f}")
        y -= 0.6*cm
        
        # Si la factura es muy larga, crear nueva página
        if y < 3*cm:
            c.showPage()
            y = height - 3*cm
            c.setFont("Helvetica-Bold", 10)
            c.drawString(2*cm, y, "PRODUCTO")
            c.drawString(10*cm, y, "CANT.")
            c.drawString(13*cm, y, "PRECIO")
            c.drawString(17*cm, y, "SUBTOTAL")
            y -= 0.5*cm
            c.setFont("Helvetica", 9)
    
    # ============ TOTAL ============
    y -= 0.5*cm
    c.line(12*cm, y, width - 2*cm, y)
    y -= 0.6*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(14*cm, y, f"TOTAL: Bs. {venta.total:.2f}")
    
    # ============ PIE DE PÁGINA ============
    y = 2*cm
    c.setFont("Helvetica", 8)
    c.drawString(2*cm, y, "📧 info@ayayai.com")
    c.drawString(9*cm, y, "📞 (591) 7-123-4567")
    c.drawString(16*cm, y, "📍 Av. Principal #123 · Bolivia")
    
    y = 1.2*cm
    c.drawString(2*cm, y, "¡Gracias por su compra! · Este documento es un comprobante fiscal válido")
    
    c.save()
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'factura_{venta.id}.pdf',
        mimetype='application/pdf'
    )