from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, storage
from django.views import View
from .forms import *
from django.urls import reverse
import string    
import random 
from datetime import datetime, date
import datetime
import pyrebase
import os
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib import messages

# from firebase import firebase

cred = credentials.Certificate("./lenanodrug-firebase-adminsdk-37ucm-d4c7316850.json")
firebase = firebase_admin.initialize_app(cred, {'storageBucket': 'lenanodrug.appspot.com'})
db = firestore.client()

from .decorator import is_login
from django.utils.decorators import method_decorator

# db = firestore.client()



#login
def cek_login(request):
    if request.session['email'] : 
        return function(request, *args, **kwargs)
def index(request):
    if 'email' in request.session : 
        return HttpResponseRedirect(reverse('dashboards'))
    return render(request, 'login.html')
def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return HttpResponseRedirect(reverse('login'))

def login(request):
    return render(request, 'login.html')
def postsignIn(request):
    firebaseConfig = {
        "apiKey": "AIzaSyCwSaua3dJRhGD8zVd_uHB9CfTQE3Q5Yc8",
        "authDomain": "lenanodrug.firebaseapp.com",
        "projectId": "lenanodrug",
        "storageBucket": "lenanodrug.appspot.com",
        "messagingSenderId": "173301267370",
        "appId": "1:173301267370:web:8ef5711422114a8b0949d3",
        "measurementId": "G-SPK5M256V3",
        "databaseURL": "https://lenanodrug.firebaseio.com"
        }
    email=request.POST['email']
    password=request.POST['password']

    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    try:
        login = auth.sign_in_with_email_and_password(email,password)
    except:
        messages.warning(request, 'Username atau Password salah! ')
        return HttpResponseRedirect(reverse('dashboards'))
    print(login)
    if(login):
        request.session['email'] = email
        if(email=='hinanowebapp@gmail.com'):
            return HttpResponseRedirect(reverse('dashboards'))
        else:
            raise PermissionDenied()
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
#dashboard
# @is_login
# @method_decorator(is_login())
def dashboards(request):
    # del request.session['email']
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    print(request.session['email'])
    return render(request, 'dashboard/index.html')
# topics
def topics_index(request):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    docs = db.collection('topics').stream()
    stock = []
    for doc in docs:
        temp = doc.id
        doc = doc.to_dict()
        doc['id'] = temp
        stock.append(doc)
        print(stock)
    return render(request, 'topics/index.html', {'tampil': stock})

def topics_read(request,id):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    doc = db.collection('topics').document(id).get()
    doc = doc.to_dict()
    doc['id']  = id
    return render(request, 'topics/read.html', {'tampil': doc})

class Topics_create(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))

        return render(request, 'topics/create.html')

    def post(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20)) 
        print(request.POST)
        id = str(ran)
        if not request.POST['id'] :
            id = str(ran)
        else: 
            id = request.POST['id']
        db.collection('topics').document(id).set(
            {
                'title': request.POST['title'],
                'description': request.POST['description'],
            }
        )
        return HttpResponseRedirect(reverse('topics'))

