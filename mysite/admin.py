from django.contrib import admin
from .models import ips,contacted, IPData, CountryData, Hashes

admin.site.register(ips)
admin.site.register(contacted)
admin.site.register(IPData)
admin.site.register(CountryData)
admin.site.register(Hashes)