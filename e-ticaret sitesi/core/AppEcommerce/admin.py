from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

# Register your models here.


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ("user", "brand", "model", "description", 
                    "price", "gender", "color", "case_shape", 
                    "strap_type", "glass_feature", "style", "mechanism")
    
    search_fields = ("brand__brand", "gender__gender", 
                     "color__color", "case_shape__case_shape", 
                     "strap_type__strap_type", "glass_feature__glass_feature", 
                     "style__style", "mechanism__mechanism")
    
    list_filter = ("gender", "brand", "color")
    
    fieldsets = (
                 ("Kullanıcı Bilgileri", {"fields": ("user",)}),
                 ("Marka ve Model", {"fields": ("brand", "model")}),
                 ("Açıklama", {"fields": ("description",)}),
                 ("Fiyat", {"fields": ("price",)}),
                 ("Cinsiyet", {"fields": ("gender",)}),
                 ("Diğer Özellikler", {"fields": ("color", "case_shape", "strap_type", "glass_feature", "style", "mechanism", "image")}),

    )
    
    ordering = ("-price",)
    
    





@admin.register(Brand)
class BrandAdmin(TranslationAdmin):
    list_display = ("brand",)
    search_fields = ("brand",)
    list_filter = ("brand",)
    
    fieldsets = (
                 ("Marka", {"fields": ("brand",)}),
                 ("Resim", {"fields": ("image",)}),
    )

    ordering = ("brand",)
    readonly_fields = ("image",)






@admin.register(Gender)
class GenderAdmin(TranslationAdmin):
    list_display = ("gender",)
    search_fields = ("gender",)
    list_filter = ("gender",)
    
    fieldsets = (
                 ("Cinsiyet", {"fields": ("gender",)}),
    )
    
    ordering = ("-gender",)
    





@admin.register(Color)
class ColorAdmin(TranslationAdmin):
    list_display = ("color",)
    search_fields = ("color",)
    list_filter = ("color",)
    
    fieldsets = (
                 ("Renk", {"fields": ("color",)}),
    )
    
    ordering = ("color",)






@admin.register(CaseShape)
class CaseShapeAdmin(TranslationAdmin):
    list_display = ("case_shape",)
    search_fields = ("case_shape",)
    list_filter = ("case_shape",)
    
    fieldsets = (
                 ("Kasa Şekli", {"fields": ("case_shape",)}),
    )
    
    ordering = ("-case_shape",)






@admin.register(StrapType)
class StrapTypeAdmin(TranslationAdmin):
    list_display = ("strap_type",)
    search_fields = ("strap_type",)
    list_filter = ("strap_type",)
    
    fieldsets = (
                 ("Kayış Tipi", {"fields": ("strap_type",)}),
    )
    
    ordering = ("-strap_type",)






@admin.register(GlassFeature)
class GlassFeatureAdmin(TranslationAdmin):
    list_display = ("glass_feature",)
    search_fields = ("glass_feature",)
    list_filter = ("glass_feature",)
    
    fieldsets = (
                 ("Cam Özellik", {"fields": ("glass_feature",)}),
    )
    
    ordering = ("glass_feature",)






@admin.register(Style)
class StyleAdmin(TranslationAdmin):
    list_display = ("style",)
    search_fields = ("style",)
    list_filter = ("style",)
    
    fieldsets = (
                 ("Tarz", {"fields": ("style",)}),
    )
    
    ordering = ("style",)






@admin.register(Mechanism)
class MechanismAdmin(TranslationAdmin):
    list_display = ("mechanism",)
    search_fields = ("mechanism",)
    list_filter = ("mechanism",)
    
    fieldsets = (
                 ("Mekanizma", {"fields": ("mechanism",)}),
    )
    
    ordering = ("mechanism",)






class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "attempts", "last_attempt", "locked_until")
    search_fields = ("user__username", "user__email")
    list_filter = ("user",)
    
    fieldsets = (
                 ("Kullanıcı Bilgileri", {"fields": ("user",)}),
                 ("Giriş Detayları", {"fields": ("attempts", "last_attempt", "locked_until")}),
    )
    
    ordering = ("-last_attempt",)
    readonly_fields = ("attempts",)






class BasketProductAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity")
    search_fields = ("user__username", "user__email", "product__brand__brand")
    list_filter = ("user",)

    fieldsets = (
                 ("Kullanıcı Bilgileri", {"fields": ("user",)}),
                 ("Ürünler", {"fields": ("product",)}),
                 ("Miktar", {"fields": ("quantity",)}),
    )

    ordering = ("-quantity",)
    readonly_fields = ("quantity",)






class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "birthdate")
    search_fields = ("user__username", "user__email")
    list_filter = ("user",)

    fieldsets = (
                 ("Kullanıcı Bilgileri", {"fields": ("user",)}),
                 ("Telefon No", {"fields": ("phone_number",)}),
                 ("Doğum Tarihi", {"fields": ("birthdate",)}),
    )

    ordering = ("user",)
    readonly_fields = ("phone_number", "birthdate")






class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "province", "district", "neighbourhood")
    search_fields = ("user__username", "province")
    list_filter = ("user", "province", "district")

    fieldsets = (
                 ("Kullanıcı Bilgileri", {"fields": ("user",)}),
                 ("Adres", {"fields": ("address",)}),
                 ("İl", {"fields": ("province",)}),
                 ("İlçe", {"fields": ("district",)}),
                 ("Mahalle", {"fields": ("neighbourhood",)}),
    )

    ordering = ("-province",)
    readonly_fields = ("province", "district", "neighbourhood")






class FavorilerAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    search_fields = ("user__username", "user__email")
    list_filter = ("user", "product")

    fieldsets = (
                 ("Kullanıcı Bilgileri", {"fields": ("user",)}),
                 ("Ürün", {"fields": ("product",)}),
    )






class YorumlarAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "product", "created_date", "comment")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    list_filter = ("user", "first_name", "last_name")

    fieldsets = (
                 ("Kullanıcı Bilgileri", {"fields": ("user",)}),
                 ("Ad Soyad", {"fields": ("first_name", "last_name")}),
                 ("Ürün", {"fields": ("product",)}),
                 ("Yorum", {"fields": ("comment",)}),
    )

    ordering = ("-created_date",)
    




admin.site.register(BasketProduct, BasketProductAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Favoriler, FavorilerAdmin)
admin.site.register(Yorumlar, YorumlarAdmin)
admin.site.register(LoginAttempt, LoginAttemptAdmin)





