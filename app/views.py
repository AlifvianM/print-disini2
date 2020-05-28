from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Pemesanan, CheckOut
from .forms import PemesananForm, CheckOutForm, PemesananUpdateForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404

from django.views.generic import FormView

from django.contrib.auth.decorators import login_required

import PyPDF2, io

# Create your views here.

@login_required
def UserPost(request):
    user_post = Pemesanan.objects.filter(pengguna = request.user).order_by('-created_at')
    template = 'app/list.html'
    return render(request, template, {
                'pemesanans':user_post
            }
        )

class Home(TemplateView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = "users/index.html"


class PemesananListView(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = Pemesanan
    template_name = "app/list.html"
    context_object_name = 'pemesanans'
    ordering_by = ['-created_at']
    # queryset = Pemesanan.objects.filter(pengguna = user)

    def get_queryset(self):
        my_post = Pemesanan.objects.filter(pengguna = self.request.user)
        return super().get_queryset()

class PemesananCreateView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    # model = Pemesanan
    form_class = PemesananForm
    template_name = "app/create.html"



    def form_valid(self, form):
    	form.instance.pengguna = self.request.user
    	return super().form_valid(form)	


class PemesananUpdateView(UpdateView):
    model = Pemesanan
    template_name = 'app/bayar.html'
    form_class = PemesananUpdateForm


    def get_success_url(self, **kwargs):
        return reverse('app-detail', kwargs={'pk':self.object.id})

    def test_func(self):
        pemesanan = self.get_object()
        if self.request.user == pemesanan.pengguna:
            return True
        return False

class PemesananDeleteView(DeleteView):
    model = Pemesanan
    template_name = "app/delete.html"
    success_url = '/home'

    

    def test_func(self):
        pemesanan = self.get_object()
        if self.request.user == pemesanan.pengguna:
            return True
        return False


class PemesananDetailView(DetailView, LoginRequiredMixin, UserPassesTestMixin):
    model = Pemesanan
    template_name = "app/detail.html"
    queryset = Pemesanan.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     obj = Pemesanan.objects.get(id=self.kwargs['pk'])
    #     # print(obj.file)
    #     pdf = PyPDF2.PdfFileReader(obj.file.path)
    #     info = pdf.getNumPages()
    #     # print(info)



    #     total = info * 10
    #     # print(total)

    #     context['total'] = total

    #     return context

    def get_object(self):
        obj = super().get_object()
        print(obj.file.path)
        print(obj.banyak_halaman)
        hal = obj.banyak_halaman
        print(hal*obj.harga_bayar)
        pdf = PyPDF2.PdfFileReader(obj.file.path)
        info = pdf.getNumPages()
        obj.banyak_halaman = info
        # obj.save()
        obj.harga_bayar = (obj.banyak_halaman * obj.print_id.harga * obj.copy) + obj.jilid_id.harga_jilid
        print(obj.harga_bayar)

        if obj.bukti:
            obj.status_bayar = 'Menunggu Konfirmasi Admin'
        else:
            pass

        obj.save()

        return obj

    def get_context_data(self, **kwargs):
        context = super(PemesananDetailView, self).get_context_data(**kwargs)
        # context['comments'] = Comment.objects.filter(post=self.object)
        context['form'] = CheckOutForm
        return context

class FormCheckOut(CreateView):
    form_class = CheckOutForm
    
    def get_success_url(self, **kwargs):
        # return reverse('app-detail', kwargs={'pk':self.object.pemesanan_id.id})
        return reverse('app-list')

    


def PemesananDetail(request, pk):
    post = get_object_or_404(Pemesanan, pk = pk)
    return render(request, "app/detail.html", {'object':post})


class CreateCheckOut(CreateView):
    model = CheckOut
    template_name = 'app/checkout.html'
    form_class = CheckOutForm
   
    

class CheckDetailView(DetailView):
    model = CheckOut
    template_name = 'app/detailCheck.html'

    def get_object(self):
        obj = super().get_object()
        print('status : ',obj.status_bayar)
        obj.status_bayar = 'Telah Dibayar'
        obj.save()

        return obj