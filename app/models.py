from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import os
import PyPDF2, io
from django.utils.text import slugify
from hashid_field import HashidField, HashidAutoField


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
	JILID = (
			('Ya', 'ya'),
			('Tidak', 'tidak'),
		)
	pengguna 				= models.ForeignKey(User, on_delete=models.CASCADE)
	print_id				= models.ForeignKey(Print, on_delete=models.CASCADE)
	jilid					= models.CharField(max_length=255, default='Ya')
	status_id				= models.ForeignKey(Status, on_delete=models.CASCADE, default='1')
	created_at				= models.DateTimeField(auto_now_add=True)
	update_at 				= models.DateTimeField(auto_now=True)
	waktu_pengambilan 		= models.DateField()
	pengambilan_id 			= models.ForeignKey(Pengambilan, on_delete=models.CASCADE)
	copy 					= models.IntegerField(default=1)
	harga_bayar				= models.FloatField(default=0)
	status_bayar 			= models.CharField(max_length=255, choices=STATUS, default='Belum Dibayar')
	bukti 					= models.ImageField(upload_to='documents/', null=True, blank=True)
	slug  					= models.SlugField(max_length=255, null=True, blank=True)
	keterangan 				= models.CharField(max_length=255, null=True, blank=True)

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
		self.slug = slugify(self.created_at)
		super(Pemesanan, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('app-detail',
		 kwargs={'pk':self.pk})




class FilePemesanan(models.Model):
	pemesanan_id 	= models.ForeignKey(Pemesanan, on_delete = models.CASCADE)
	file 		 	= models.FileField()
	nama_file 		= models.CharField(max_length=255, null=True, blank=True)
	banyak_halaman	= models.IntegerField(default=0, null=True, blank=True)
	harga 			= models.FloatField(default=0)


	def filename(self):
		self.nama_file = os.path.basename(self.file.name)
		return self.nama_file

	# def get_absolute_url(self):
	# 	return reverse('app-detail',
	# 	 kwargs={'pk':self.pemesanan_id.id})

	def save(self, *args, **kwargs):
		base_dir =settings.MEDIA_ROOT    
		# my_file = os.path.join(base_dir, str(self.file))
		pdf = PyPDF2.PdfFileReader(self.file)
		self.banyak_halaman = pdf.getNumPages()
		self.harga = self.banyak_halaman * self.pemesanan_id.print_id.harga


		super(FilePemesanan, self).save(*args, **kwargs)

	def __str__(self):
		return "ID {}. {}, {}. ".format(self.id, 'Pemesanan ID : ', self.pemesanan_id)

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
		



