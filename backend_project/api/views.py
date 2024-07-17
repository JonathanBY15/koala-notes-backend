# from django.shortcuts import render, redirect
# # from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# # from django.contrib.auth import login, logout
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Note
# from .serializers import NoteSerializer

# # Create your views here.
# # def home_view(request):
# #     """Display the homepage."""
# #     return render(request, 'home.html')

# # def register_view(request):
# #     """Register a new user."""
# #     if request.method == 'POST':
# #         # Grab the data from the user's submission
# #         form = UserCreationForm(request.POST)
# #         if form.is_valid():
# #             # Save the new user to the database and redirect to homepage
# #             form.save()
# #             return redirect('home')
# #     else:
# #         # Display a blank registration form
# #         form = UserCreationForm()

# #     return render(request, 'users/register.html', {'form': form, 'user': request.user})

# # def login_view(request):
# #     """Log in an existing user."""
# #     if request.method == 'POST':
# #         # Grab the data from the user's submission
# #         form = AuthenticationForm(data=request.POST)
# #         if form.is_valid():
# #             # Log in the user and redirect to homepage
# #             login(request, form.get_user())
# #             return redirect('home')
# #     else:
# #         # Display a blank login form
# #         form = AuthenticationForm()

# #     return render(request, 'users/login.html', {'form': form})

# # def logout_view(request):
# #     """Log out the current user."""
# #     if request.method == 'POST':
# #         # Log out the user and redirect to homepage
# #         logout(request)
# #         return redirect('login')

# # API Views

# # @permission_classes([IsAuthenticated])

# # @api_view(['GET', 'POST'])
# # def note_list_create(request):
# #     """List all notes or create a new note."""
# #     if request.method == 'GET':
# #         notes = Note.objects.filter(user=request.user)
# #         serializer = NoteSerializer(notes, many=True)
# #         return Response(serializer.data)

# #     elif request.method == 'POST':
# #         serializer = NoteSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save(user=request.user)
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST'])
# def note_list_create(request):
#     """List all notes or create a new note."""
#     if request.method == 'GET':
#         notes = Note.objects.all()
#         serializer = NoteSerializer(notes, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # @permission_classes([IsAuthenticated])
# @api_view(['GET', 'PUT', 'DELETE'])
# def note_detail(request, pk):
#     """Retrieve, update, or delete a note."""
#     try:
#         note = Note.objects.get(pk=pk, user=request.user)
#     except Note.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = NoteSerializer(note)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = NoteSerializer(note, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)





from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer

# User API endpoints
@api_view(['POST'])
def register(request):
    """Register a new user."""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password)
    return Response({'success': 'User registered successfully'},
                    status=status.HTTP_201_CREATED)

@api_view(['POST'])
def user_login(request):
    """Log in a user."""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request=request._request, username=username, password=password)
    
    if user is not None:
        login(request._request, user)
        return Response({'success': 'User logged in successfully'},
                        status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'},
                        status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def user_logout(request):
    """Log out a user."""
    logout(request)
    return Response({'success': 'User logged out successfully'},
                    status=status.HTTP_200_OK)



# Note API endpoints
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def note_list_create(request):
    """List all notes or create a new note."""
    # if request.method == 'GET':
    #     notes = Note.objects.all()
    #     serializer = NoteSerializer(notes, many=True)
    #     return Response(serializer.data)

    if request.method == 'GET':
        # Filter notes by the logged-in user
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    
    # elif request.method == 'POST':
    #     serializer = NoteSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the currently logged-in user to the note before saving
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def note_detail(request, pk):
    """Retrieve, update, or delete a note."""
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
