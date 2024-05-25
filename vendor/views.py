from django.shortcuts import render,redirect,HttpResponse
from store.models import *
from .models import *
from .utils import *
from .receivers import *
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Avg, Sum
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from django.http import JsonResponse
from datetime import date, datetime
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def home(request):
    return render(request,'home.html')

@csrf_exempt
def vendor_requirded(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

@csrf_exempt
def superuser_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)

@vendor_requirded(login_url='v_login')
def dashboard(request):
    try:
        # order_list = orders.objects.all()
        if products.objects.filter(vendoraddedby = request.user.customer.id):
            product = products.objects.filter(vendoraddedby = request.user.customer.id)
        else:
            product = []
        if orders.objects.filter(vendor_id = request.user.id).exists():
            order_list = orders.objects.filter(vendor_id = request.user.id)
        else:
            order_list =[]
    except Exception as e:
        print(e)

    context={'navbar':'dashboard','products':product,'order_list':order_list}
    return render(request,'dashboard.html',context)

@vendor_requirded(login_url='v_login')
def vendor_profile(request):
    user = request.user
    if LastLogin.objects.filter(user=user).exists():
        last_login = LastLogin.objects.filter(user=user).first()
    else:
        last_login = ""
    if address.objects.filter(isactive=True,username = user).exists():
        address_ins = address.objects.filter(isactive=True,username = user).first()
    else:
        address_ins = []
    if customer.objects.filter(user=user).exists():
        cust_ins = customer.objects.filter(user=user).first()
    else:
        cust_ins = []
    if store_details.objects.filter(store_vendor=user).exists():
        store_ins = store_details.objects.filter(store_vendor=user).first()
    else:
        store_ins = []
    if request.method=="POST":
        if 'profile_update' in request.POST:
            try:
                name= request.POST.get('name')
                birthday= request.POST.get('birthday')
                user_email= request.POST.get('user_email')
                user_phone= request.POST.get('user_phone')
                abline1= request.POST.get('adrline1')
                abline2= request.POST.get('adrline2')
                abline3= request.POST.get('adrline3')
                city= request.POST.get('city')
                district= request.POST.get('district')
                state= request.POST.get('state')
                postal= request.POST.get('postal')

                cust_ins.name = name
                cust_ins.email = user_email
                cust_ins.phone_number = user_phone
                cust_ins.birthday = birthday

                if 'profile_photo' in request.FILES:
                    cust_ins.cusstomer_image = request.FILES['profile_photo']
                cust_ins.save()

                if not address.objects.filter(username=request.user,isactive=True):
                    address.objects.create(username=request.user,name=name,email=user_email,phone=user_phone,abline1=abline1,abline2=abline2,abline3=abline3,city=city,state=state,zip=postal,isactive=True)
                    messages.success(request,"Address added successfully.")
                    return redirect('store_details')
                else :
                    address.objects.filter(username=request.user,isactive=True).update(username=request.user,name=name,email=user_email,phone=user_phone,abline1=abline1,abline2=abline2,abline3=abline3,city=city,state=state,zip=postal,isactive=True)
                    messages.success(request,"Address updated successfully!")
                    return redirect('store_details')
                # else:
                #     address.objects.create(username=request.user,name=name,email=user_email,phone=user_phone,abline1=abline1,abline2=abline2,abline3=abline3,city=city,state=state,zip=postal)

                return redirect('store_details')
            except Exception as e:
                messages.error(request,e)
                return redirect('store_details')

        if 'store_update' in request.POST:
            try:
                store_name= request.POST.get('store_name')
                store_email= request.POST.get('store_email')
                store_abline1= request.POST.get('store_abline1')
                store_abline2= request.POST.get('store_abline2')
                store_abline3= request.POST.get('store_abline3')
                city= request.POST.get('city')
                district= request.POST.get('district')
                # state= request.POST.get('state')
                zip= request.POST.get('zip')
                store_facebook= request.POST.get('store_facebook')
                store_instagram= request.POST.get('store_instagram')
                store_twitter= request.POST.get('store_twitter')
                if not store_details.objects.filter(store_vendor = request.user):
                    store_details.objects.create(store_vendor = request.user,store_name=store_name,store_email=store_email,abline1=store_abline1,abline2=store_abline2,abline3=store_abline3,city=city,district=district,store_facebook=store_facebook,store_instagram=store_instagram,store_twitter=store_twitter,zip=zip,store_logo = request.FILES['store_logo'])
                    messages.success(request,"Store created.")
                    return redirect('store_details')
                elif store_details.objects.filter(store_vendor = request.user).exists():
                    store_ins.store_name=store_name
                    store_ins.store_email=store_email
                    store_ins.abline1=store_abline1
                    store_ins.abline2=store_abline2
                    store_ins.abline3=store_abline3
                    store_ins.city=city
                    store_ins.district=district
                    # store_ins.state=state
                    store_ins.store_facebook=store_facebook
                    store_ins.store_instagram=store_instagram
                    store_ins.store_twitter=store_twitter
                    store_ins.zip=zip
                    if 'store_logo' in request.FILES:
                        store_ins.store_logo = request.FILES['store_logo']
                    store_ins.save()
                    messages.success(request,"Store details updated.")
                    return redirect('store_details')
                else:
                    store_details.objects.create(store_vendor = request.user,store_name=store_name,store_email=store_email,abline1=store_abline1,abline2=store_abline2,abline3=store_abline3,city=city,district=district,store_facebook=store_facebook,store_instagram=store_instagram,store_twitter=store_twitter,zip=zip,store_logo = request.FILES['store_logo'])
                    return redirect('store_details')

            except Exception as e:
                print(e)
                messages.success(request,e)
                return redirect('store_details')


        if 'update_user' in request.POST:
            try:
                username= request.POST.get('username')
                password= request.POST.get('password')
                user = User.objects.filter(username=username).first()
                print(user)
                user.set_password(password)
                user.save()
                messages.success(request,"Login credentials changed.")
                return redirect('v_login')
            except Exception as e:
                messages.success(request, str(e))
                return redirect('v_login')



    cur_date = date.today()
    if cust_ins.birthday is not None:
        age = cur_date.year - cust_ins.birthday.year
    else:
        age = ''
    context={'navbar':'store_details','user':user,'last_login':last_login,'address_ins':address_ins,'store_ins':store_ins,'age':age}
    return render(request,'vendor_profile.html',context)


