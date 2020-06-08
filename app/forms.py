from django import forms
from .models import Pemesanan, CheckOut, Print, Jilid, Pengambilan, Status, FilePemesanan

class PemesananForm(forms.ModelForm):
    # nama_file = forms.CharField(
    #         widget= forms.TextInput(
    #                 attrs = {
    #                     'class' : 'form-control'
    #                 }
    #             )
    #     )

    file = forms.FileField(
            widget=forms.ClearableFileInput(
                    attrs = {
                        'multiple': True,
                        'class' : '',
                        'type'  : 'file',
                        'onchange' : 'document.getElementById("prepend-small-btn").value = files[0].name;',
                    }
                )   
        )

    JILID = (
            ('Ya', 'ya'),
            ('Tidak', 'tidak'),
        )

    print_id = forms.ModelChoiceField(queryset=Print.objects.all(), 
            widget=forms.Select(
                    attrs = {
                        'class' : 'form-control',
                    }
                ), label='Jenis Cetak'   
        )

    jilid   = forms.ChoiceField(choices=JILID,
            widget=forms.Select(
                    attrs = {
                        'class' : 'form-control',
                    }
                ), label='Jilid'
        )

    waktu_pengambilan = forms.DateField(
            widget = forms.TextInput(
                    attrs = {
                    'type':'date',
                    'class': 'form-control'
                    }
                )
        )

    pengambilan_id = forms.ModelChoiceField(queryset=Pengambilan.objects.all(), 
            widget=forms.Select(
                    attrs = {
                        'class' : 'form-control',
                    }
                ), label='Lokasi Pengambilan'   
        )

    copy = forms.IntegerField(
            widget=forms.NumberInput(
                    attrs={
                        'class' : 'form-control',
                        'value' : 1
                    }
                )
        )
    keterangan = forms.CharField(
            widget= forms.TextInput(
                    attrs = {
                        'class' : 'form-control'
                    }
                )
        )
    # status_id = forms.ModelChoiceField(queryset=Status.objects.all(), 
    #         widget=forms.Select(
    #                 attrs = {
    #                     'class' : 'form-control',
    #                 }
    #             )   
    #     )

    class Meta:
        model = Pemesanan
        fields = (
            # 'nama_file',
        	# 'file',
        	'print_id',
            'jilid',
        	'waktu_pengambilan',
        	'pengambilan_id',
            'copy',
        	# 'harga_bayar',
        	# 'status_id',
            'keterangan',
        	)

class PemesananUpdateForm(forms.ModelForm):
    bukti = forms.ImageField(
            widget=forms.FileInput(
                    attrs = {
                        'class' : 'form-control col-md-6',
                        'type'  : 'file',
                        'onchange' : 'document.getElementById("prepend-small-btn").value = files[0].name;',
                    }
                )   
        )
    class Meta:
        model = Pemesanan
        fields = (
            'bukti',
            )
    

class FilePemesananForm(forms.ModelForm):
    class Meta:
        model = FilePemesanan
        fields = (
            'file',
            )
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }
    




class CheckOutForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = (
            # 'pemesanan_id',
            'bukti',
            )
    