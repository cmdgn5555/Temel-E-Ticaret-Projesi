from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta

# Create your views here.



def product_quantity_view(request):
    if request.user.is_authenticated:
        return BasketProduct.objects.filter(user=request.user)
    else:
        return None




def index_view(request):
    
    products = Product.objects.all()
    
    favorite_products = Favoriler.objects.all()

    if request.method == "POST":
        urunid = request.POST.get("urun_id")

        urun = Product.objects.filter(id=urunid).first() 

        if not urun:
            return redirect("index")

        if request.POST.get("btnsubmit") == "btnsepet":

            sepet_urun = BasketProduct.objects.filter(user=request.user, product=urun).first()

            if sepet_urun:
                sepet_urun.quantity += 1
                sepet_urun.save()
                
                return redirect("index")
            
            else:
                sepet_urun = BasketProduct.objects.create(
                    user = request.user,
                    product = urun,
                    quantity = 1
                )

                sepet_urun.save()
                
                return redirect("index")
            
        
        elif request.POST.get("btnsubmit") == "btnfavori":

            current_url = request.get_full_path()

            if Favoriler.objects.filter(user=request.user, product=urun).exists():
                favori = Favoriler.objects.get(user=request.user, product=urun)
                favori.delete()
                return redirect(current_url)
            
            else:
                favori = Favoriler.objects.create(
                    user = request.user,
                    product = urun
                )

                favori.save()
                return redirect(current_url)

    
    data = {
        "products": products,
        "favorite_products": favorite_products,
        "product_quantity": product_quantity_view(request)
    }
    
    return render(request, "index.html", data)




