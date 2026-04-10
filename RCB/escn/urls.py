from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name="home"),
    path('register',views.register,name="register"),
    path('pin generation',views.pin_gen,name="pin"),
    path('validate',views.validate,name="validate"),
    path('checkbalance',views.check_balance,name="checkbalance"),
    path('deposit',views.deposit,name="deposit"),
    path('withdraw',views.withdraw,name="withdraw"),
    path('acc to acc',views.acc_transfer,name="acc_transfer")
]