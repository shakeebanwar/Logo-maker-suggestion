from django.shortcuts import render,HttpResponse,redirect
from .models import category,product,logoinfo,client
from django.db.models import Q
# Create your views here.
def index(request):
    if request.method=="POST":
        logoname=request.POST['logoname']
        cat=request.POST['cat']
        company=request.POST['companyname']
        price=request.POST['price']
        data=product(logoname=logoname,category=category.objects.get(cname=cat),price=price,companyname=company)
        data.save()
        request.session['category'] = cat
       
   
        f=logoinfo.objects.filter(category__cname=cat)
       
     
        #return HttpResponse(f)
        return render(request,'listing-grid.html',{'data':f})
      
    

    
    
    data=category.objects.all()
    return render(request,'index-2.html',{'data':data})
    

def listing(request):
    return render(request,'listing-grid.html')


def search(request):
    #category=request.session['category']
    search=request.POST['search']
    data=logoinfo.objects.filter(title__contains=search)
   
    return render(request,'listing-grid.html',{'data':data})
      
    

# data=Student.objects.filter(Q(fname__contains=search) |Q(age__contains=search) | Q(lname__contains=search) )
def detail(request,id):


    
    data=logoinfo.objects.filter(sno=id)
    return render(request,'listing-detail.html',{'data':data})


def data(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        number=request.POST['number']
        message=request.POST['message']
        logoid=logoinfo.objects.get(sno=request.POST['logoid'])
        data=client(name=name,email=email,contact=number,message=message,logoid=logoid)
        data.save()
        if data:
            return redirect('https://logodesigning.org/')
    return HttpResponse('404')

