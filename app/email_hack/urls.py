from django.conf.urls import url
# from django.contrib.auth.views import logout_then_login,login,logout
from .views import home,alldata,help1,user_login,logoutuser
urlpatterns=[
	url(r'^$',user_login),
	# url(r'^login$',login,name='login'),
	# url(r'^logout/$',logout,name='logout'),
	# url(r'^logout-then-login/$',logout_then_login,name='logout_then_login'),
	url(r'^logout/$',logoutuser),
	url(r'^final/$',alldata),
	url(r'^help/$',help1),
	url(r'^people-lookup/$',home,name='people-lookup'),
	# url(r'^logout-then-login/$',logout_then_login,
# name='logout_then_login')

]