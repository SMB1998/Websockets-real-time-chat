from django.contrib import admin
from .models import Requests

class RequestsAdmin(admin.ModelAdmin):
    readonly_fields =('orden_de_compra',)
    list_display = ('referencia', 'nombre', 'status')  # Campos a mostrar en la lista de registros
    list_filter = ('status',)  # Filtro por el campo 'status'
    search_fields = ('nombre', 'referencia')  # Campos por los cuales se puede buscar
    
    def orden_de_compra(self, obj):
        return obj.get_custom_id()

admin.site.register(Requests, RequestsAdmin)
