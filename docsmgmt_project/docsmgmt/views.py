from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Documents, UserProfile, UserDepartment, Accepted, Comments
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import HttpResponseRedirect
from django.db.models import Q
import json
from django.views.generic import ListView, CreateView, UpdateView
#from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
# Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
@login_required
def Home(request):
    # show document counter on home page.
    # readed
    readed_docs = Accepted.objects.filter(
        Q(is_accepted=True) &
        Q(user__user_id=request.user.profile.id)).values_list('doc_no', flat=True)

    #readed_count = readed_docs.count()

    # ----------Check Role QuerySet---------
    # ----Edited on --25-May-2020----
    if (request.user.profile.role == 1):
        unread_list = Documents.objects.filter(
            Q(role=1) |
            Q(role=3) &
            Q(doc_dept=request.user.profile.dept)
        ).exclude(id__in=readed_docs).order_by('-id')
        docscount = unread_list.count()
    else:
        unread_list = Documents.objects.filter(
            Q(doc_dept=request.user.profile.dept)
        ).exclude(id__in=readed_docs).order_by('-id')

    unread_count = unread_list.count()

    #context = {'unread_count':unread_count, 'readed_count':readed_count}
    context = {'unread_count': unread_count}
    # print(context)
    return render(request, 'docsmgmt/home.html', context)


@login_required
def ShowAllDocuments(request):
    docs = Documents.objects.all()
    error = "ไม่มีเอกสารใหม่"
    context = {'docs': docs, 'error': error}
    return render(request, 'docsmgmt/alldocs.html', context)


@login_required
# Show Unreaded Documents filter by Current User ID!
def ShowUnreadDocs(request):
    # Find Readed (Accepted Documents) - QuerySet
    readed_docs = Accepted.objects.filter(
        Q(is_accepted=True) &
        Q(user__user_id=request.user.profile.id)
    ).values_list('doc_no', flat=True)

# ----------Check Role QuerySet---------
# ----Edited on --25-May-2020----
    if (request.user.profile.role == 1):
        unread_list = Documents.objects.filter(
            Q(role=1) |
            Q(role=3) &
            Q(doc_dept=request.user.profile.dept)
        ).exclude(id__in=readed_docs).order_by('-id')
        docscount = unread_list.count()
    else:
        unread_list = Documents.objects.filter(
            Q(doc_dept=request.user.profile.dept)
        ).exclude(id__in=readed_docs).order_by('-id')

        docscount = unread_list.count()
# ----------End Query----

    # DEBUG
    #print('User Role', request.user.profile.role)
    # print('unread_role',unread_list.values_list())
    #print('User dept',request.user.profile.dept)

    # Paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(unread_list, 15)
    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)

    error = "ไม่มีเอกสารใหม่"
    context = {'error': error, 'docs': docs, 'docscount': docscount}
    return render(request, 'docsmgmt/unread.html', context)


@login_required
# Show Accepted Documents filter by User ID!
def ShowAcceptedDocs(request):
    # Find Readed - QuerySet
    accepted_list = Accepted.objects.filter(
        Q(is_accepted=True) &
        Q(user__user_id=request.user.profile.id)
    ).order_by('-accepted_date')
    acceptedcount = accepted_list.count()
    # Paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(accepted_list, 15)
    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)

    error = {"No data!"}
    context = {'error': error, 'docs': docs, 'acceptedcount': acceptedcount}
    return render(request, 'docsmgmt/showaccepted.html', context)


@login_required
def ShowDocsByDept(request):
    # Complete -QuerySet-
    docs_list = Documents.objects.filter(
        Q(doc_dept=request.user.profile.dept) |
        Q(doc_dept__id=3)
    ).order_by('-doc_dept__id', 'upload_date')
    docscount = docs_list.count()
    # Paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(docs_list, 15)
    # -----DEBUG-------
    # print(paginator.count)
    # print(paginator.num_pages)
    # print(paginator.page_range)
    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)

    error = {"No data!"}
    context = {'docs': docs, 'error': error, 'docscount': docscount}
    return render(request, 'docsmgmt/docsbydept.html', context)


