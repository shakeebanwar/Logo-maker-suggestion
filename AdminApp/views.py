from django.shortcuts import render,HttpResponse,redirect
from logomaker.models import client,category,users,logoinfo,SerClient,SerCategory
from django.contrib.sessions.models import Session 
from passlib.hash import pbkdf2_sha256
import json

# Create your views here.
def index(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    orders=client.objects.all().count()
    logos=logoinfo.objects.all().count()
    catedata=category.objects.all().count()
    userdata=client.objects.all().order_by('-id')
    data={
        'userdata':userdata,
        'order':orders,
        'logos':logos,
        'catedata':catedata
    }
    return render(request,'dashboard/home.html',data)

def orders(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    userdata=client.objects.all().order_by('-id')
    data={
        'userdata':userdata
    }
    return render(request,'dashboard/orders.html',data)

# logos
def logos(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    if request.method =="POST":
        title= request.POST['title']
        cate=category.objects.get(cid=request.POST['category'])
        image= request.FILES['image']
        addlogo=logoinfo(title=title,category=cate,img=image)
        addlogo.save()
        return redirect('logos')
    datas=logoinfo.objects.all().order_by('-sno')
    cat=category.objects.all()
    data={
        'data':datas,
        'category':cat
        }
    return render(request,'dashboard/logos.html',data)


def logoupdate(request,id):
    if not request.session.has_key('userid'):
        return redirect('login')
    userdata=logoinfo.objects.get(sno=id)
    ucat=category.objects.all()
    data={
        'data':userdata,
        'category':ucat
        }
    return render(request,'dashboard/updatelogos.html',data)

# update logo data
def updatelogodata(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    if request.method =="POST":
        id= request.POST['uid']
        title= request.POST['title']
        cate=category.objects.get(cid=request.POST['category'])
        image= request.FILES['image']
        data= logoinfo.objects.get(sno=id)
        data.title=title
        data.category=cate
        data.img =image
        data.save()
        return redirect('logos')
        
    
# Delete Logos
def deletelogo(request,id):
    if not request.session.has_key('userid'):
        return redirect('login')
    deletelogo=logoinfo.objects.get(sno=id)
    deletelogo.delete()
    return redirect('logos')

# category 
def categoryview(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    return render(request,'dashboard/category.html')
# 
def categorydata(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    catdata= category.objects.all().order_by('-cid')
    alldata=SerCategory(catdata, many=True)
    return HttpResponse(json.dumps(alldata.data))


# category update data
def categoryupdatedata(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    if request.method =='GET':
        mydata=list()
        uid=request.GET['id']
        datas=category.objects.get(cid=uid)
        udata=SerCategory(datas)
        mydata.append(udata.data)
        return HttpResponse(json.dumps(mydata))
    elif request.method =='POST':
        uid=request.POST['uid']
        title=request.POST['utitle']
        data=category.objects.get(cid=uid)
        data.cname=title
        data.save()
        return HttpResponse("success")

def categoryinsert(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    if request.method=="POST":
        title=request.POST['title']
        datas=category(cname=title)
        datas.save()
        return HttpResponse('success')

# delete category
def delcategory(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    if request.method=="GET":
        id=request.GET['id']
        data=category.objects.get(cid=id)
        data.delete()
        return HttpResponse("success")

def orderviews(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    userdata=client.objects.all().order_by('-id')
    serdata= SerClient(userdata, many=True)
    return HttpResponse(json.dumps(serdata.data))

def notifications(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    userdata=client.objects.filter(mark_time=0)
    serdata= SerClient(userdata, many=True)
    return HttpResponse(json.dumps(serdata.data))


def accept(request, id):
    if not request.session.has_key('userid'):
        return redirect('login')
    data=client.objects.get(id=id)
    data.mark_time=1
    data.save()
    return redirect('/administrator')

# client message
def clientmessage(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    if request.method=="GET":
        msg = list()
        clientid=request.GET['id']
        msgdata=client.objects.get(id=clientid)
        mydata= SerClient(msgdata)
        msg.append(mydata.data)
        return HttpResponse(json.dumps(msg))

# settings
def settings(request):
    if not request.session.has_key('userid'):
        return redirect('login')

    if request.method=="POST":
        name=request.POST['uname']
        email=request.POST['uemail']
        password=request.POST['upassword']
        hashpwd=pbkdf2_sha256.hash(password)
        user=users.objects.get(userid=1)
        user.fullname=name
        user.email=email
        user.password=hashpwd
        user.save()
        return redirect('settings')
    data=users.objects.get(userid=1)
    return render(request,'dashboard/settings.html',{'data':data})

# login 
def login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
       
        try:
             logindata=users.objects.get(email=email)
             if logindata:
                 
                if pbkdf2_sha256.verify(password,logindata.password):
                        request.session['userid']=logindata.userid
                        request.session['name']=logindata.fullname
                        return redirect('/administrator')
                else:
                    return redirect('login')
        except users.DoesNotExist:
            return redirect('login')

    return render(request,'dashboard/login.html')

# logout
def logout(request):
    if not request.session.has_key('userid'):
        return redirect('login')
    del request.session['userid']
    del request.session['name']
    return redirect('login')
