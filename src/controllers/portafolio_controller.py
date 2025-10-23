# backend_file/src/controllers/portafolio_controller.py
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.models import db, Proyecto, Hashtag, Medio

@jwt_required()
def crear_proyecto():
    data = request.get_json()
    campos = ['titulo', 'breve_descripcion', 'descripcion', 'analisis', 'categoria']
    for c in campos:
        if not data.get(c):
            return jsonify({"msg": f"Falta el campo: {c}"}), 400

    p = Proyecto(
        titulo=data['titulo'],
        breve_descripcion=data['breve_descripcion'],
        descripcion=data['descripcion'],
        analisis=data['analisis'],
        categoria=data['categoria'],
        enlace_documentos=data.get('enlace_documentos'),
        enlace_herramienta=data.get('enlace_herramienta'),
        enlace_github=data.get('enlace_github')
    )
    db.session.add(p)
    db.session.flush()

    # Hashtags
    for nombre in data.get('hashtags', []):
        h = Hashtag.query.filter_by(nombre=nombre).first()
        if not h:
            h = Hashtag(nombre=nombre)
            db.session.add(h)
        p.hashtags.append(h)

    # Medios
    for i, m in enumerate(data.get('medios', [])):
        if 'url' in m and 'tipo' in m:
            medio = Medio(url=m['url'], tipo=m['tipo'], orden=i, proyecto_id=p.id)
            db.session.add(medio)

    db.session.commit()
    return jsonify({"msg": "Proyecto creado", "id": p.id}), 201

def obtener_proyectos():
    cat = request.args.get('categoria')
    query = Proyecto.query
    if cat:
        query = query.filter_by(categoria=cat)
    proyectos = query.order_by(Proyecto.created_at.desc()).all()
    res = []
    for p in proyectos:
        miniatura = next((m.url for m in sorted(p.medios, key=lambda x: x.orden) if m.tipo == 'imagen'), None)
        res.append({
            "id": p.id,
            "titulo": p.titulo,
            "breve_descripcion": p.breve_descripcion,
            "categoria": p.categoria,
            "miniatura": miniatura,
            "hashtags": [h.nombre for h in p.hashtags]
        })
    return jsonify(res), 200

def obtener_proyecto(id):
    p = Proyecto.query.get_or_404(id)
    medios = [{"url": m.url, "tipo": m.tipo, "orden": m.orden} for m in p.medios]
    return jsonify({
        "id": p.id,
        "titulo": p.titulo,
        "breve_descripcion": p.breve_descripcion,
        "descripcion": p.descripcion,
        "analisis": p.analisis,
        "categoria": p.categoria,
        "enlace_documentos": p.enlace_documentos,
        "enlace_herramienta": p.enlace_herramienta,
        "enlace_github": p.enlace_github,
        "hashtags": [h.nombre for h in p.hashtags],
        "medios": sorted(medios, key=lambda x: x['orden'])
    }), 200

@jwt_required()
def actualizar_proyecto(id):
    p = Proyecto.query.get_or_404(id)
    data = request.get_json()
    for campo in ['titulo', 'breve_descripcion', 'descripcion', 'analisis', 'categoria']:
        if campo in data:
            setattr(p, campo, data[campo])
    p.enlace_documentos = data.get('enlace_documentos')
    p.enlace_herramienta = data.get('enlace_herramienta')
    p.enlace_github = data.get('enlace_github')

    if 'hashtags' in data:
        p.hashtags.clear()
        for nombre in data['hashtags']:
            h = Hashtag.query.filter_by(nombre=nombre).first()
            if not h:
                h = Hashtag(nombre=nombre)
                db.session.add(h)
            p.hashtags.append(h)

    if 'medios' in data:
        Medio.query.filter_by(proyecto_id=p.id).delete()
        for i, m in enumerate(data['medios']):
            if 'url' in m and 'tipo' in m:
                db.session.add(Medio(url=m['url'], tipo=m['tipo'], orden=i, proyecto_id=p.id))

    db.session.commit()
    return jsonify({"msg": "Proyecto actualizado"}), 200

@jwt_required()
def eliminar_proyecto(id):
    p = Proyecto.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"msg": "Proyecto eliminado"}), 200