from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import os
import PyPDF2, io


# Create your models here.

class Print(models.Model):
	jenis_print 	= models.CharField(max_length=50)
	harga 			= models.FloatField()

	def __str__(self):
	   	return "{}, harga {}.".format(self.jenis_print, self.harga)

class Jilid(models.Model):
	jilid 			= models.CharField(max_length=50)
	harga_jilid 	= models.FloatField()

	def __str__(self):
		return "{} (harga + {})".format(self.jilid, self.harga_jilid)

class Pengambilan(models.Model):
	tempat_pengambilan 	= models.CharField(max_length=50)

	def __str__(self):
		return "{}".format(self.tempat_pengambilan)

class Status(models.Model):
	STATUS = (
			('Belum Di Cetak', 'belum_di_cetak'),
			('Sudah Di Cetak', 'sudah_di_cetak'),
		)
	status 		= models.CharField(max_length=50, choices=STATUS)
		
	def __str__(self):
		return self.status

class Pemesanan(models.Model):
	STATUS = (
		('Telah Dibayar' , 'dibayar'),
		('Menunggu Pembayaran' , 'menunggu'),
		('Belum Dibayar', 'belum')
	)
	pengguna 				= models.ForeignKey(User, on_delete=models.CASCADE)
	nama_file 				= models.CharField(max_length=255)
	file 					= models.FileField(upload_to='documents/')
	print_id				= models.ForeignKey(Print, on_delete=models.CASCADE)
	jilid_id 				= models.ForeignKey(Jilid, on_delete=models.CASCADE)
	status_id				= models.ForeignKey(Status, on_delete=models.CASCADE, default='1')
	created_at				= models.DateTimeField(auto_now_add=True)
	update_at 				= models.DateTimeField(auto_now=True)
	waktu_pengambilan 		= models.DateField()
	pengambilan_id 			= models.ForeignKey(Pengambilan, on_delete=models.CASCADE)
	banyak_halaman			= models.IntegerField(default=0, null=True, blank=True)
	copy 					= models.IntegerField(default=1)
	harga_bayar				= models.FloatField(default=0)
	status_bayar 			= models.CharField(max_length=255, choices=STATUS, default='Belum Dibayar')
	bukti 					= models.ImageField(upload_to='documents/', null=True, blank=True)




	def filename(self):
		return os.path.basename(value.file.name)

	def __str__(self):
		return "ID {}. {}, {}. ".format(self.id, self.pengguna, self.created_at)

	# def total(self, *args, **kwargs):
	# 	obj = Pemesanan.objects.get(id = self.kwargs['pk'])
	# 	print(obj.file.path)
	# 	# with open(obj.file.path, 'r') as f:
	# 	pdf = PyPDF2.PdfFileReader(obj.file.path)
	# 	info = pdf.getNumPages()
	# 	print(info)

	# 	self.banyak_halaman=info
	# 	obj.save()



	def save(self, *args, **kwargs):
		
		super(Pemesanan, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('app-detail',
		 kwargs={'pk':self.pk})


class CheckOut(models.Model):
	STATUS = (
		('Telah Dibayar' , 'dibayar'),
		('Menunggu Pembayaran' , 'menunggu'),
	)
	pemesanan_id 		= models.OneToOneField(Pemesanan, on_delete=models.CASCADE)
	bukti 				= models.ImageField(upload_to='documents/')
	status_bayar 		= models.CharField(max_length=255, choices=STATUS, default='Menunggu Pembayaran')


	def __str__(self):
		return "id {}, id pemb {}".format(self.id, self.pemesanan_id)

	def get_absolute_url(self):
		return reverse('app-checkout-detail',
		 kwargs={'pk':self.pk})


	def save(self, *args, **kwargs):
		self.pemesanan_id = Pemesanan.objects.latest('id')
		super(CheckOut, self).save(*args, **kwargs) 
		