@vendor_requirded(login_url='v_login')
def all_products(request):
    categories = category.objects.all()
    product = products.objects.filter(vendoraddedby = request.user.customer.id)
    get_cat_id = request.GET.get('category')
    get_rating = request.GET.get('rating')

    if get_cat_id:
        product = products.objects.filter(itmclass=get_cat_id, vendoraddedby = request.user.customer.id)

    if get_rating:
        min_rating_value = float(get_rating)

        # Annotate average rating for products
        products_queryset = product.annotate(
            get_average_rating=Avg('reviews__rating')
        )

        # Filter products based on minimum rating
        product = products_queryset.filter(
            get_average_rating__gte=min_rating_value
        )

    if request.method == 'GET':
        search_attr = request.GET.get('search', '')
        if search_attr:
            product = products.objects.filter(itmname__icontains=search_attr,vendoraddedby = request.user.customer.id)
    page = request.GET.get('page',1)
    paginator = Paginator(product,10)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)

    context={'navbar':'products','categories':categories,'products':product,'paginator':page}
    return render(request,'products.html',context)

@vendor_requirded(login_url='v_login')
def toggle_product(request, product_id):
    product = get_object_or_404(products, id=product_id)
    product.itm_isactive = not product.itm_isactive
    product.save()
    return JsonResponse({'success': True, 'is_active': product.itm_isactive})

@vendor_requirded(login_url='v_login')
def add_product_variant(request,id):
    product_ins = products.objects.get(id=id)
    variant = product_variants()
    try:
        varient_name = request.POST.get('varient_name')
        color_code = request.POST.get('color_code')
        quantity = request.POST.get('quantity')

        if not varient_name or color_code or quantity:
            return JsonResponse({'error': True})
        else:
            variant.product_id=product_ins
            variant.varient_name = varient_name
            variant.color_code = color_code
            variant.quantity = quantity
            variant.save()
    except Exception as e:
        print(e)
    return JsonResponse({'success': True})


@vendor_requirded(login_url='v_login')
def update_product_variant(request):
    # Extract data from the POST request
    variant_id = request.POST.get('variant_id')
    varient_name = request.POST.get('varient_name')
    color_code = request.POST.get('color_code')
    quantity = request.POST.get('quantity')

    try:
        variant = product_variants.objects.get(id=variant_id)
        variant.varient_name = varient_name
        variant.color_code = color_code
        variant.quantity = quantity
        variant.save()

        # Optionally, you can return a success message or any other data
        return JsonResponse({'success': True, 'message': 'Variant updated successfully'})
    except product_variants.DoesNotExist:
        # Variant with the given ID does not exist
        return JsonResponse({'success': False, 'message': 'Variant not found'}, status=404)
    except Exception as e:
        # Handle other exceptions
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@vendor_requirded(login_url='v_login')
def delete_variant(request,id):
    variant = get_object_or_404(product_variants,id=id)
    product_id= variant.product_id.id
    variant.delete()
    return redirect('/product_details/'+str(product_id))


