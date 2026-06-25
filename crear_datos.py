from app import create_app, db
from app.models import Rol, Usuario, Categoria, Proveedor, Medicamento, Cliente

app = create_app()
with app.app_context():
    # 1. Crear roles
    roles = ['admin', 'farmaceutico', 'cajero']
    for nombre in roles:
        if not Rol.query.filter_by(nombre=nombre).first():
            rol = Rol(nombre=nombre)
            db.session.add(rol)
    db.session.commit()
    print("✅ Roles creados")

    # 2. Crear usuario admin
    if not Usuario.query.filter_by(username='admin').first():
        admin_rol = Rol.query.filter_by(nombre='admin').first()
        admin = Usuario(username='admin', rol_id=admin_rol.id)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario admin creado: admin / admin123")

    # 3. Crear categorías
    categorias = ['Analgésicos', 'Antibióticos', 'Antiinflamatorios', 'Vitaminas']
    for nombre in categorias:
        if not Categoria.query.filter_by(nombre=nombre).first():
            cat = Categoria(nombre=nombre)
            db.session.add(cat)
    db.session.commit()
    print("✅ Categorías creadas")

    # 4. Crear proveedores
    proveedores = [
        {'nombre': 'Lab Farma S.A.', 'telefono': '777-1234', 'email': 'ventas@labfarma.com'},
        {'nombre': 'Distribuidora Medica', 'telefono': '777-5678', 'email': 'info@distmedica.com'},
    ]
    for p in proveedores:
        if not Proveedor.query.filter_by(nombre=p['nombre']).first():
            prov = Proveedor(**p)
            db.session.add(prov)
    db.session.commit()
    print("✅ Proveedores creados")

    # 5. Crear medicamentos
    categoria_analgesicos = Categoria.query.filter_by(nombre='Analgésicos').first()
    categoria_antibioticos = Categoria.query.filter_by(nombre='Antibióticos').first()
    proveedor1 = Proveedor.query.filter_by(nombre='Lab Farma S.A.').first()
    proveedor2 = Proveedor.query.filter_by(nombre='Distribuidora Medica').first()

    medicamentos = [
        {'nombre': 'Paracetamol 500mg', 'descripcion': 'Analgésico y antipirético', 'precio': 15.50, 'stock': 100, 'stock_minimo': 10, 'categoria_id': categoria_analgesicos.id, 'proveedor_id': proveedor1.id},
        {'nombre': 'Ibuprofeno 400mg', 'descripcion': 'Antiinflamatorio', 'precio': 25.00, 'stock': 80, 'stock_minimo': 8, 'categoria_id': categoria_analgesicos.id, 'proveedor_id': proveedor1.id},
        {'nombre': 'Amoxicilina 500mg', 'descripcion': 'Antibiótico de amplio espectro', 'precio': 45.00, 'stock': 60, 'stock_minimo': 5, 'categoria_id': categoria_antibioticos.id, 'proveedor_id': proveedor2.id},
    ]
    for m in medicamentos:
        if not Medicamento.query.filter_by(nombre=m['nombre']).first():
            med = Medicamento(**m)
            db.session.add(med)
    db.session.commit()
    print("✅ Medicamentos creados")

    # 6. Crear clientes
    clientes = [
        {'nombre': 'Ana Pérez', 'telefono': '777-1111', 'email': 'ana@email.com'},
        {'nombre': 'Luis Gómez', 'telefono': '777-2222', 'email': 'luis@email.com'},
    ]
    for c in clientes:
        if not Cliente.query.filter_by(nombre=c['nombre']).first():
            cli = Cliente(**c)
            db.session.add(cli)
    db.session.commit()
    print("✅ Clientes creados")

    print("✅ DATOS DE PRUEBA CREADOS EXITOSAMENTE")