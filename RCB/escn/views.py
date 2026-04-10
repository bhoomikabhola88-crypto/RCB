from django.shortcuts import render,redirect
from .forms import RegisterationForm
from .models import Accounts
from django.core.mail import send_mail
from django.conf  import settings
from django.contrib import messages
from .utils.send_otp import otp

# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    form=RegisterationForm()
    if request.method=='POST':
        form=RegisterationForm(request.POST,request.FILES)
        if form.is_valid():
            phone=form.cleaned_data['phone']
            form.save()
            data=Accounts.objects.get(phone=phone)
            send_mail("thanks for creating Acont in our bank,"f"yo account number is {data.acc_number}\n thak you\nregards\nmanager\n bhoomika",settings.EMAIL_HOST_USER[data.email],fail_silently=True)
            return redirect("home")
        
            
    context={
        'form':form
    } 
    return render(request,'register.html',context)   

def pin_gen(request):
    data=None
    if request.method=='POST':
        acc=int(request.POST.get('acc'))
        phone=int(request.POST.get('phone'))
        aadhar=int(request.POST.get('aadhar'))
        try:
            data=Accounts.objects.get(aadhar=aadhar)
        except:
            messages.error(request,'AAdhar number is invalid ','pin.html')
        if data:
            if data.acc_number==acc:
                if data.phone==phone:
                    one_time_password=otp()
                    request.session['otp']=one_time_password
                    request.session['acc']=data.acc_number
                    send_mail("one time password",f"your one time password is{one_time_password}\n please don't share with anyone\n thank you",settings.EMAIL_HOST_USER,[data.email],fail_silently=True)
                    return redirect("validate")
                else:
                    messages.error(request,'please the registered phone number','pin.html')
            else:
                    messages.error(request,'please check your Account number','pin.html')
    return render(request,'pin.html')

def validate(request):
    if request.method=='POST':
        otp=int(request.session['otp'])
        acc=int(request.session['acc'])
        opt=int(request.POST.get('opt'))
        pin=int(request.POST.get('pin'))
        c_pin=int(request.POST.get('c_pin'))
        #print(otp,opt,acc,pin,c_pin)
        if otp==opt:
            if pin==c_pin:
                data=Accounts.objects.get(acc_number=acc)
                data.set_pin(str(pin))
                data.save()
                return redirect("home")
            else:
                messages.error(request,"pin mismath",'validate.html')
        else:
            messages.error(request,"OTP missmatch",'validate.html')
    return render(request,'validate.html')  


def check_balance(request):
    data=None
    if request.method=="POST":
        acc=request.POST.get('acc')
        pin=request.POST.get('pin')
        #print(acc,pin)
        try:
            data=Accounts.objects.get(acc_number=acc)
        except:
            messages.error(request,"Account number is incorrect")
        if data:
            if int(data.get_pin())==int(pin):
                messages.error(request,f"your current available balance is{data.balance}")
            else:
                messages.error(request,'invalid pin')  
    return render(request,'check_balance.html')


def deposit(request):
    data:None
    if request.method=="POST":
        acc=request.POST.get('acc')
        pin=request.POST.get('pin')
        amt=int(request.POST.get('amt'))
        #print(acc,pin,amt)
        try:
            data=Accounts.objects.get(acc_number=acc)
        except:
          messages.error(request,"Account number is incorrect")
        if data:
            if int(data.get_pin())==int(pin):
                if amt>=100:
                    if amt<=10000:
                        bal=data.balance
                        data.balance=bal+amt
                        data.save()
                        send_mail("AMOUNT CREADITED",f"amount{amt} has been credited to ur account {data.acc_number} vai ATM ur current available is {data.balance}",settings.EMAIL_HOST_USER,[data.email],fail_silently=True)
                        return redirect("home")
                    else:
                        messages.error(request,"pls visit the branch for huge amount deposit")
                else:
                    messages.error(request,"amount is too low for deposit")
            else:
                messages.error(request,"incorrect pin ")
    return render(request,"transaction.html")

def withdraw(request):
    data:None
    if request.method=="POST":
        acc=request.POST.get('acc')
        pin=request.POST.get('pin')
        amt=int(request.POST.get('amt'))
        #print(acc,pin,amt)
        try:
            data=Accounts.objects.get(acc_number=acc)
        except:
          messages.error(request,"Account number is incorrect")
        if data:
            if int(data.get_pin())==int(pin):
                if amt>=100:
                    if amt<=10000:
                        bal=data.balance
                        if amt>=100:
                         data.balance=bal-amt
                         data.save()
                         send_mail("AMOUNT DEBIITED",f"amount{amt} has been debited to ur account {data.acc_number} vai ATM ur current available is {data.balance}",settings.EMAIL_HOST_USER,[data.email],fail_silently=True)
                         return redirect("home")
                    else:
                        messages.error(request,"insuffuisient funds")
                else:
                    messages.error(request,"bichagadu")
            else:
                messages.error(request,"incorrect pin ")
    context={
        'flag':True
    }
    return render(request,"transaction.html")


def acc_transfer(request):
    f_data=None
    t_data = None
    if request.method == "POST":
        f_acc = request.POST.get('f_acc')
        t_acc = request.POST.get('t_acc')
        pin = request.POST.get('pin')
        amt = int(request.POST.get('amt'))
        try:
            f_data = Accounts.objects.get(acc_number = f_acc)
        except :
            messages.error(request,"sender account number is invlaid")
        try:
            t_data = Accounts.objects.get(acc_number = t_acc)
        except:
            messages.error(request,"Receiver Account is invalid")
        if f_data:
            if int(f_data.get_pin())== int(pin):
                bal = f_data.balance
                if amt>=1:
                    if amt<=bal:
                        f_data.balance = bal-amt
                        f_data.save()
                        send_mail("AMOUNT DEBITED",f"amount {amt} has been debited from ur account {f_data.acc_number} via Account transfer  ur current available balance is {f_data.balance}",settings.EMAIL_HOST_USER,[f_data.email],fail_silently=True)
                        if t_data:
                            t_data.balance = amt+t_data.balance
                            t_data.save()
                            send_mail("AMOUNT CREDITED",f"amount {amt} has been credited to ur account {t_data.acc_number} via ATM  ur current available balance is {t_data.balance}",settings.EMAIL_HOST_USER,[t_data.email],fail_silently=True)
                            return redirect("home")
                else:
                    messages.error(request,"kanisam 1 rs leka potey why ...")
    return render(request,'acc_tran.html')

       


    