
# En tu_app/views.py
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from .models import Users, Role
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from .serializers import LoginSerializer
from django.contrib.auth.hashers import make_password
from .utils.getUserFormToken import get_user_from_token
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken




@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
           
            user = authenticate(request, username=username, password=password)
         
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({'message': 'Inicio de sesión exitoso', 'access_token': str(refresh.access_token),'user': {
                        'id': user.id,
                        'username': user.username,
                        'role':user.role
                        # Aquí puedes incluir más campos del usuario si lo deseas
                    }}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Nombre de usuario o contraseña incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Se esperaba una solicitud POST'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@api_view(['POST'])
def create_user(request):

    # Obtén los datos del formulario
    username = request.data.get('username')
    password = request.data.get('password')
    display_name = request.data.get('displayName')
    role_id = request.data.get('role_id')
    
    # Verifica si se proporcionó un nombre de usuario
    if not username:
        return JsonResponse({'error': 'El nombre de usuario es requerido'}, status=400)

    # Verifica si el nombre de usuario ya existe
    if Users.objects.filter(username=username).exists():
        return JsonResponse({'error': 'El nombre de usuario ya está en uso'}, status=400)

    
    # Si no se proporciona un nombre de rol, utiliza el rol de cliente por defecto
    if not role_id:
        default_role_name = 'cliente'
        try:
            role = Role.objects.get(name=default_role_name)
        except Role.DoesNotExist:
            # Si no existe un rol de cliente en la base de datos, crea uno
            role = Role.objects.create(name=default_role_name)
    else:
        # Verifica si el rol especificado existe en la base de datos
        try:
            role = Role.objects.get(name='cliente')
        except Role.DoesNotExist:
            return JsonResponse({'error': 'El rol especificado no existe'}, status=400)
    
        

    # Encripta la contraseña antes de guardarla
    hashed_password = make_password(password)

    # Crea un nuevo usuario con la contraseña encriptada
    user = Users.objects.create(username=username, password=password, displayName = display_name, role=role)

    return JsonResponse({'message': 'Usuario creado correctamente'}, status=201)

    return JsonResponse({'error': 'Se esperaba una solicitud POST'}, status=400)
@permission_classes([IsAuthenticated])
@csrf_exempt

def read_user(request, user_id):
    if request.method == 'GET':
        # Lógica para leer los detalles de un usuario
        try:
            user = Users.objects.get(id=user_id)
            data = {
                'id': user.id,
                'username': user.username,
                'role': user.role if user.role else None,
                'displayName':user.displayName, 
                'photo':user.photo, 
                'email':user.email
            }
            return JsonResponse(data)
        except Users.DoesNotExist:
            return JsonResponse({'error': 'El usuario especificado no existe'}, status=404)
        
@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['PUT'])
def update_user(request, user_id):
   
    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return JsonResponse({'error': 'El usuario especificado no existe'}, status=404)
    print(request), "err-------"
    if user != request.user:
        
        return JsonResponse({'error': 'No tienes permiso para realizar esta acción'}, status=403)

    if request.method == 'PUT':
        allowed_fields = {'username', 'displayName', 'photo', 'role_id'}
        
        request_fields = set(request.data.keys())

        # Verificar si hay campos no permitidos en la solicitud
        if not request_fields.issubset(allowed_fields):
            return JsonResponse({'error': 'Se enviaron campos no permitidos'}, status=400)
        
        username = request.data.get('username')
        displayName = request.data.get('displayName')
        photo = request.data.get('photo')
        role_id = request.data.get('role_id')

        if username:
            user.username = username
        if displayName:
            user.displayName = displayName
        if photo:
            user.photo = photo
        if role_id:
            try:
                role = Role.objects.get(id=role_id)
                user.role = role
            except Role.DoesNotExist:
                return JsonResponse({'error': 'El rol especificado no existe'}, status=400)

        user.save()
        return JsonResponse({'message': 'Usuario actualizado correctamente'})
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['PUT'])
def update_password(request, user_id):
    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return JsonResponse({'error': 'El usuario especificado no existe'}, status=404)
    
    if user != request.user:
        return JsonResponse({'error': 'No tienes permiso para realizar esta acción'}, status=403)

    if request.method == 'PUT':
        password = request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
            return JsonResponse({'message': 'Contraseña actualizada correctamente'})
        return JsonResponse({'error': 'La contraseña es requerida'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@permission_classes([IsAuthenticated])
@csrf_exempt

def delete_user(request, user_id):
    if request.method == 'DELETE':
        # Lógica para eliminar un usuario
        try:
            user = Users.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': 'Usuario eliminado correctamente'})
        except Users.DoesNotExist:
            return JsonResponse({'error': 'El usuario especificado no existe'}, status=404)
        


def generate_temp_password(length=8):
    chars = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    return ''.join(random.choice(chars) for _ in range(length))

@api_view(['POST'])
def password_reset_request(request):
    email = request.data.get('email')
    if not email:
        return JsonResponse({'error': 'El correo electrónico es requerido'}, status=400)
    
    try:
        user = Users.objects.get(email=email)
    except Users.DoesNotExist:
        return JsonResponse({'error': 'El usuario con ese correo electrónico no existe'}, status=404)

    token = default_token_generator.make_token(user)
    uid = user.pk
    current_site = get_current_site(request)
    domain = current_site.domain
    temp_password = generate_temp_password()
    link = f'http://{domain}/api/reset_password_confirm/{uid}/{token}/{temp_password}/'
    
    mail_subject = 'Restablecimiento de contraseña'
    js_script = '''
        <script>
        document.getElementById('confirmButton').onclick = function() {
            this.style.pointerEvents = 'none';  // Inhabilita los eventos de clic
            this.style.opacity = 0.5;  // Reduce la opacidad para indicar que está deshabilitado
        };
        </script>
    '''
    message = f'''
        Hola {user.username},<br><br>
        Has solicitado restablecer tu contraseña. Tu contraseña temporal es: {temp_password}<br><br>
        Haz clic en el botón a continuación para confirmar el cambio:<br><br>
        <form action="{link}" method="post">
            <button type="submit" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border: none;">Confirmar Cambio de Contraseña</button>
        </form><br><br>
        Si no solicitaste este cambio, ignora este correo electrónico.
    '''

    
    send_mail(mail_subject, '', 'santiagomunoz318@gmail.com', ['santiagomunoz318@gmail.com'], html_message=message + js_script)
    
    return JsonResponse({'message': 'Correo electrónico de restablecimiento de contraseña enviado'}, status=200)

def invalidate_jwt_token(user):
    # Obtener el token JWT actual del usuario
    token = UntypedToken.from_token_string(user.token)
    
    # Agregar el token a la lista negra (blacklist)
    BlacklistedToken.objects.create(token=token)

    # Limpiar el token actual del usuario para indicar que ya no es válido
    user.token = None
    user.save()

@api_view(['POST'])
def password_reset_confirm(request, id, token, password):
    try:
        uid = id
        user = Users.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
        return JsonResponse({'error': 'El enlace de restablecimiento de contraseña no es válido'}, status=400)

    if not default_token_generator.check_token(user, token):
        return JsonResponse({'error': 'El enlace de restablecimiento de contraseña no es válido'}, status=400)

    if not password:
        return JsonResponse({'error': 'La nueva contraseña es requerida'}, status=400)

    user.set_password(password)
    user.save()
    token.blacklist()
    return JsonResponse({'message': 'Contraseña restablecida correctamente'}, status=200)