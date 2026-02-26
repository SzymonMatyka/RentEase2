from django.contrib import admin
from .models import Offer
from .models import Photo
from .models import TenantUser
from .models import LandlordUser

admin.site.register(Offer)
admin.site.register(Photo)
admin.site.register(TenantUser)
admin.site.register(LandlordUser)
# Register your models here.
