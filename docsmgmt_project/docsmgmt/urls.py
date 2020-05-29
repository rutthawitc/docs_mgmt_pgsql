from django.urls import path, include
from django.conf.urls import url
from .views import Home, ShowAllDocuments, ShowDocsByDept, DocAccepted, DocDetail, ShowUnreadDocs, ShowAcceptedDocs, loginuser, logoutuser, getcomment, change_password, searchdocs, listusers_accepted

urlpatterns = [
    path('', Home, name='home'),
    path('showall/', ShowAllDocuments, name='showalldocs'),
    path('showbydept/', ShowDocsByDept, name='showbydept'),
    path('accepted/', DocAccepted, name='accepted'),
    path('docdetail/<int:doc_pk>', DocDetail, name='docdetail'),
    path('unread/', ShowUnreadDocs, name='unread'),
    path('showaccepted/', ShowAcceptedDocs, name='showaccepted'),
    path('login/', loginuser, name='loginuser'),
    path('logout/', logoutuser, name='logoutuser'),
    path('getcomment/', getcomment, name='getcomment'),
    path('searchdocs/', searchdocs, name='searchdocs'),
    path('listaccepted/<int:doc_pk>', listusers_accepted, name='listaccepted'),
    url(r'^password/$', change_password, name='change_password'),
]