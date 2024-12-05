from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class Brand(models.Model):
    brand = models.CharField(max_length=250)
    image = models.ImageField(upload_to="Brand Image")

    def __str__(self):
        return self.brand
    
    class Meta:
        verbose_name_plural = "Markalar"                




class Gender(models.Model):
    gender = models.CharField(max_length=250)

    def __str__(self):
        return self.gender
    
    class Meta:
        verbose_name_plural = "Cinsiyetler"                         




class Color(models.Model):
    color = models.CharField(max_length=250)

    def __str__(self):
        return self.color
    
    class Meta:
        verbose_name_plural = "Renkler"




class CaseShape(models.Model):
    case_shape = models.CharField(max_length=250)

    def __str__(self):
        return self.case_shape
    
    class Meta:
        verbose_name_plural = "Kasa Şekilleri"




class StrapType(models.Model):
    strap_type = models.CharField(max_length=250)

    def __str__(self):
        return self.strap_type
    
    class Meta:
        verbose_name_plural = "Kayış Tipleri"




class GlassFeature(models.Model):
    glass_feature = models.CharField(max_length=250)

    def __str__(self):
        return self.glass_feature
    
    class Meta:
        verbose_name_plural = "Cam Özellikleri"




class Style(models.Model):
    style = models.CharField(max_length=250)

    def __str__(self):
        return self.style
    
    class Meta:
        verbose_name_plural = "Tarzlar"




class Mechanism(models.Model):
    mechanism = models.CharField(max_length=250)

    def __str__(self):
        return self.mechanism
    
    class Meta:
        verbose_name_plural = "Mekanizmalar"




class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to="Product Image")
    price = models.FloatField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    case_shape = models.ForeignKey(CaseShape, on_delete=models.CASCADE) # Kasa Şekli
    strap_type = models.ForeignKey(StrapType, on_delete=models.CASCADE) # Kayış Tipi
    glass_feature = models.ForeignKey(GlassFeature, on_delete=models.CASCADE) # Cam Özelliği
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    mechanism = models.ForeignKey(Mechanism, on_delete=models.CASCADE)

    def __str__(self):
        return self.model
    
    class Meta:
        verbose_name_plural = "Ürünler"




class BasketProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.model
    
    class Meta:
        verbose_name_plural = "Sepetteki Ürünler"
        unique_together = ("user", "product")




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Profiller"         




class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    province = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    neighbourhood = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Adresler"




class Favoriler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Favoriler"




class Yorumlar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Yorumlar"




class LoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(default=now)
    locked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Son Login Girişimleri"