@vendor_requirded(login_url='v_login')
def product_add(request):
    if request.method=='POST':
        try:
            product = products()
            product_image = product_images()
            product_name = request.POST.get('product_name')
            product_title = request.POST.get('product_title')
            product_desc = request.POST.get('product_desc')
            old_price = request.POST.get('old_price')
            new_price = request.POST.get('new_price')
            product_status = request.POST.get('product_status')
            product_category = request.POST.get('product_category')
            product_subcategory = request.POST.get('product_subcategory')
            product_sku = request.POST.get('product_sku')
            product_tag = request.POST.get('product_tag')

            if not products.objects.filter(itmname=product_name,itmtitle=product_title,vendoraddedby = request.user.customer,itm_old_price=old_price,itm_new_price=new_price,sku_no=product_sku,itm_tags=product_tag).exists():
                product.vendoraddedby = request.user.customer
                product.itmname=product_name
                product.itmtitle=product_title
                product.itmdesc=product_desc
                product.itm_old_price=old_price
                product.itm_new_price=new_price
                product.itm_isactive=product_status
                product.sku_no=product_sku
                product.itm_tags=product_tag
                if product_category:
                    cat_ins = category.objects.get(id=product_category)
                    product.itmclass=cat_ins
                if product_subcategory:
                    subcat_ins = subcategory.objects.get(id=product_subcategory)
                    product.itmsubclass=subcat_ins
                product.save()
                product = products.objects.get(itmname=product_name,itmtitle=product_title,vendoraddedby = request.user.customer)

                product_image.product_id = product
                if 'image1' in request.FILES:
                    product_image.image1 = request.FILES['image1']
                if 'image2' in request.FILES:
                    product_image.image2 = request.FILES['image2']
                if 'image3' in request.FILES:
                    product_image.image3 = request.FILES['image3']
                if 'image4' in request.FILES:
                    product_image.image4 = request.FILES['image4']
                if 'image5' in request.FILES:
                    product_image.image5 = request.FILES['image5']
                product_image.save()
                return redirect('products')
        except Exception as e:
            print(e)
        return redirect('products')

    categories = category.objects.all()
    sub_categories = subcategory.objects.all()
    context={'navbar':'products','categories':categories,'sub_categories':sub_categories}
    return render(request,'product_add.html',context)

@vendor_requirded(login_url='v_login')
def product_details(request,id):
    if request.method=='POST':
        try:
            product = products.objects.get(id=id)
            # product_image = product_images.objects.get(product_id=product)
            product_name = request.POST.get('product_name')
            product_title = request.POST.get('product_title')
            product_desc = request.POST.get('product_desc')
            old_price = request.POST.get('old_price')
            new_price = request.POST.get('new_price')
            product_coupon = request.POST.get('product_coupon')
            product_status = request.POST.get('product_status')
            product_category = request.POST.get('product_category')
            product_subcategory = request.POST.get('product_subcategory')
            product_sku = request.POST.get('product_sku')
            product_tag = request.POST.get('product_tag')
            sizes = request.POST.getlist('size')

            if product_coupon == 'No Discount' or product_coupon == '' :
                if discount.objects.filter(vendor_by=request.user,if_on_product=product):
                    discount.objects.filter(vendor_by=request.user,if_on_product=product).update(if_on_product = None)
                else:
                    pass
            else:
                discount.objects.filter(offer=product_coupon,vendor_by=request.user).update(if_on_product=product)

            product.itmname=product_name
            product.itmtitle=product_title
            product.itmdesc=product_desc
            product.itm_old_price=old_price
            product.itm_new_price=new_price
            product.itm_isactive=product_status
            product.sku_no=product_sku
            product.itm_tags=product_tag

            if product_category:
                cat_ins = category.objects.get(id=product_category)
                product.itmclass=cat_ins
            if product_subcategory:
                subcat_ins = subcategory.objects.get(id=product_subcategory)
                product.itmsubclass=subcat_ins
            product.save()

            # if 'image1' in request.FILES:
            #     product_image.image1 = request.FILES['image1']
            # if 'image2' in request.FILES:
            #     product_image.image2 = request.FILES['image2']
            # if 'image3' in request.FILES:
            #     product_image.image3 = request.FILES['image3']
            # if 'image4' in request.FILES:
            #     product_image.image4 = request.FILES['image4']
            # if 'image5' in request.FILES:
            #     product_image.image5 = request.FILES['image5']
            # product_image.save()

            if not product_sizes.objects.filter(product=product).first():
                for size in sizes:
                    product_sizes.objects.create(
                        product=product,
                        product_size=size
                    )
            else:
                existing_sizes = product_sizes.objects.filter(product=product)
                existing_sizes.delete()
                for size in sizes:
                    product_sizes.objects.create(
                        product=product,
                        product_size=size
                    )

        except Exception as e:
            print(e)
    product = products.objects.filter(id=id).first()
    pro_sizes = product_sizes.objects.filter(product=product)
    categories = category.objects.all()
    sub_categories = subcategory.objects.all()
    product = products.objects.filter(id=id)
    pro_id = product.first().id
    coupon = discount.objects.filter(if_on_product = pro_id,vendor_by = request.user).first()
    variants = product_variants.objects.filter(product_id=id)
    context={'navbar':'products','product':product,'categories':categories,'sub_categories':sub_categories,'variants':variants,'coupon':coupon,'pro_sizes':pro_sizes}
    return render(request,'product_details.html',context)

