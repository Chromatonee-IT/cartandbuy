from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Sum
from .models import *
import sqlite3
import datetime
from vendor.utils import *
from vendor.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Prefetch
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . serializer import *
from store.populate_data import data_fetch
from django.db.models.functions import Lower



def home(request):
    try:
        home_offer = home_offers.objects.all()
        cur_user  = request.user if request.user.is_authenticated else None
        categories = category.objects.all()
        subcategories = subcategory.objects.all()
        product_list = products.objects.prefetch_related('product_images','itmclass')
        size_list = product_sizes.objects.all()
        new_arrival = product_list.order_by('-itm_datecreated')

        if cur_user:
            cart_ins = Cart.objects.get(user=request.user)
            cart_items = cartItems.objects.filter(cart_ins=cart_ins)
            cart_total = 0
            for data in cart_items:
                cart_total += data.product.itm_new_price*data.cart_count
        else:
            cart_items =[]
            cart_total = 0.00

        # for product in product_list:
        #     if reviews.objects.filter(product_id = product.pk):
        #         review_stats = reviews.objects.filter(product_id = product.pk).aggregate(
        #             average_rating=Avg('rating')
        #         )
        #         average_rating = review_stats['average_rating']
        #     else:
        #         average_rating = '0.0'
        #     product.average_rating = average_rating
        #     if reviews.objects.filter(product_id = product.pk):
        #         review_stats = reviews.objects.filter(product_id = product.pk).aggregate(
        #             total_reviews=Count('id')
        #         )
        #         total_reviews = review_stats['total_reviews']
        #     else:
        #         total_reviews = '0'

        #     product.total_review = total_reviews
        #     product.save()
        
        # if request.user:
        #     recently_viewed = request.session['product_sets']
        # else:
        #     recently_viewed=[]
        context = {'cur_user':cur_user,'categories':categories,'subcategories':subcategories,'home_offers':home_offer,'product_list':product_list,'new_arrival':new_arrival,'size_list':size_list,'cart_items':cart_items,'cart_total':cart_total}
        return render(request,'store/home1.html',context)

    except Exception as e:
        print(e)
        return redirect('home')

@api_view(['GET'])
def search_product(request,search):
    product_list = products.objects.filter(itmname__icontains=search)
    serializer = ProductSerilizer(product_list,many=True)
    return Response(serializer.data)


def product_search(request,search):
    try:
        product_list = products.objects.filter(itmname__icontains=search)
        payload =[]
        for product in product_list:
            payload.append({
                'id': product.pk,
                'product': product.itmname,
                'category' : product.itmclass.classname,
            })
        return JsonResponse({
            'status': True,
            'data' : payload,
        })
    except Exception as e:
        return JsonResponse({
            'ststus': False,
            'error': e,
        })


def product_search_results(request,search_param):
    product_list = products.objects.filter(itmname__icontains=search_param)

    if category.objects.filter(classname__icontains=search_param):
        product_list = products.objects.filter(itmclass__classname__icontains=search_param)
    elif midcategory.objects.filter(classname__icontains=search_param):
        print("midcategory",search_param)
    elif subcategory.objects.filter(classname__icontains=search_param):
        print("subcategory",search_param)

    

    
    price_filter = request.GET.get('price',"")
    if price_filter != "":
        filter_min_price = price_filter.split("-")[0]
        filter_max_price = price_filter.split("-")[1]
    else:
        filter_min_price = 0
        filter_max_price = 0
    if price_filter == "0-500":
        product_list = product_list.filter(itm_new_price__lte=500)
    elif price_filter == "500-1000":
        product_list = product_list.filter(itm_new_price__range=(500,1000))
    elif price_filter == "1000-3000":
        product_list = product_list.filter(itm_new_price__range=(1000,3000))
    elif price_filter == "3000-5000":
        product_list = product_list.filter(itm_new_price__range=(3000,5000))
    elif price_filter == "5000+":
        product_list = product_list.filter(itm_new_price__gte=5000)
    elif price_filter != "":
        product_list = product_list.filter(itm_new_price__range=(filter_min_price,filter_max_price))



    ordering = request.GET.get('ordering',"")
    if ordering == "popularity":
        product_list = product_list.order_by("-total_review")
    elif ordering == "average-rating":
        product_list = product_list.order_by("-average_rating")
    elif ordering == "latest":
        product_list = product_list.order_by("-itm_datecreated")
    elif ordering == "low-to-high":
        product_list = product_list.order_by("itm_new_price")
    elif ordering == "high-to-low":
        product_list = product_list.order_by("-itm_new_price")






    context = {'search_result':product_list,'cur_ordering':ordering,'search_param':search_param,'filter_min_price':filter_min_price,'filter_max_price':filter_max_price}
    return render(request,'store/search-products.html',context)