@login_required(login_url="/login/")
def category_view(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    genders = Gender.objects.all()
    colors = Color.objects.all()
    case_shapes = CaseShape.objects.all()
    strap_types = StrapType.objects.all()
    glass_features = GlassFeature.objects.all()
    styles = Style.objects.all()
    mechanisms = Mechanism.objects.all()
    favorite_products = Favoriler.objects.all()

    filters = Q()

    if "markasi" in request.GET:
        markalar = request.GET.getlist("markasi")
        for marka in markalar:
            filters |= Q(brand__brand=marka)
    
    
    if "cinsiyet" in request.GET:
        filters &= Q(gender=request.GET.get("cinsiyet"))
    

    if "rengi" in request.GET:
        renkler = request.GET.getlist("rengi")
        for renk in renkler:
            filters |= Q(color__color=renk)
    

    if "kasanin_sekli" in request.GET:
        kasa_sekilleri = request.GET.getlist("kasanin_sekli")
        for kasa_sekli in kasa_sekilleri:
            filters |= Q(case_shape__case_shape=kasa_sekli)
    

    if "kayisin_tipi" in request.GET:
        kayis_tipleri = request.GET.getlist("kayisin_tipi")
        for kayis_tipi in kayis_tipleri:
            filters |= Q(strap_type__strap_type=kayis_tipi)
    

    if "camin_ozelligi" in request.GET:
        cam_ozellikleri = request.GET.getlist("camin_ozelligi")
        for cam_ozelligi in cam_ozellikleri:
            filters |= Q(glass_feature__glass_feature=cam_ozelligi)
    

    if "tarzi" in request.GET:
        tarzlar = request.GET.getlist("tarzi")
        for tarz in tarzlar:
            filters |= Q(style__style=tarz)
    

    if "mekanizmasi" in request.GET:
        mekanizmalar = request.GET.getlist("mekanizmasi")
        for mekanizma in mekanizmalar:
            filters |= Q(mechanism__mechanism=mekanizma)
    
    
    fiyat_min = request.GET.get("fiyat_min")
    fiyat_max = request.GET.get("fiyat_max")

    if fiyat_min in (None, ""):
        fiyat_min = 0.0
    
    else:
       fiyat_min = float(fiyat_min)
       
        
    if fiyat_max in (None, ""):
        fiyat_max = 1000000000.0
    
    else:
       fiyat_max = float(fiyat_max)
        
    
    if fiyat_min > fiyat_max:
        messages.error(request, "Minimum Fiyat Maksimum Fiyattan Büyük Olamaz!")
        return render(request, "category.html")
        
        
    filters &= Q(price__gte=fiyat_min, price__lte=fiyat_max)
    
    products = products.filter(filters)

    if request.method == "POST":
        urunid = request.POST.get("urun_id")

        urun = Product.objects.get(id=urunid)

        if request.POST.get("btnsubmit") == "btnsepet":

            current_url = request.get_full_path()

            sepet_urun = BasketProduct.objects.filter(user=request.user, product=urun).first()

            if sepet_urun:
                sepet_urun.quantity += 1
                sepet_urun.save()
                
                return redirect(current_url)
            
            else:
                sepet_urun_ekle = BasketProduct.objects.create(
                    user = request.user,
                    product = urun,
                    quantity = 1
                )

                sepet_urun_ekle.save()
                
                return redirect(current_url)
        
        
        elif request.POST.get("btnsubmit") == "btnfavori":

            current_url = request.get_full_path()

            if Favoriler.objects.filter(user=request.user, product=urun).exists():
                favori = Favoriler.objects.get(user=request.user, product=urun)
                favori.delete()
                return redirect(current_url)
            
            else:
                favori = Favoriler.objects.create(
                    user = request.user,
                    product = urun
                )

                favori.save()
                return redirect(current_url)
            

    sayfalandirici = Paginator(products, 4)
    sayfa_no = request.GET.get("page")
    products = sayfalandirici.get_page(sayfa_no)
    
    
    data = {
        "products": products,
        "brands": brands,
        "genders": genders,
        "colors": colors,
        "case_shapes": case_shapes,
        "strap_types": strap_types,
        "glass_features": glass_features,
        "styles": styles,
        "mechanisms": mechanisms,
        "favorite_products": favorite_products,
        "product_quantity": product_quantity_view(request)

    }

    return render(request, "category.html", data)




@login_required(login_url="/login/")
def basket_view(request):
    sepet_urunler = BasketProduct.objects.filter(user=request.user)

    kargo = 29.99
    product_total_price = 0
    total_price = 0

    for urun in sepet_urunler:
        product_total_price += urun.product.price * urun.quantity
    total_price = kargo + product_total_price
    
    
    if request.method == "POST":
        prod_id = request.POST.get("prod_id")

        if request.POST.get("btnsubmit") == "btnsil":
            sepet_urun = BasketProduct.objects.get(id=prod_id)
            sepet_urun.delete()

            return redirect("sepet")
        
        
        elif request.POST.get("btnsubmit") == "btneksi":
            sepet_urun = BasketProduct.objects.get(id=prod_id)
            sepet_urun.quantity -= 1
            sepet_urun.save()

            return redirect("sepet")
        

        elif request.POST.get("btnsubmit") == "btnartı":
            sepet_urun = BasketProduct.objects.get(id=prod_id)
            sepet_urun.quantity += 1
            sepet_urun.save()

            return redirect("sepet")

    
    data = {
        "basket_products": sepet_urunler,
        "product_total_price": product_total_price,
        "total_price": total_price,
        "kargo": kargo,
        "product_quantity": product_quantity_view(request)
    }
    
    return render(request, "basket.html", data)




@login_required(login_url="/login/")
def profile_view(request):
    kullanici = User.objects.get(username=request.user)
    profili = Profile.objects.get(user=request.user)
    adresi = Address.objects.get(user=request.user)

    if request.method == "POST":
        
        if request.POST.get("btnsubmit") == "btnsifre":
            eski_sifre = request.POST.get("eskisifre")
            yeni_sifre = request.POST.get("yenisifre")
            yeni_sifre_tekrar = request.POST.get("yenisifretekrar") 

            if yeni_sifre == yeni_sifre_tekrar:
                
                if kullanici.check_password(eski_sifre):
                    kullanici.set_password(yeni_sifre)
                    kullanici.save() 
                    logout(request)
                    return redirect("giris")
                
                else:
                    messages.error(request, "Eski Şifrenizi Yanlış Girdiniz! Tekrar Deneyiniz...")
            
            else:
                messages.error(request, "Şifreler Birbirlerine Uymamaktadır! Tekrar Deneyiniz...")
        

        elif request.POST.get("btnsubmit") == "btnprofil":
            ad = request.POST.get("isim")
            soyad = request.POST.get("soyisim")
            e_posta = request.POST.get("eposta")
            telefon_no = request.POST.get("telefon")
            dogum_tarihi = request.POST.get("dogumtarihi")

            
            if kullanici.email != e_posta:
                
                if not User.objects.filter(email=e_posta).exists():
                    kullanici.first_name = ad
                    kullanici.last_name = soyad
                    kullanici.email = e_posta
                    profili.phone_number = telefon_no
                    profili.birthdate = dogum_tarihi

                    kullanici.save()
                    profili.save()
                    return redirect("profil")
            
                else:
                    messages.error(request, "Bu E-Posta Adresi Zaten Başka Bir Kullanıcı Tarafından Kullanılmaktadır")

            else:
                kullanici.first_name = ad
                kullanici.last_name = soyad
                kullanici.email = e_posta
                profili.phone_number = telefon_no
                profili.birthdate = dogum_tarihi

                kullanici.save()
                profili.save()
                return redirect("profil")
        

        elif request.POST.get("btnsubmit") == "btnadres":
            il = request.POST.get("il")
            ilce = request.POST.get("ilçe")
            mahalle = request.POST.get("mahalle")
            adres = request.POST.get("adres")

            adresi.province = il
            adresi.district = ilce
            adresi.neighbourhood = mahalle
            adresi.address = adres

            adresi.save()
            return redirect("profil")

    
    data = {
        "product_quantity": product_quantity_view(request),
        "profili": profili,
        "adresi": adresi
    }
    
    return render(request, "user/profil.html", data)




@login_required(login_url="/login/")
def product_detail_view(request, product_id):
    
    try:
        urunumuz = Product.objects.get(id=product_id)
    
    except Product.DoesNotExist:
        messages.error(request, "Aradığınız ürün mevcut olmadığından ötürü kategori sayfasına yönlendirildiniz.")
        
        return redirect("kategori")


    yorumlar = Yorumlar.objects.filter(product=urunumuz)
    
    yorum_user = None

    for yorum in yorumlar:
        if yorum.user == request.user:
            yorum_user = yorum.user

    if request.method == "POST":

        if request.POST.get("btnsubmit") == "btnsepet":
            
            urunid = request.POST.get("urun_id")

            urun = Product.objects.get(id=urunid)

            miktar = request.POST.get("miktar")

            sepet_urun = BasketProduct.objects.filter(user=request.user, product=urun).first()

            if sepet_urun:
                sepet_urun.quantity += int(miktar)
                sepet_urun.save()
                
                return redirect("ürün-detayi", product_id=product_id)
            
            else:
                sepet_urun_ekle = BasketProduct.objects.create(
                    user = request.user,
                    product = urun,
                    quantity = miktar
                )

                sepet_urun_ekle.save()
                
                return redirect("ürün-detayi", product_id=product_id)
        
        
        elif request.POST.get("btnsubmit") == "btnyorum":
            
            yorum = request.POST.get("yorum")

            yeni_yorum = Yorumlar.objects.create(
                user=request.user,
                first_name = request.user.first_name,
                last_name = request.user.last_name,
                product=urunumuz,
                comment=yorum
            )

            yeni_yorum.save()
            
            return redirect("ürün-detayi", product_id=product_id)
        

        elif request.POST.get("btnsubmit") == "btnyorumgüncelle":
            
            yorumid = request.POST.get("yorum_id")
            yorum = request.POST.get("yorum")
            
            yorum_güncelle = Yorumlar.objects.get(id=yorumid)

            if yorum_güncelle.user == request.user:
                yorum_güncelle.comment = yorum
            
                yorum_güncelle.save()

            return redirect("ürün-detayi", product_id=product_id)
        

        elif request.POST.get("btnsubmit") == "btnyorumsil":

            yorum_id = request.POST.get("yorum_id")
            yorum_sil = Yorumlar.objects.get(id=yorum_id)

            if yorum_sil.user == request.user:
                yorum_sil.delete()

            return redirect("ürün-detayi", product_id=product_id)

            
    data = {
        "product": urunumuz,
        "comments": yorumlar,
        "yorum_user": yorum_user,
        "product_quantity": product_quantity_view(request)

    }

    return render(request, "product-detail.html", data)




@login_required(login_url="/login/")
def favorite_view(request):
    favoriler = Favoriler.objects.filter(user=request.user)

    data = {
        "favorites": favoriler
    }

    return render(request, "favorite.html", data)





def login_view(request):

    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "E-posta ve şifre alanlarının her ikisini de doldurunuz.") 
            return render(request, "user/login.html")
        
        try:
            validate_email(email)
        
        except ValidationError:
            messages.error(request, "Geçersiz formatta bir e-posta adresi girdiniz.")
            return render(request, "user/login.html")

        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            attempt, created = LoginAttempt.objects.get_or_create(user=user) 

            if attempt.locked_until and attempt.locked_until >= now():
                remaining_seconds = (attempt.locked_until - now()).seconds

                if remaining_seconds >= 60:
                    remaining_minutes = remaining_seconds // 60
                    remaining_seconds %= 60
                    messages.error(request, f"Hesabınız kilitli. Lütfen {remaining_minutes} dakika {remaining_seconds} saniye sonra tekrar deneyin.")
                
                else:
                    messages.error(request, f"Hesabınız kilitli. Lütfen {remaining_seconds} saniye sonra tekrar deneyin.")
                
                return render(request, "user/login.html")
            
            
            if attempt.locked_until and attempt.locked_until <= now():
                attempt.attempts = 0
                attempt.locked_until = None
                attempt.save()

            
            
            if user.check_password(password):
                attempt.attempts = 0
                attempt.locked_until = None
                attempt.save()

                login(request, user)
                return redirect("index")
            
            
            else:
                if attempt.last_attempt and (now() - attempt.last_attempt).seconds <= 30:  
                    attempt.attempts += 1                                                                                                  
                
                else:                                                                            
                    attempt.attempts = 1
                
                attempt.last_attempt = now()

                if attempt.attempts >= 3:
                    attempt.locked_until = now() + timedelta(minutes=2)
                    messages.error(request, "Hesabınız çok fazla başarısız giriş denemesi nedeniyle 2 dakika boyunca kilitlendi.")

                else:
                    messages.error(request, f"Şifre hatalı! Kalan deneme hakkınız: {3 - attempt.attempts}")
                
                attempt.save()
                
                return render(request, "user/login.html")


        else:
            messages.error(request, "E-Posta Adresiniz Hatalı! Lütfen Tekrar Deneyiniz")

    return render(request, "user/login.html")