@vendor_requirded(login_url='v_login')
def all_orders(request):
    store_details_ins = store_details.objects.filter(store_vendor=request.user).first()
    order_list = orders.objects.filter(vendor_id = store_details_ins)
    print(order_list.first())
    context={'navbar':'orders','order_list':order_list}
    return render(request,'orders.html',context)


@vendor_requirded(login_url='v_login')
def order_details(request,id):
    order_detail = get_object_or_404(orders, pk=id)
    customer_instance = order_detail.cutomer_id
    user_instance = customer_instance.user
    user_address = address.objects.filter(username=user_instance,isactive = True)
    context={'navbar':'orders','order_detail':order_detail,'user_address':user_address}
    return render(request,'order_details.html',context)

@vendor_requirded(login_url='v_login')
def customers(request):
    order_list = orders.objects.filter(vendor_id = request.user.id)
    customer_instances = []
    for order in order_list:
        customer_instance = order.cutomer_id
        customer_instances.append(customer_instance)
    context={'navbar':'customers','customer_instances':customer_instances}
    return render(request,'customers.html',context)

@vendor_requirded(login_url='v_login')
def customer_details(request,id):
    customers = customer.objects.filter(id = id)
    customer_instance = customer.objects.filter(id=id).first()
    if customer_instance:
        user_instance = customer_instance.user
        user_address = address.objects.filter(username=user_instance, isactive=True)

    all_order_customer = orders.objects.filter(cutomer_id = customer_instance,vendor_id = request.user.id)
    context={'navbar':'customers','customers':customers,'user_address':user_address,'all_order_customer':all_order_customer}
    return render(request,'customer_details.html',context)

@vendor_requirded(login_url='v_login')
def sales_promotions(request):
    cupons = discount.objects.filter(vendor_by = request.user)
    context={'navbar':'sales_promotions','cupons':cupons}
    return render(request,'sales_promotions.html',context)

@vendor_requirded(login_url='v_login')
def coupon_edit(request, id):
    coupon = discount.objects.filter(id=id)
    categories = category.objects.all()

    if request.method == 'POST':
        try:
            coupon = discount.objects.get(id=id)
            coupon_status = request.POST.get('couponsstatus')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            coupon_code = request.POST.get('coupon_name')
            discount_category_id = request.POST.get('discount_category')
            coupon_type_id = request.POST.get('couponstype')
            discount_value = request.POST.get('discount_value')

            discount_type_ins = discount_type.objects.get(id=coupon_type_id)
            # Update the attributes of the coupon object
            coupon.offer = coupon_code
            coupon.offer_cat = discount_type_ins
            if discount_category_id:
                discount_category_ins = category.objects.get(id=discount_category_id)
                coupon.if_on_category = discount_category_ins
            else:
                coupon.if_on_category = None
            coupon.discount_value = discount_value
            coupon.is_active = coupon_status
            coupon.start_date = start_date
            coupon.end_date = end_date

            # Save the updated object to the database
            coupon.save()

            return redirect('sales_promotions')
        except Exception as e:
            messages.error(request,e)
            return redirect('/coupon_edit/'+ str(id))

    context = {'navbar': 'sales_promotions', 'categories': categories, 'coupon': coupon}
    return render(request, 'coupon_edit.html', context)