def all_products(request):
    try:
        all_product = products.objects.filter(itm_isactive=True).prefetch_related('product_images','itmclass')
        cur_user  = request.user if request.user.is_authenticated else None
        categories = category.objects.all()
        context = {'all_product':all_product,'categories':categories,'cur_user':cur_user}
        return render(request,'store/all_products.html',context)
    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def cart(request):
    try:
        cur_user  = request.user if request.user.is_authenticated else None
        cart_ins = Cart.objects.get(user = request.user, is_paid=False)
        cart_items = cartItems.objects.filter(cart_ins = cart_ins)

        cart_total = 0
        for data in cart_items:
            cart_total += data.product.itm_new_price*data.cart_count

        context = {'cur_user':cur_user,'cart_items':cart_items,'cart_total':cart_total}
        return render(request,'store/cart.html',context)
    except Exception as e:
        return redirect('cart')

# @csrf_exempt
# def populate_product(request,n):
#     try:
#         response = data_fetch(n)
#         for data in response:
#             payload = tuple(data.values())

#             id = payload[0]
#             name =payload[1]
#             title = payload[2]
#             description = payload[3]
#             category=payload[4]
#             old_price=payload[5]
#             new_price=payload[6]
#             status=payload[7]
#             images=payload[8]
#             rating=payload[9]
#             stock=payload[10]
#             brand=payload[11]

#             product = products.objects.create(itmname=name,itmtitle=title,itmdesc=description,itmclass=category,itm_price_old=old_price,itm_price_new=new_price,itm_isactive=status,average_rating=rating)
#             product_image = product_images.objects.create(product_id=product,image1=images[0],image2=images[1],image3=images[2],images4=images[3],images5=images[4])
#     except Exception as e:
#         return JsonResponse({
#         "status": False,
#         "Error": e
#     })
#     return JsonResponse({
#         "status": True
#     })

@login_required(login_url='login')
def checkout(request):
    context = {}
    return render(request,'store/checkout.html',context)


def all_stores(request):
    cur_user  = request.user if request.user.is_authenticated else None
    categories = category.objects.all()
    context = {'cur_user':cur_user,'categories':categories}
    return render(request,'store/all_stores.html',context)

@csrf_exempt
def login_user(request):
    try:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username, password=password)
            if_buyer = buyer.objects.filter(user=user).first()
            if if_buyer is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"Error Login!")
                return redirect('login')
    except Exception as e:
        print(e)
        messages.error(request,"Error Login!")
        return redirect('login')
    context = {}
    return render(request,'store/login.html',context)

@csrf_exempt
def login_user_popup(request):
    try:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username, password=password)
            if_buyer = buyer.objects.filter(user=user).first()
            if if_buyer is not None:
                login(request,user)
                return JsonResponse({
                    "status": True
                })
            else:
                return JsonResponse({
                    "status": False,
                    "error": "Error login!"
                })
    except Exception as e:
        return JsonResponse({
                    "status": False,
                    "error": str(e),
                })
    context = {}
    return render(request,'store/login.html',context)