def register_view(request):

    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")


        try:
            validate_email(email)
        
        except ValidationError:
            messages.error(request, "Geçersiz formatta bir e-posta adresi girdiniz.")
            return render(request, "user/register.html", {
                "f_name": first_name,
                "l_name": last_name,
                "mail": email
            })

        
        if password != re_password:
            messages.error(request, "Şifreler eşleşmiyor. Lütfen tekrar deneyin.")
            return render(request, "user/register.html", {
                "f_name": first_name,
                "l_name": last_name,
                "mail": email
            })
        
        
        
        if len(password) < 8:
            messages.error(request, "Şifreniz en az 8 karakter uzunluğunda olmalıdır.")
            return render(request, "user/register.html", {
                "f_name": first_name,
                "l_name": last_name,
                "mail": email
            })
        

        
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            messages.error(request, "Şifreniz hem en az bir harf hem de en az bir rakam içermelidir.")
            return render(request, "user/register.html", {
                "f_name": first_name,
                "l_name": last_name,
                "mail": email
            })

        
        
        if not User.objects.filter(email=email).exists():  
            user = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
        
            user.save()
            login(request, user)
            return redirect("index")
        
        else:
            messages.error(request, "Bu E-Posta Adresi Zaten Başka Bir Kullanıcı Tarafından Kullanılmaktadır")

            return render(request, "user/register.html", {
                "f_name": first_name,
                "l_name": last_name,
                "mail": email
            })
    
    return render(request, "user/register.html")




def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))




def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)

        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        
        except Resolver404:
            view = None
        
        if view:
            break
    
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    
    else:
        response = HttpResponseRedirect("/")
    return response