@login_required
def DocAccepted(request):
    data = json.loads(request.body)
    documentId = data['documentId']
    action = data['action']
    # --DEBUG---
    #print('Document Id:', documentId)
    #print('Action:', action)

    # Set values
    user = request.user.profile
    document = Documents.objects.get(id=documentId)

    accepted = Accepted.objects.create(
        user=user, doc_no=document, is_accepted=True)
    accepted.save()
    # --DEBUG---
    #print('User:', user)
    #print('Document ID:', document)

    return JsonResponse('Accepted', safe=False)


@login_required
def DocDetail(request, doc_pk):
    doc = Documents.objects.get(id=doc_pk)
    comments = Comments.objects.filter(doc_no=doc.id)
    usercount = Accepted.objects.filter(
        doc_no=doc_pk, user__dept=request.user.profile.dept, is_accepted=True).count()
    try:
        isaccepted = Accepted.objects.get(doc_no=doc.id, user=request.user.id)
    except Accepted.DoesNotExist:
        isaccepted = None

    context = {'doc': doc, 'isaccepted': isaccepted,
               'comments': comments, 'usercount': usercount}
    return render(request, 'docsmgmt/docdetail.html', context)


def getcomment(request):
    data = json.loads(request.body)
    documentId = data['documentId']
    action = data['action']
    text = data['memo']
    # --DEBUG---
    #print('Document Id:', documentId)
    #print('Action:', action)
    #print('text:', text)

    # Set values
    user = request.user.profile
    document = Documents.objects.get(id=documentId)

    # DEBUG
    # print(user)
    #print('Doc ID :',document.id)
    #print('text:', text)
    comment = Comments.objects.create(user=user, doc_no=document, comment=text)
    comment.save()

    return JsonResponse('Commented', safe=False)


def loginuser(request):
    username_value = ''
    password_vlaue = ''
    if request.method == 'GET':
        return render(request, 'docsmgmt/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        # DEBUG
        # print(request.POST['username'])
        # print(request.POST['password'])
        # print(user)
        if user is None:
            return render(request, 'docsmgmt/login.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')


@login_required
def logoutuser(request):
    # if request.method == 'POST':
    logout(request)
    return HttpResponseRedirect('/login/')

# Change password
@login_required
def change_password(request):
    msg = ''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            msg = 'Your password was successfully updated!'
            # return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
            msg = 'Please correct the error below.'
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form,
        'msg': msg,
    })


@login_required  # User must login first
def searchdocs(request):
    if request.method == 'POST':
        data = request.POST.copy()
        #print('Data:', data)
        search_title = data.get('search')
        if search_title == '':
            return redirect('searchdocs')
        try:
            res = Documents.objects.filter(
                Q(doc_title__contains=search_title) |
                Q(doc_mtno__contains=search_title) &
                Q(doc_dept=request.user.profile.dept)
            ).order_by('-id')
            # print(request.user.profile.dept)
            rescount = res.count()
            context = {'res': res, 'src': 'founded',
                       'rescount': rescount, 'search_title': search_title}
        except Documents.DoesNotExist:
            context = {'res': 'Has no resualt', 'src': 'notfound'}
            #res = 'Has no resualt'
            #print('RES:', context)

        return render(request, 'docsmgmt/searchdoc.html', context)
    return render(request, 'docsmgmt/searchdoc.html')


# List Users accepted --> Doc
@login_required
def listusers_accepted(request, doc_pk):
    context = {}
    doc = Documents.objects.get(id=doc_pk)
    user_list = Accepted.objects.filter(
        doc_no=doc_pk, user__dept=request.user.profile.dept, is_accepted=True).order_by('accepted_date')
    usercount = user_list.count()

    # DEBUG
    # print(user_list)
    # print(usercount)
    context = {'user_list': user_list, 'usercount': usercount, 'doc': doc}
    return render(request, 'docsmgmt/listaccepted.html', context)

# class DocumentView(CreateView):
#    model = Documents
#    fields = ('type_code', 'doc_mtno', 'doc_title', 'doc_desc', 'doc_date', 'doc_dept', 'doc_file')
#    success_url = reverse_lazy('home')