@csrf_exempt
def register_user(request):
    try:

        if request.method == 'POST':
            terms_and_conditions = request.POST.get('termsandconditions', False)
            ref_code = request.GET.get('referal')
            username = request.POST['email']
            password = request.POST['password']
            name = request.POST['name']
            email = request.POST['email']
            phone_number = request.POST['phone']

            request.session['ref_code'] = ref_code
            request.session['username'] = username
            request.session['password'] = password
            request.session['name'] = name
            request.session['email'] = email
            request.session['phone_number'] = phone_number

            if username=="" or password=="" or name=="" or email=="" or  phone_number=="":
                messages.error(request, "Fill in all details!")
                return redirect('register')

            if terms_and_conditions == False:
                messages.info(request,"Kindly agree to the terms and conditions.")
                return redirect('register')

            if User.objects.filter(username=username).exists():
                print(User.objects.filter(username=username))
                messages.info(request,"Username already exists!")
                return redirect('register')
            if buyer.objects.filter(phone_number=phone_number).exists():
                messages.info(request,"Phone Number already exists!")
                return redirect('register')
            else:
                email_code = generate_unique_code()
                request.session['email_code'] = email_code
                subject = 'Please verify your email.'
                from_email = settings.EMAIL_HOST_USER
                to_email = [email]
                base_url = settings.BASE_URL
                html_content = render_to_string('email_verification.html', {'base_url':base_url,'email_code': email_code})
                email = EmailMultiAlternatives(subject, 'This is a plain text message.', from_email, to_email)
                email.attach_alternative(html_content, "text/html")
                email.send()
                return redirect('email_verification')

        context = {}
    except Exception:
        return redirect('register')
    return render(request,'store/register.html',context)

@csrf_exempt
def email_verify(request):
    try:
        user_otp = request.POST.get('user_otp')
        ref_code = request.session.get('ref_code')
        username = request.session.get('username')
        password = request.session.get('password')
        name = request.session.get('name')
        email = request.session.get('email')
        phone_number = request.session.get('phone_number')
        email_code = request.session.get('email_code')
        if request.POST:

            user_otp = request.POST.get('user_otp')
            ref_code = request.session.get('ref_code')
            username = request.session.get('username')
            password = request.session.get('password')
            name = request.session.get('name')
            email = request.session.get('email')
            phone_number = request.session.get('phone_number')
            email_code = request.session.get('email_code')
            if email_code=="":
                messages.error(request,"Register to get OTP.")
                return redirect('register')
            if user_otp == email_code:
                if buyer.objects.filter(code = ref_code).exists():
                    user = User.objects.create_user(username=username, password=password)
                    user.first_name = name
                    user.email = email
                    user.save()
                    buyer_ins = buyer.objects.get(code = ref_code)
                    buyer.objects.create(user=user, name = name, email=email, phone_number=phone_number, referred_by_user=buyer_ins.user)
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.first_name = name
                    user.email = email
                    user.save()
                    buyer.objects.create(user=user, name = name, email=email, phone_number=phone_number)
                user = authenticate(username=username, password=password)
                login(request, user)

                del request.session['ref_code']
                del request.session['username']
                del request.session['password']
                del request.session['name']
                del request.session['email']
                del request.session['phone_number']
                del request.session['email_code']

                return redirect('home')
            else:
                messages.error(request,"Incorrect OTP.")
                return redirect('email_verification')
    except Exception:
        messages.error(request,"Error submitting OTP.")
        return redirect('email_verification')
    context = {}
    return render(request,'store/otp_verification.html',context)


