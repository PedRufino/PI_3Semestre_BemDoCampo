import mongoengine

def tipo_usuario(request):
    db = mongoengine.connection.get_db()
    
    if request.user.is_authenticated:
        user = db.usuarios.find_one({"user_id": request.user.id})
        if user:
            return {'tipo_usuario': user.get('tipo_usuario')}
    
    return {'tipo_usuario': None}
