from django.shortcuts import render,redirect
from datetime import datetime,date
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def displayRooms(request):
    rooms=Rooms.objects.all()
    return render(request,'roomsPage.html',{'rooms':rooms})

def searchRooms(request):
    return render(request,'searchRooms.html')

def showAvailableRooms(request):
    if request.method=='POST':
        check_in_raw=request.POST['check_in']
        check_out_raw=request.POST['check_out']
        check_in=check_in_raw.split('-')
        check_out=check_out_raw.split('-')
        check_in=date(int(check_in[0]),int(check_in[1]),int(check_in[2]))
        check_out=date(int(check_out[0]),int(check_out[1]),int(check_out[2]))
        today=date.today()
        delta1=check_in-today
        delta2=check_out-check_in
        print(delta1,'asdfaefae')
        if delta2.days==0:
            messages.error(request,'choose next day as check out day')
            return render(request,'searchRooms.html')
        if delta1.days < 0:
            messages.error(request,'you choosed earlier check-in date')
            return render(request,'searchRooms.html')
        if delta2.days < 0:
            messages.error(request,'invalid dates')
            return render(request,'searchRooms.html')
        bookedRooms = Reservations.objects.filter(
                    check_in_date__lt=check_out,
                    check_out_date__gt=check_in
                ).values('room_id')
        available_rooms=Rooms.objects.exclude(room_number__in=bookedRooms)
        return render(request,'searchRooms.html',{'rooms':available_rooms,'check_in':check_in_raw,'check_out':check_out_raw})
    else:
        return render(request,'searchRooms.html')

def reserve(request,pk):
    number=int(pk)
    room=Rooms.objects.get(room_number=number)
    if request.method=='POST':
        check_in_raw=request.POST['check_in_date']
        check_out_raw=request.POST['check_out_date']
        check_in=check_in_raw.split('-')
        check_out=check_out_raw.split('-')
        check_in=date(int(check_in[0]),int(check_in[1]),int(check_in[2]))
        check_out=date(int(check_out[0]),int(check_out[1]),int(check_out[2]))
        today=date.today()
        delta1=check_in-today
        delta2=check_out-check_in
        print(delta1,'asdfaefae')
        if delta2.days==0:
            messages.error(request,'choose next day as check out day')
            return redirect('reserve',pk=pk)
        if delta1.days < 0:
            messages.error(request,'you choosed earlier check-in date')
            return redirect('reserve',pk=pk)
        if delta2.days < 0:
            messages.error(request,'invalid dates')
            return redirect('reserve',pk=pk)
        cst=customer(name=request.POST['name'],contact_no=request.POST['contact_no'],address=request.POST['address'],)
        cst.save()
        reservations=Reservations(reserved_for=cst,room=room,check_in_date=check_in,check_out_date=check_out)
        reservations.save()
        messages.success(request,f'room successfully reserved with id {reservations.id}')
        return redirect('search')
    return render(request,'reservations.html',{'room':room})

@login_required(login_url='signIn')
def upcomingReservations(request):
    reservations=Reservations.objects.filter(check_in_date__gte=datetime.now().date()).order_by('check_in_date')
    return render(request,'showCheckins.html',{"reservations":reservations})

def viewRoom(request,pk):
    room=Rooms.objects.get(room_number=pk)
    features=Room_features.objects.filter(room_type=room.room_type).last()
    room_images=Room_images.objects.filter(room_type=room.room_type)
    return render(request,'viewRoom.html',{'room':room,'features':features,'images':room_images})

def viewHome(request):
    return render(request,'homePage.html')

@login_required(login_url='signIn')
def employeePage(request):
    return render(request,'employeePage.html')
@login_required(login_url='signIn')
def recordPayment(request,pk):
    reservation=Reservations.objects.get(id=pk)
    if request.method=='POST':
        payment_mode=request.POST['payment_mode']
        payment_status=request.POST['payment_status']
        pymnt=Payments.objects.filter(reservation=reservation).first()
        if pymnt:
            pymnt.payment_mode=payment_mode
            pymnt.payment_status=payment_status
            pymnt.save()
        else:
            Payments.objects.create(reservation=reservation,payment_mode=payment_mode,payment_status=payment_status,amount=reservation.room.price)
        if payment_status=='completed': 
            reservation.payment_status=True
        else:
            reservation.payment_status=False
        reservation.save()
        return redirect('check-ins')
    return render(request,'paymentRecordPage.html',{'reservation':reservation})

@login_required(login_url='signIn')
def addRoom(request):
    room_types=Room_type.objects.all()
    if request.method=='POST':
        typeofRoom=request.POST['room_type']
        num=request.POST['room_number']
        room_type=Room_type.objects.get(id=typeofRoom)
        price=room_type.price
        # Rooms.objects.create(room_number=num,room_type=room_type,price=price)
        try:
            Rooms.objects.create(room_number=num,room_type=room_type,price=price)
        except:
            messages.error(request,'a room with same room number exists')
            return render(request,'addRoom.html',{'room_types':room_types})
        messages.info(request,f'room no {num} added successfully')
        return redirect('employee')
    return render(request,'addRoom.html',{'room_types':room_types})