def resend_otp_email(request):
    email_id = request.session.get('email')
    email_code=request.session.get('email_code')
    subject = 'Please verify your email.'
    from_email = settings.EMAIL_HOST_USER
    to_email = [email_id]
    base_url = settings.BASE_URL
    html_content = render_to_string('email_verification.html', {'base_url':base_url,'email_code': email_code})
    email = EmailMultiAlternatives(subject, 'This is a plain text message.', from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()
    messages.success(request,"OTP sent. Please check your inbox.")
    return redirect('email_verification')

def otp_verification_forgotpass(requests):
    return render(requests,"store/email_otp_verify.html")


def forgotpass(request):
    if request.method=="POST":
        email = request.POST.get('email')
        now =datetime.datetime.now()
        expiry_get_str = request.session['expiry_otp']
        expiry_get = datetime.datetime.fromisoformat(expiry_get_str)

        if now < expiry_get:
            email_code = request.session.get('email_code')
            subject = 'Please verify your email.'
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            base_url = settings.BASE_URL
            html_content = render_to_string('email_verification.html', {'base_url':base_url,'email_code': email_code})
            email = EmailMultiAlternatives(subject, 'This is a plain text message.', from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send()
            return redirect('otp-verification')
        else:
            email_code = generate_unique_code()
            request.session['email_code'] = email_code
            expiry_date = generate_expiry(request)
            request.session['expiry_otp'] = expiry_date
            subject = 'Please verify your email.'
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            base_url = settings.BASE_URL
            html_content = render_to_string('email_verification.html', {'base_url':base_url,'email_code': email_code})
            email = EmailMultiAlternatives(subject, 'This is a plain text message.', from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send()
            return redirect('otp-verification')
    context = {}
    return render(request,'store/forgotpassword.html',context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request,'Logout successful.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def dashboard(request):
    try:
        customer_instance = get_object_or_404(buyer,user=request.user)
        if request.method == 'POST':
            customer_instance.name = request.POST['name']
            customer_instance.email = request.POST['email']
            customer_instance.phone_number = request.POST['phone']
            if buyer.objects.filter(user=request.user).exists():
                customer_instance.save()
                buyer.success(request,'Profile Updated.')
                return redirect('dashboard')
            else:
                messages.info(request,"some error.")
                return redirect('dashboard')

        cur_user  = buyer.objects.filter(user=request.user)
        categories = category.objects.all()
        context = {'cur_user':cur_user,'categories':categories}
        return render(request,'store/account_details.html',context)
    except Exception as e:
        print(e)
        return redirect('dashboard')

@login_required(login_url='login')
def orders_user(request):
    try:
        cur_user  = buyer.objects.filter(user=request.user)
        order_list = orders.objects.filter(user=request.user)
        context = {'cur_user':cur_user,'order_list':order_list}
        return render(request,'store/orders.html',context)
    except Exception as e:
        return redirect('oders')

@login_required(login_url='login')
def order_tracking(request):
    try:
        cur_user  = buyer.objects.filter(user=request.user)
        context = {'cur_user':cur_user}
        return render(request,'store/order_tracking.html',context)
    except Exception:
        return redirect('order_tracking')

@login_required(login_url='login')
def referal(request):
    cur_user  = buyer.objects.filter(user=request.user).first()
    all_referals = buyer.objects.filter(referred_by_user = request.user)
    context={'cur_user':cur_user,'all_referals':all_referals}
    return render(request,'store/referal_page.html',context)


@login_required(login_url='login')
def address_user(request):
    try:
        addresses = address.objects.filter(username=request.user)
        active_address = address.objects.filter(isactive=True)
        cur_user=buyer.objects.filter(user=request.user)
        context = {'addresses':addresses,'active_address':active_address,'cur_user':cur_user}
        return render(request,'store/address.html',context)
    except Exception as e:
        return redirect('address')
    

@login_required(login_url="login")
def address_user_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        addln1 = request.POST['adrline1']
        addln2 = request.POST['adrline2']
        addln3 = request.POST['adrline3']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        postal = request.POST['zip' ]
        if not address.objects.filter(username=request.user):
            address.objects.create(username=request.user,name=name,email=email,phone=phone,abline1=addln1,abline2=addln2,abline3=addln3,city=city,state=state,country=country,zip=postal,isactive=True)
            messages.success(request,"Address added successfully.")
            return redirect('address')
        elif address.objects.filter(name=name,zip=postal).exists():
            messages.error(request,"Address already exists!")
            return redirect('address')
        else:
            address.objects.create(username=request.user,name=name,email=email,phone=phone,abline1=addln1,abline2=addln2,abline3=addln3,city=city,state=state,country=country,zip=postal)
            messages.success(request,"Address added successfully.")
            return redirect('address')
    return render(request,'store/address-add.html')


@login_required(login_url="login")
def address_user_edit(request,id):
    if request.method == "POST":
        id=id
        name = request.POST['name_edit']
        phone = request.POST['phone_edit']
        email = request.POST['email_edit']
        addln1 = request.POST['adrline1_edit']
        addln2 = request.POST['adrline2_edit']
        addln3 = request.POST['adrline3_edit']
        city = request.POST['city_edit']
        state = request.POST['state_edit']
        country = request.POST['country_edit']
        postal = request.POST['zip_edit']
        default_address = request.POST.get('default_address',False)
        if address.objects.filter(id=id).exists():
            address.objects.filter(id=id).update(username=request.user,name=name,email=email,phone=phone,abline1=addln1,abline2=addln2,abline3=addln3,city=city,state=state,country=country,zip=postal)
            if default_address:
                prev_address = address.objects.filter(username=request.user,isactive=True).first()
                prev_address.isactive = False
                prev_address.save()
                cur_address = address.objects.filter(id=id).first()
                cur_address.isactive = True
                cur_address.save()
            messages.success(request,'Address Updated')
            return redirect('address')
        else:
            messages.error(request,'Error updating address')
            return redirect('address')
        
    cur_address = address.objects.filter(id=id,username=request.user).first()
    context = {'cur_address':cur_address}
    return render(request,'store/address-edit.html',context)


@login_required(login_url='login')
def payment_method(request):
    if 'card_add' in request.POST:
        card_name = request.POST['name']
        card_number = request.POST['number']
        card_expiry = request.POST['expiry']
        card_cvv = request.POST['cvv']
        print(card_name)
        print(card_number)
        print(card_expiry)
        print(card_cvv)
    context = {}
    return render(request,'store/payment_method.html',context)

@login_required(login_url='login')
def my_reviews(request):
    try:
        my_reviews = reviews.objects.filter(username=request.user).first()
        context = {'my_reviews':my_reviews}
        return redirect('dashboard')
        # return render(request,'store/my_reviews.html',context)
    except Exception as e:
        return redirect('dashboard')
        # return redirect('my_reviews')

@login_required(login_url='login')
def my_favourites(request):
    try:
        cur_user  = request.user if request.user.is_authenticated else None
        favourite_ins = favourite.objects.filter(user=request.user).first()
        Products = favourite_items.objects.filter(favourite_ins=favourite_ins)
        context = {'cur_user':cur_user,'products':Products}
        return render(request,'store/my_favourites.html',context)
    except Exception as e:
        return redirect('my_favourites')

def product_single(request,id):
    try:
        if request.method == 'POST':
            rating = request.POST.get('rating')
            review = request.POST.get('review')
            if not reviews.objects.filter(username = request.user,product_id = id):
                reviews.objects.create(username = request.user,product_id = id,rating = rating, review = review)
                messages.success(request,'Review submitted.')
                return redirect('product_single',id=id)
            else:
                messages.error(request,'Already reviewed this product.')
                return redirect('all_products')
        single_product = products.objects.filter(id=id).first()
        product_ins = single_product
        size_ins = product_sizes.objects.filter(product=product_ins)
        all_reviews = reviews.objects.filter(product = id)
        discount_coupon = discount.objects.filter(if_on_product=product_ins)

        if reviews.objects.filter(product_id = id).exists():
            reviews_ins =  reviews.objects.filter(product_id = id)
            one_star_rating_count = 0
            two_star_rating_count = 0
            three_star_rating_count = 0
            four_star_rating_count = 0
            five_star_rating_count = 0

            for review in reviews_ins:
                if review.rating == 1:
                    one_star_rating_count += 1
                elif review.rating == 2:
                    two_star_rating_count += 1
                elif review.rating == 3:
                    three_star_rating_count += 1
                elif review.rating == 4:
                    four_star_rating_count += 1
                elif review.rating == 5:
                    five_star_rating_count += 1
            one_star_rating_percentage = ((one_star_rating_count/single_product.total_review)*100)
            two_star_rating_percentage = ((two_star_rating_count/single_product.total_review)*100)
            three_star_rating_percentage = ((three_star_rating_count/single_product.total_review)*100)
            four_star_rating_percentage = ((four_star_rating_count/single_product.total_review)*100)
            five_star_rating_percentage = ((five_star_rating_count/single_product.total_review)*100)
        else:
            one_star_rating_percentage = 0
            two_star_rating_percentage = 0
            three_star_rating_percentage = 0
            four_star_rating_percentage = 0
            five_star_rating_percentage = 0

        cur_user  = request.user if request.user.is_authenticated else None
        categories = category.objects.all()
        store_info = store_details.objects.filter(store_vendor = product_ins.vendoraddedby.user).first()
        vendor_products = products.objects.filter(vendoraddedby=product_ins.vendoraddedby)[:3]
        context = {'cur_user':cur_user,'product':single_product,'reviews':all_reviews,'categories':categories,'discount_coupon':discount_coupon,'store_info':store_info,'size_ins':size_ins,'vendor_products':vendor_products,'one_star_rating_percentage':f'{one_star_rating_percentage:.0f}', 'two_star_rating_percentage':f'{two_star_rating_percentage:.0f}', 'three_star_rating_percentage':f'{three_star_rating_percentage:.0f}', 'four_star_rating_percentage':f'{four_star_rating_percentage:.0f}', 'five_star_rating_percentage':f'{five_star_rating_percentage:.0f}'}

        return render(request,'store/single-product.html',context)
    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def all_category(request):
    all_product = products.objects.filter(itm_isactive=True).prefetch_related('product_images','itmclass')
    ordering = request.GET.get('ordering',"")
    if ordering == "popularity":
        all_product = all_product.order_by("-total_review")
    elif ordering == "average-rating":
        all_product = all_product.order_by("-average_rating")
    elif ordering == "latest":
        all_product = all_product.order_by("-itm_datecreated")
    elif ordering == "low-to-high":
        all_product = all_product.order_by("itm_new_price")
    elif ordering == "high-to-low":
        all_product = all_product.order_by("-itm_new_price")

    cur_user  = request.user if request.user.is_authenticated else None
    all_cat = category.objects.prefetch_related('sub_category').all()
    context = {'cur_user':cur_user,'all_cat':all_cat,'products':all_product,'cur_ordering':ordering}
    return render(request,'store/all-category.html',context)

def category_detail(request,category_name):
    new_arrival = products.objects.filter(itmclass__classname = category_name).prefetch_related('product_images','itmclass').order_by('-itm_datecreated')
    ordering = request.GET.get('ordering',"")
    if ordering == "popularity":
        new_arrival = new_arrival.order_by("-total_review")
    elif ordering == "average-rating":
        new_arrival = new_arrival.order_by("-average_rating")
    elif ordering == "latest":
        new_arrival = new_arrival.order_by("-itm_datecreated")
    elif ordering == "low-to-high":
        new_arrival = new_arrival.order_by("itm_new_price")
    elif ordering == "high-to-low":
        new_arrival = new_arrival.order_by("-itm_new_price")

    
    cur_user  = request.user if request.user.is_authenticated else None
    categories = category.objects.all()
    sub_categories = subcategory.objects.filter(itmclass__classname = category_name)
    for sub_category in sub_categories:
        print(sub_category.classname,sub_category.get_product_total)
    context = {'cur_user':cur_user,'categories':categories,'new_arrival':new_arrival,'cur_category':category_name,'sub_categories':sub_categories,'cur_ordering':ordering}
    if category.objects.filter(classname = category_name):
        return render(request,'store/single-category.html',context)
    else:
        return redirect('/all_category/')

def subcategory_detail(request,category_name,midcategory_name):
    new_arrival = products.objects.filter(itmmidclass__classname=category_name).order_by('-itm_datecreated')
    cur_user  = request.user if request.user.is_authenticated else None
    categories = category.objects.all()
    sub_categories = subcategory.objects.filter(itmmidclass__classname = midcategory_name)
    context = {'cur_user':cur_user,'categories':categories,'new_arrival':new_arrival,'cur_category':midcategory_name,'sub_categories':sub_categories}
    return render(request,'store/single-midcategory.html',context)


@login_required(login_url='login')
def add_to_cart(request,id):
    try:
        count = request.GET.get('quantity','')
        if count != '':
            quantity = int(count)
        else:
            quantity = 1
        color_variant = request.GET.get('color','none')
        size_variant = request.GET.get('size','none')
        product = products.objects.filter(id=id).first()
        user = request.user
        cart, _ = Cart.objects.get_or_create(user = user, is_paid = False)

        if product_variants.objects.filter(product_id = product,varient_name = color_variant).exists():
            color_variant_ins = product_variants.objects.get(product_id = product,varient_name = color_variant).pk
        else:
            color_variant_ins = None

        if product_sizes.objects.filter(id=size_variant).exists():
            size_variant_ins = size_variant
        else:
            size_variant = None

        print(size_variant)

        if product_variants.objects.filter(product_id=product).exists() and not color_variant:
            messages.error(request,"Please select a color.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        elif product_sizes.objects.filter(product=product).exists() and not color_variant:
            messages.error(request,"Please select a size.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        cart_item_exists = cartItems.objects.filter(cart_ins = cart, product = product,variant_id = color_variant_ins,size = size_variant_ins).first()

        if cart_item_exists:
            cart_item_exists.cart_count += quantity
            cart_item_exists.save()
        else:
            cart_items = cartItems.objects.create(cart_ins = cart, product = product)
            if color_variant and product_variants.objects.filter(product_id=product).exists():
                color_variant_ins = product_variants.objects.get(product_id = product,varient_name = color_variant)
                cart_items.variant = color_variant_ins

            if size_variant and product_sizes.objects.filter(product=product,id=size_variant).exists():
                size_variant_ins = product_sizes.objects.get(product=product,id = size_variant)
                cart_items.size = size_variant_ins

            cart_items.cart_count = quantity
            cart_items.save()
        messages.success(request,"Added to cart")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@login_required(login_url='login')
def add_to_cart_api(request,id):
    color_variant = request.GET.get('color','')
    product = products.objects.filter(id=id).first()
    product_variant_ins = product_variants.objects.filter(product_id=product).exists()
    user = request.user
    cart, _ = Cart.objects.get_or_create(user = user, is_paid = False)
    if product_variant_ins and not color_variant:
        return JsonResponse({
            'status': False,
            'message': 'Please select a color.'
        })
    elif product_sizes.objects.filter(product=product).exists() and not color_variant:
        return JsonResponse({
            'status': False,
            'message': 'Please select a size.'
        })
    if color_variant != "":
            cart_items = cartItems.objects.create(cart_ins = cart, product = product,)
            color_variant_ins = product_variants.objects.get(varient_name = color_variant)
            cart_items.variant = color_variant_ins
            cart_items.save()

    return JsonResponse({
            'status': True,
            'message': 'Added to cart.'
        })

@login_required(login_url='login')
def remove_from_cart(request,id):
    try:
        cart_item = cartItems.objects.filter(id=id).first()
        cart_item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='login')
def clear_cart(request):
    try:
        user = request.user
        cart = Cart.objects.filter(user = user, is_paid = False).first()
        cart_items= cartItems.objects.filter(cart_ins = cart)
        cart_items.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@login_required(login_url="/login/")
def increase_cart_count(request,id):
    user = request.user
    cart = Cart.objects.filter(user = user, is_paid = False).first()
    cart_items= cartItems.objects.get(id = id)
    cart_items.cart_count += 1
    cart_items.save()
    return JsonResponse({
        'status':True,
        'message': cart_items.cart_count
    })

@login_required(login_url="/login/")
def decrease_cart_count(request,id):
    user = request.user
    cart = Cart.objects.filter(user = user, is_paid = False).first()
    cart_items= cartItems.objects.get(id = id)
    cart_items.cart_count -= 1
    cart_items.save()
    return JsonResponse({
        'status':True,
        'message': cart_items.cart_count
    })




@login_required(login_url='login')
def add_to_favourite(request,id):
    try:
        product = products.objects.filter(id=id).first()
        user = request.user
        favourites, _ = favourite.objects.get_or_create(user = user)
        if not favourite_items.objects.filter(favourite_ins = favourites, product = product).exists():
            favourites_item = favourite_items.objects.create(favourite_ins = favourites, product = product,)
        return JsonResponse({
            'status': True
        })
    except Exception as e:
        return JsonResponse({
            'status': False,
            'error': str(e)
        })

@login_required(login_url='login')
def remove_from_favourite(request,id):
    try:

        favourites_item = favourite_items.objects.filter(favourite_ins= favourite.objects.get(user=request.user),product__id=id).first()
        favourites_item.delete()
        return JsonResponse({
            'status': True,
            'product': str(favourites_item.product)[:-1],
        })
    except Exception as e:
        return JsonResponse({
            'status': False,
            'error': str(e)
        })


def add_browsing_data(request,id):
    if 'product_sets' in request.session:
       products = request.session['product_sets']
    else:
       products =[]
    if id in products:
        pass
    else:
        products.append(id)
    request.session['product_sets'] = products
    return JsonResponse({
        'status': True,
        'data': request.session['product_sets'],
    })