@vendor_requirded(login_url='v_login')
def coupon_add(request):
    categories = category.objects.all()
    if request.method == 'POST':
        try:
            coupon_status = request.POST.get('couponsstatus')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            coupon_code = request.POST.get('coupon_name')
            discount_category_id = request.POST.get('discount_category')
            coupon_type_id = request.POST.get('couponstype')
            discount_value = request.POST.get('discount_value')

            discount_type_ins = discount_type.objects.get(id=coupon_type_id)
            if discount_category_id:
                discount_category_ins = category.objects.get(id=discount_category_id)
            else:
                discount_category_ins = None

            discount.objects.create(vendor_by=request.user,offer=coupon_code,offer_cat=discount_type_ins,if_on_category=discount_category_ins,discount_value=discount_value,is_active=coupon_status,start_date=start_date,end_date=end_date)
            return redirect('sales_promotions')
        except Exception as e:
            print(e)
            messages.error(request,e)
            return redirect('/coupon_add/')
    context={'navbar':'sales_promotions','categories':categories}
    return render(request,'coupon_add.html',context)

def coupon_delete(request,id):
    del_ind = discount.objects.get(id=id)
    del_ind.delete()
    return redirect('sales_promotions')

@vendor_requirded(login_url='v_login')
def create_invoice(request):
    context={'navbar':'create_invoice'}
    return render(request,'create_invoice.html',context)

@vendor_requirded(login_url='v_login')
def update_invoice(request,id):
    invoice_ins = order_invoices.objects.get(id=id)
    vendor_ins = User.objects.get(id=invoice_ins.order_id.vendor_id.store_vendor.id)
    context={'navbar':'create_invoice','invoice_ins':invoice_ins,'vendor_ins':vendor_ins}
    return render(request,'update_invoice.html',context)

@vendor_requirded(login_url='v_login')
def all_invoices(request):
    order_list = orders.objects.filter(vendor_id = request.user.id)
    invoice_list = []
    for order in order_list:
        invoices = order_invoices.objects.get(order_id = order)
        invoice_list.append(invoices)
    context={'navbar':'create_invoice','invoice_list':invoice_list}
    return render(request,'invoice.html',context)


def render_to_pdf(template,data={}):
    template = get_template(template)
    html = template.render(data)
    results = BytesIO()
    pdf  = pisa.pisaDocument(html.encode("UTF-8"),results)
    if not pdf.err:
        return HttpResponse(results.getvalue(),content_type="application/pdf")
    return None


def generate_invoice(request,id):
    try:
        order_detail = orders.objects.get(id=id,vendor_id=request.user.id)
    except:
        return HttpResponse('Invoice Not Found')
    data = {
        'order_id':order_detail.id,
        'name':order_detail.cutomer_id.name,
        'paymentid':order_detail.paymentid,
    }
    pdf = render_to_pdf('generate_invoice.html',data)
    return HttpResponse(pdf,content_type='application/pdf')
    # return render(request,'generate_invoice.html')


@vendor_requirded(login_url='v_login')
def all_report(request):
    context={'navbar':'all_report'}
    return render(request,'all_reports.html',context)

@vendor_requirded(login_url='v_login')
def help(request):
    context={'navbar':'help'}
    return render(request,'help.html',context)