@login_required(login_url='signIn')
def addRoomType(request):
    taxes=Tax_rate.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        price=request.POST['price']
        area=request.POST['area']
        tax=request.POST['tax']
        tax=Tax_rate.objects.get(id=tax)
        rt= Room_type(type=name,tax_name=tax,area=area,price=price)
        rt.save()
        Room_pricing.objects.create(room_type=rt,price=price)
        messages.info(request,f'room type :{name} added successfully')
        return redirect('employee')
    return render(request,'addRoomType.html',{'taxes':taxes})

@login_required(login_url='signIn')
def addRoomImage(request):
    room_types=Room_type.objects.all()
    if request.method=='POST':
        room_type_id=request.POST['room_type_id']
        room_type=Room_type.objects.get(id=room_type_id)
        img=request.FILES['image']
        Room_images.objects.create(room_type=room_type,image=img)
        messages.info(request,f'room image added succesfully')
        return redirect('employee')
    return render(request,'addRoomImage.html',{'rooms':room_types})

@login_required(login_url='signIn')
def addRoomFeature(request):
    rooms=Room_features.objects.all().values('room_type')
    print(rooms)
    room_types=Room_type.objects.exclude(id__in=rooms)
    if request.method=='POST':
        id=room_number=request.POST['room_type']
        features=request.POST['features']
        room_type=Room_type.objects.get(id=id)
        Room_features.objects.create(room_type=room_type,feature=features,standard='high')
        messages.info(request,f'room features added succesfully')
        return redirect('employee')
    return render(request,'addRoomFeatures.html',{'room_types':room_types})

def viewAllRooms(request):
    rooms=Rooms.objects.all()

    return render(request,'viewAllRooms.html',{'rooms':rooms})

def customerPage(request):
    return render(request,'customerPage.html')

def hotelRatingRecord(request):
    if request.method=='POST':
        cst=customer(name=request.POST['name'],contact_no=request.POST['contact_no'],address=request.POST['address'],)
        cst.save()
        Customer_Rating.objects.create(customer=cst,rating=request.POST['rating'])
        messages.success(request,f'rating successfully recorded')
        return redirect('customer')
    return render(request,'hotelRating.html')

def recordRoomReview(request):
    rooms=Rooms.objects.all()
    if request.method=='POST':
        cst=customer(name=request.POST['name'],contact_no=request.POST['contact_no'],address=request.POST['address'],)
        cst.save()
        room=Rooms.objects.get(room_number=request.POST['room'])
        Room_reviews.objects.create(customer=cst,room=room,review=request.POST['review'])
        messages.success(request,f'review recorded successfully')
        return redirect('customer')
    return render(request,'roomReviewPage.html',{'rooms':rooms})

def showReviews(request,pk):
    room=Rooms.objects.get(room_number=pk)
    reviews=Room_reviews.objects.filter(room=room)
    return render(request,'allRoomReviews.html',{'reviews':reviews,'room':room})

def signUp(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['confirmPassword']
        role=request.POST['role']
        name=request.POST['name']
        contact_no=request.POST['contact_no']
        user=Employees(username=username,contact_no=contact_no,role=role,name=name)
        user.set_password(password)
        user.save()
        messages.info(request,'account created succesfully')
        return redirect('signIn')
    return render(request,'signUp.html')

def signIn(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            messages.info(request,'successfully logged in')
            return redirect('employee')
        else:
            messages.info(request,'invalid credentials')
    return render(request,'signIn.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def allHotelRatings(request):
    ratings=Customer_Rating.objects.all()
    return render(request,'seeHotelRatings.html',{'ratings':ratings})

def UpdateRoomPricing(request):
    room_types=Room_type.objects.all()
    if request.method=='POST':
        newPrice=int(request.POST['price'])
        room_type_id=request.POST['room_type']
        room_type=Room_type.objects.get(id=room_type_id)
        room_type.price=newPrice+newPrice*(room_type.tax_name.tax_percent/100)
        room_type.save()
        roomP=Room_pricing.objects.get(room_type=room_type)
        roomP.price=newPrice
        roomP.save()
        messages.info(request,'room Pricing updated succesfully')
        return redirect('employee')
    return render(request,'updateRoomPricing.html',{'room_types':room_types})

def newTax(request):
    if request.method=='POST':
        name=request.POST['name']
        percent=request.POST['percent']
        Tax_rate.objects.create(tax_name=name,tax_percent=percent)
        messages.info(request,'new Tax added')
        return redirect('employee')
    return render(request,'addNewTax.html')