class Topics_update(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        doc = db.collection('topics').document(self.kwargs['id']).get()
        # temp = doc.id
        doc = doc.to_dict()
        doc['id'] = self.kwargs['id']
        return render(request, 'topics/update.html',{'tampil': doc})

    def post(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        db.collection('topics').document(self.kwargs['id']).update(
                {
                    'title': request.POST['title'],
                    'description': request.POST['description'],
                }
            )
        return HttpResponseRedirect(reverse('topics'))


class Topics_delete(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        db.collection('topics').document(self.kwargs['id']).delete()
        return HttpResponseRedirect(reverse('topics'))



    
# users
def users_index(request):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    docs = db.collection('users').stream()
    stock = []
    for doc in docs:
        temp = doc.id
        doc = doc.to_dict()
        doc['id'] = temp
        stock.append(doc)
    return render(request, 'users/index.html', {'tampil': stock})

def users_read(request,id):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    doc = db.collection('users').document(id).get()
    doc = doc.to_dict()
    doc['id']  = id
    return render(request, 'users/read.html', {'tampil': doc})
    print(doc)

class Users_create(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'users/create.html')

    def post(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 28)) 
        print(request.POST)
        id = str(ran)
        cr_date = request.POST['birthday']
        cr_date = datetime.datetime.strptime(cr_date, '%m/%d/%Y')
        cr_date = cr_date.strftime("%Y-%m-%d")
        db.collection('users').document(id).set(
            {
                'name': request.POST['name'],
                'gender': request.POST['gender'],
                'email': request.POST['email'],
                'birthday': cr_date,
            }
        )
        return HttpResponseRedirect(reverse('users'))

class Users_update(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        doc = db.collection('users').document(self.kwargs['id']).get()
        # temp = doc.id
        doc = doc.to_dict()
        doc['id'] = self.kwargs['id']
        cr_date = doc.get('birthday')
        cr_date = datetime.datetime.strptime(cr_date, '%Y-%m-%d')
        cr_date = cr_date.strftime("%m/%d/%Y")
        doc['bday'] = cr_date
        return render(request, 'users/update.html',{'tampil': doc})

    def post(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        cr_date = request.POST['birthday']
        cr_date = datetime.datetime.strptime(cr_date, '%m/%d/%Y')
        cr_date = cr_date.strftime("%Y-%m-%d")
        db.collection('users').document(self.kwargs['id']).update(
                {
                    'name': request.POST['name'],
                    'email': request.POST['email'],
                    'birthday': cr_date,
                    'gender': request.POST['gender'],
                }
            )
        return HttpResponseRedirect(reverse('users'))


class Users_delete(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        db.collection('users').document(self.kwargs['id']).delete()
        return HttpResponseRedirect(reverse('users'))

# quizzes
def quizzes_index(request):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    docs = db.collection('quizzes').stream()
    stock = []
    for doc in docs:
        temp = doc.id
        doc = doc.to_dict()
        doc['id'] = temp
        stock.append(doc)
    return render(request, 'quizzes/index.html', {'tampil': stock})

def quizzes_read(request,id):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    doc = db.collection('quizzes').document(id).get()
    doc = doc.to_dict()
    doc['id']  = id
    return render(request, 'quizzes/read.html', {'tampil': doc})
    print(doc)

class Quizzes_create(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'quizzes/create.html')

    def post(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 28)) 
        print(request.POST)
        id = str(ran)
        if not request.POST['id'] :
            id = str(ran)
        else: 
            id = request.POST['id']
        if not request.POST['answer4'] :
            answer = [ request.POST['answer0'],request.POST['answer1'],request.POST['answer2'],request.POST['answer3']]
        else:
            answer = [ request.POST['answer0'],request.POST['answer1'],request.POST['answer2'],request.POST['answer3'],request.POST['answer4']]
        db.collection('quizzes').document(id).set(
            {
                'question': request.POST['question'],
                'detail': request.POST['detail'],
                'true_answer': request.POST['true_answer'],
                'answers': answer,
            }
        )
        return HttpResponseRedirect(reverse('quizzes'))

class Quizzes_update(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        doc = db.collection('quizzes').document(self.kwargs['id']).get()
        # temp = doc.id
        doc = doc.to_dict()
        doc['id'] = self.kwargs['id']
        return render(request, 'quizzes/update.html',{'tampil': doc})

    def post(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        answer4 = request.POST['answer4'] if 'answer4' in request.POST else None
        if(answer4):
            answer = [ request.POST['answer0'],request.POST['answer1'],request.POST['answer2'],request.POST['answer3'],request.POST['answer4']]
        else:
            answer = [ request.POST['answer0'],request.POST['answer1'],request.POST['answer2'],request.POST['answer3']]
        db.collection('quizzes').document(self.kwargs['id']).update(
                {
                'question': request.POST['question'],
                'detail': request.POST['detail'],
                'true_answer': request.POST['true_answer'],
                'answers': answer,
                }
            )
        return HttpResponseRedirect(reverse('quizzes'))


class Quizzes_delete(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        db.collection('quizzes').document(self.kwargs['id']).delete()
        return HttpResponseRedirect(reverse('quizzes'))

# comments
def comments_index(request):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    docs = db.collection('comments').stream()
    stock = []
    for doc in docs:
        temp = doc.id
        doc = doc.to_dict()
        doc['id'] = temp
        stock.append(doc)
    return render(request, 'comments/index.html', {'tampil': stock})

def comments_read(request,id):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    doc = db.collection('comments').document(id).get()
    doc = doc.to_dict()
    doc['id']  = id
    return render(request, 'comments/read.html', {'tampil': doc})
    print(doc)

# records
def records_index(request):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    docs = db.collection('records').stream()
    stock = []
    for doc in docs:
        temp = doc.id
        doc = doc.to_dict()
        doc['id'] = temp
        stock.append(doc)
    return render(request, 'records/index.html', {'tampil': stock})

def records_read(request,id):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    doc = db.collection('records').document(id).get()
    doc = doc.to_dict()
    doc['id']  = id
    return render(request, 'records/read.html', {'tampil': doc})
    print(doc)

# contents
def contents_index(request):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    docs = db.collection('contents').stream()
    stock = []
    for doc in docs:
        temp = doc.id
        doc = doc.to_dict()
        doc['id'] = temp
        stock.append(doc)
    return render(request, 'contents/index.html', {'tampil': stock})

def contents_read(request,id):
    if 'email' not in request.session : 
        return HttpResponseRedirect(reverse('login'))
    doc = db.collection('contents').document(id).get()
    doc = doc.to_dict()
    doc['id']  = id
    return render(request, 'contents/read.html', {'tampil': doc})
    print(doc)

class Contents_create(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        docs = db.collection('topics').stream()
        stock = []
        for doc in docs:
            temp = doc.id
            doc = doc.to_dict()
            doc['id'] = temp
            stock.append(doc)
        a = 1
        return render(request, 'contents/create.html', {'tampil': stock})

    def post(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        coba = {
        "apiKey": "AIzaSyCwSaua3dJRhGD8zVd_uHB9CfTQE3Q5Yc8",
        "authDomain": "lenanodrug.firebaseapp.com",
        "projectId": "lenanodrug",
        "storageBucket": "lenanodrug.appspot.com",
        "messagingSenderId": "173301267370",
        "appId": "1:173301267370:web:8ef5711422114a8b0949d3",
        "measurementId": "G-SPK5M256V3",
        "databaseURL": "https://lenanodrug.firebaseio.com"
        }
        firebase = pyrebase.initialize_app(coba)
        storage = firebase.storage()

        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 28)) 
        print(request.POST)
        id = str(ran)
        if not request.POST['id'] :
            id = str(ran)
        else: 
            id = request.POST['id']

        if request.FILES['datafile_cover']:
            image_cover = request.FILES['datafile_cover']
            storage.child('content/'+id+'/cover.jpeg').put(image_cover)
        else: return 1
        if request.FILES['datafile_doc']:
            document = request.FILES['datafile_doc']
            storage.child('content/'+id+'/document.pdf').put(document)
        else: return 1
        auth = firebase.auth()
        email = "elloyyabest@gmail.com"
        password = "123456"
        user = auth.sign_in_with_email_and_password(email,password)
        url_cover = storage.child('content/'+id+'/cover.jpeg').get_url(user['idToken'])
        url_document = storage.child('content/'+id+'/document.pdf').get_url(user['idToken'])
        print(request.POST['answer'])
        # if request.POST['answer']:
        #     answer = [request.POST['answer']]
        

        # https://oauth2.googleapis.com/token
        db.collection('contents').document(id).set(
            {
                'title': request.POST['title'],
                'description': request.POST['description'],
                'cover': url_cover,
                'topic': request.POST['topic'],
                'document_url': url_document,
                'date': datetime.datetime.utcnow(),
                'videos': request.POST.getlist('answer'),
                'quizzes': request.POST.getlist('quizzes'),
                }
        )
        return HttpResponseRedirect(reverse('contents'))

class Contents_update(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        doc = db.collection('contents').document(self.kwargs['id']).get()
        # temp = doc.id
        doc = doc.to_dict()
        doc['id'] = self.kwargs['id']
        return render(request, 'contents/update.html',{'tampil': doc})

    def post(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        answer4 = request.POST['answer4'] if 'answer4' in request.POST else None
        if(answer4):
            answer = [ request.POST['answer0'],request.POST['answer1'],request.POST['answer2'],request.POST['answer3'],request.POST['answer4']]
        else:
            answer = [ request.POST['answer0'],request.POST['answer1'],request.POST['answer2'],request.POST['answer3']]
        db.collection('contents').document(self.kwargs['id']).update(
                {
                'question': request.POST['question'],
                'detail': request.POST['detail'],
                'true_answer': request.POST['true_answer'],
                'answers': answer,
                }
            )
        return HttpResponseRedirect(reverse('contents'))


class Contents_delete(View):
    def get(self, request, *args, **kwargs):
        if 'email' not in request.session : 
            return HttpResponseRedirect(reverse('login'))
        db.collection('contents').document(self.kwargs['id']).delete()
        coba = {
        "apiKey": "AIzaSyCwSaua3dJRhGD8zVd_uHB9CfTQE3Q5Yc8",
        "authDomain": "lenanodrug.firebaseapp.com",
        "projectId": "lenanodrug",
        "storageBucket": "lenanodrug.appspot.com",
        "messagingSenderId": "173301267370",
        "appId": "1:173301267370:web:8ef5711422114a8b0949d3",
        "measurementId": "G-SPK5M256V3",
        "databaseURL": "https://lenanodrug.firebaseio.com"
        }
        # firebase = pyrebase.initialize_app(coba)
        # storage = firebase.storage()
        # firebase.storage().delete('20180428100432_IMG_5221.JPG')
        return HttpResponseRedirect(reverse('contents'))


def inputfile(request):
    bucket = storage.bucket()
    blob = bucket.blob('images/coba.jpeg')
    outfile='C:\Python\hinano_admin\client1.jpeg'
    with open(outfile, 'rb') as my_file:
        blob.upload_from_file(my_file)
    return render(request, 'login.html')