@csrf_exempt
def vendor_login(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            password = request.POST["password"]
            username_ins = User.objects.filter(email=username).first()
            if username_ins:
                username = username_ins.username
            else:
                username = request.POST["username"]
            user = authenticate(request,username = username, password=password)
            login(request,user)
            store_document_ins = store_document.objects.filter(store_vendor=request.user.id).exists()
            cust_ins = customer.objects.get(user=user)
            if user is None:
                messages.error(request,"Enter correct credintials!")
                return redirect('v_login')
            elif user.is_staff == True:
                return redirect('v_dashboard')
            elif cust_ins.email_isverified == False:
                messages.error(request,"Please verify your email.")
                return redirect('waiting_email_verification')
            elif store_document_ins == False:
                messages.error(request,"Please verify your documents.")
                return redirect('v_register_type')
            else:
                messages.error(request,"You are not verified yet.")
                return redirect('v_login')
        except Exception as e:
            messages.error(request,"Enter correct credintials!")
            return redirect('v_login')

    context={}
    return render(request,'v_login.html',context)

@csrf_exempt
def v_register(request,*args, **kwargs):
    code  = str(kwargs.get('ref_code'))
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            name = request.POST['name']
            email = request.POST['email']
            phone_number = request.POST['phone']
            terms_and_conditions = request.POST.get('termsandconditions', False)
            phone_number = request.POST.get('phone', '')
            if len(phone_number) >= 10 and not phone_number.isdigit():
                messages.error(request,"Phone number must be 10 digits!")
                return redirect('v_register')
            if terms_and_conditions:
                if User.objects.filter(username=username).exists():
                    messages.info(request,"Username is already taken.")
                    return redirect('v_register')
                if User.objects.filter(email=email).exists():
                    messages.info(request,"This email is already registered.")
                    return redirect('v_register')
                if customer.objects.filter(phone_number=phone_number):
                    messages.info(request,"This phone number is already registered.")
                    return redirect('v_register')
                # Create a new user
                user = User.objects.create_user(username=username, password=password)
                user.first_name = name
                user.email = email
                user.save()
                # Create a user profile
                if code == "None":
                    customer.objects.create(user=user, name = username, email=email, phone_number=phone_number)

                else:
                    user_ins = customer.objects.get(code = code)
                    customer.objects.create(user=user, name = username, email=email, phone_number=phone_number,referred_by_user=user_ins.user)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('waiting_email_verification')
            else:
                messages.error(request,"Kindly agree to the Terms & Conditions.")
                return redirect('v_register')
        except Exception as e:
            messages.error(request,str(e)[:25])
            return redirect('v_register')
    context={}
    return render(request,'v_register.html',context)

def waiting_email_verification(request):
    cust_ins = customer.objects.filter(user=request.user.id).first()
    if cust_ins == None:
        messages.error(request,"Please login to continue.")
        return redirect('v_login')
    if cust_ins.email_isverified == True:
        messages.error(request,"Email is already verified.")
        return redirect('v_register_type')
    else:
        subject = 'Please verify your email.'
        from_email = settings.EMAIL_HOST_USER
        to_email = [cust_ins.email]
        # static_image_url = f"{settings.BASE_URL}{settings.STATIC_URL}/images/logo-blue.png"
        base_url = settings.BASE_URL
        html_content = render_to_string('email_verification.html', {'base_url':base_url,'customer_ins': cust_ins})
        email = EmailMultiAlternatives(subject, 'This is a plain text message.', from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()
    return redirect('verify_email')

@csrf_exempt
def verify_email(request):
    cust_ins = customer.objects.filter(user=request.user.id).first()
    if cust_ins == None:
        messages.error(request,"Please login to continue.")
        return redirect('v_login')
    elif cust_ins.email_isverified == True:
        return redirect('v_register_type')
    else:
        if request.method == "POST":
            token = request.POST.get('token')
            cust_ins = customer.objects.filter(user=request.user.id).first()
            if cust_ins != None:
                if token == cust_ins.email_verification_code:
                    cust_ins.email_isverified = True
                    cust_ins.save()
                    return redirect('v_register_type')
                elif token == '':
                    messages.error(request,"Please enter OTP")
                    return redirect('verify_email')
                else:
                    messages.error(request,"Invalid OTP")
                    return redirect('verify_email')
    return render(request,'wating_email_verification.html')


def v_register_type(request):
    cust_ins = customer.objects.filter(user=request.user.id).first()
    if cust_ins is None:
        messages.error(request,"Please login to continue.")
        return redirect('v_login')
    elif cust_ins.email_isverified == False:
        messages.error(request,"Please verify email to continue.")
        return redirect('waiting_email_verification')
    return render(request,'v_register_type.html')

def v_register_gst(request):
    print(request.user)
    if request.method == 'POST':
        try:
            store_name = request.POST['store_name']
            gst_no = request.POST.get('gst_no')
            micr_code = request.POST.get('micr_code')
            adhar_card = request.FILES.get('adhar_card')
            cancelled_check = request.FILES.get('cancelled_check')
            pan_card = request.FILES.get('pan_card')
            gst_certificate = request.FILES.get('gst_certificate')
            store_doc_ins = store_document.objects.filter(store_vendor = request.user).exists()
            store_detail_ins = store_details.objects.filter(store_vendor = request.user).exists()

            # Check if any required field is missing
            if not all([store_name, gst_no, micr_code, adhar_card, cancelled_check, pan_card, gst_certificate]):
                messages.error(request, "Please fill all the required fields.")
                return redirect('v_register_gst')

            elif store_doc_ins == False and store_detail_ins == False:
                store_details.objects.create(store_vendor = request.user,store_name=store_name)
                store_document.objects.create(store_vendor=request.user,adhar_card=request.FILES['adhar_card'],cancel_check=request.FILES['cancelled_check'],pan_card=request.FILES['pan_card'],gst_no=gst_no,gst_certificate=request.FILES['gst_certificate'],bank_micr=micr_code)
                if 'trade_lisence' in request.FILES:
                        store_ins = store_document.objects.get(gst_no=gst_no)
                        store_ins.trade_lisence=request.FILES['trade_lisence']

            elif store_doc_ins == False and store_detail_ins == True:
                store_details_ins = store_details.objects.filter(store_vendor = request.user).first()
                store_details_ins.store_name = store_name
                store_details_ins.save()
                store_document.objects.create(store_vendor=request.user,adhar_card=request.FILES['adhar_card'],cancel_check=request.FILES['cancelled_check'],pan_card=request.FILES['pan_card'],gst_no=gst_no,gst_certificate=request.FILES['gst_certificate'],bank_micr=micr_code)
                if 'trade_lisence' in request.FILES:
                    store_ins = store_document.objects.get(gst_no=gst_no)
                    store_ins.trade_lisence=request.FILES['trade_lisence']
                messages.success(request,"We are verifying your account.")
                return redirect('v_login')
            else:
                messages.error(request,"Store already exists!")
                return redirect('v_login')
        except Exception:
            messages.error(request,"Fill the form correctly.")
            return redirect('v_register_gst')
    return render(request,'register_gst.html')

def terms_and_conditions(request):
    return render(request,'terms_and_conditions.html')


def v_register_aadhaar(request):
    if request.method == 'POST':
        try:
            store_name = request.POST['store_name']
            micr_code = request.POST.get('micr_code')
            adhar_card = request.FILES.get('adhar_card')
            cancelled_check = request.FILES.get('cancelled_check')
            pan_card = request.FILES.get('pan_card')
            store_doc_ins = store_document.objects.filter(store_vendor = request.user).exists()
            store_detail_ins = store_details.objects.filter(store_vendor = request.user).exists()

            # Check if any required field is missing
            if not all([store_name, micr_code, adhar_card, cancelled_check, pan_card]):
                messages.error(request, "Please fill all the required fields.")
                return redirect('v_register_gst')
            elif store_doc_ins == False and store_detail_ins == False:
                print("1")
                store_details.objects.create(store_vendor = request.user,store_name=store_name)
                store_document.objects.create(store_vendor=request.user,adhar_card=request.FILES['adhar_card'],cancel_check=request.FILES['cancelled_check'],pan_card=request.FILES['pan_card'],bank_micr=micr_code)

            elif store_doc_ins == False and store_detail_ins == True:
                print("2")
                store_details_ins = store_details.objects.filter(store_vendor = request.user).first()
                store_details_ins.store_name = store_name
                store_details_ins.save()
                store_document.objects.create(store_vendor=request.user,adhar_card=request.FILES['adhar_card'],cancel_check=request.FILES['cancelled_check'],pan_card=request.FILES['pan_card'],bank_micr=micr_code)
                messages.success(request,"We are verifying your account.")
                return redirect('v_login')

            else:
                messages.error(request,"Store already exists!")
                return redirect('v_login')
        except Exception as e:
            messages.error(request,"Fill the form correctly.")
            return redirect('v_register_aadhaar')
    return render(request,'register_aadhaar.html')

def vendor_logout(request):
    logout(request)
    return redirect('v_login')


def vendor_reset_email(request):
    try:
        email_is_verified = request.session.get('email_is_verified', False)
        if email_is_verified:
            messages.info(request,"Email already verified, enter new password.")
            return redirect('vendor_setpassword')
        email_code = request.session.get('email_code')
        now = datetime.datetime.now()
        expiry_get_str = request.session['expiry_otp']
        expiry_get = datetime.datetime.fromisoformat(expiry_get_str)
        if now < expiry_get:
            messages.info(request,"OTP already sent!")
            return redirect('vendor_resetpassword')
        if request.method == 'POST':
            email_id = request.POST.get('email')
            request.session['email_id'] = email_id
            if not request.session.get('email_code'):
                email_code = generate_unique_code()
                request.session['email_code'] = email_code
                expiry_date = generate_expiry(request)
                request.session['expiry_otp'] = expiry_date
            else:
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
            return redirect('/vendor_resetpassword/')
    except Exception:
            messages.error(request,"Unexpected error!!")
            return redirect('/vendor_reset_email/')
    return render(request,'vendor_email_reset.html')


def vendor_resetpassword(request):
    try:
        email_code = request.session.get('email_code')
        if not email_code:
            messages.error(request,"Verify your email first!")
            return redirect('vendor_reset_email')
        email_is_verified = request.session.get('email_is_verified', False)
        if email_is_verified:
            messages.info(request,"Email already verified, enter new password.")
            return redirect('vendor_setpassword')
        email_code = request.session.get('email_code')
        if request.method == 'POST':
            user_input_code = request.POST.get('token')
            if email_code == user_input_code:
                request.session['email_is_verified'] = True
                messages.success(request,"Email verified, enter new password.")
                return redirect('vendor_setpassword')
            else:
                request.session['email_is_verified'] = False
                messages.error(request,"Wrong OTP!")
                return redirect('vendor_resetpassword')
    except Exception:
        messages.error(request,"Unexpected error!!")
        return redirect('vendor_resetpassword')
    return render(request,'vendor_forgot_pass.html')


def resend_otp_vendor(request):
    email_id = request.session.get('email_id')
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
    return redirect('/vendor_resetpassword/')


def vendor_setpassword(request):
    try:
        email_code = request.session.get('email_code')
        if not email_code:
            messages.error(request,"Verify your email first!")
            return redirect('vendor_reset_email')
        email_id = request.session.get('email_id')
        email_is_verified = request.session.get('email_is_verified', False)
        if request.method == 'POST':
            if email_is_verified:
                password= request.POST.get('password')
                user = User.objects.filter(email=email_id).first()
                user.set_password(password)
                user.save()
                del request.session['email_id']
                del request.session['email_code']
                del request.session['email_is_verified']
                messages.success(request,"Login credentials changed.")
                return redirect('v_login')
            else:
                messages.error(request,"Verify your OTP first!")
                return redirect('vendor_resetpassword')
    except Exception:
        messages.error(request,"Unexpected error!!")
        return redirect('vendor_setpassword')
    return render(request,'set_new_password.html')


@csrf_exempt
def vendor_admin_login(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            password = request.POST["password"]
            username_ins = User.objects.filter(email=username).first()
            if username_ins:
                username = username_ins.username
            else:
                username = request.POST["username"]

            user = authenticate(request,username = username, password=password)
            if user.is_superuser == True:
                login(request,user)
                return redirect('vendor_admin')
        except Exception as e:
            print(e)
            messages.error(request,"Login Error!")
            return redirect('vendor_admin_login')
    return render(request,'vendor_admin_login.html')


@superuser_required(login_url='vendor_admin_login')
def vendor_admin(request):
    store_users = User.objects.filter(
    store_details__isnull=False,
    is_superuser=False
).order_by('date_joined')

    from django.db.models import Q
    if request.method == 'GET':
        search_attr = request.GET.get('search', '')
        if search_attr:
            store_users = User.objects.filter(
                Q(store_details__store_name__icontains=search_attr) |
                Q(store_details__store_vendor__email__icontains=search_attr),
                is_superuser=False
            ).select_related('store_details').order_by('date_joined')

    page = request.GET.get('page',1)
    paginator = Paginator(store_users,20)
    try:
        store_users = paginator.page(page)
    except PageNotAnInteger:
        store_users = paginator.page(1)
    except EmptyPage:
        store_users = paginator.page(paginator.num_pages)
    context = {'store_users':store_users}
    return render(request,'vendor_admin.html',context)

@superuser_required(login_url='vendor_admin_login')
def vendor_admin_all(request):
    store_users = User.objects.filter(
    is_superuser=False
).order_by('date_joined')

    from django.db.models import Q
    if request.method == 'GET':
        search_attr = request.GET.get('search', '')
        if search_attr:
            store_users = User.objects.filter(
                Q(username__icontains=search_attr) | Q(email__icontains=search_attr),
                is_superuser=False
            ).select_related('store_details').order_by('date_joined')

    page = request.GET.get('page',1)
    paginator = Paginator(store_users,20)
    try:
        store_users = paginator.page(page)
    except PageNotAnInteger:
        store_users = paginator.page(1)
    except EmptyPage:
        store_users = paginator.page(paginator.num_pages)
    context = {'store_users':store_users}
    return render(request,'vendor_admin_all.html',context)


@superuser_required(login_url='vendor_admin_login')
def vendor_gst(request,id):
    user = User.objects.filter(id=id).first()
    terms_and_conditions = request.POST.get('termsandconditions', False)
    if request.method == 'POST':
        if terms_and_conditions == '':
            user.is_staff = True
            user.save()
            subject = 'Vendor access has been  granted'
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.customer.email]
            base_url = settings.BASE_URL
            html_content = render_to_string('vedor_access_granted_email.html', {'base_url':base_url,'instance': user})
            email = EmailMultiAlternatives(subject, 'This is a plain text message.', from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send()
    context={'user':user}
    return render(request,'vendor_gst.html',context)


@superuser_required(login_url='vendor_admin_login')
def vendor_aadhaar(request,id):
    user = User.objects.filter(id=id).first()
    terms_and_conditions = request.POST.get('termsandconditions', False)
    if request.method == 'POST':
        if terms_and_conditions == '':
            user.is_staff = True
            user.save()
            subject = 'Vendor access has been  granted'
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.customer.email]
            base_url = settings.BASE_URL
            html_content = render_to_string('vedor_access_granted_email.html', {'base_url':base_url,'instance': user})
            email = EmailMultiAlternatives(subject, 'This is a plain text message.', from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send()
    context={'user':user}
    return render(request,'vendor_aadhaar.html',context)
