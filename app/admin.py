from django.contrib import admin
from .models import Print, Jilid, Pemesanan, Pengambilan, Status, CheckOut
# Register your models here.


class PemesananModelAdmin(admin.ModelAdmin):
	list_display = (
			'nama_file',
			'file',
			'print_id',
			'jilid_id',
			'status_id',
			'created_at',
			'waktu_pengambilan',
			'pengambilan_id',
			'banyak_halaman',
			'copy',
			'harga_bayar',
			'status_bayar',
			'bukti',
			'pengguna',
		)



admin.site.register(Print)
admin.site.register(Jilid)
admin.site.register(Pemesanan, PemesananModelAdmin)
admin.site.register(Pengambilan)
admin.site.register(Status)
admin.site.register(CheckOut)
