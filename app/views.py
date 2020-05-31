from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.db.models import Avg, Sum

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Pemesanan, CheckOut, FilePemesanan
from .forms import PemesananForm, CheckOutForm, PemesananUpdateForm, FilePemesananForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect

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

    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     files = request.FILES.getlist('file')
    #     if form.is_valid():
    #         for f in files:
    #             pdf = PyPDF2.PdfFileReader(obj.file.path)
    #             print(pdf)
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

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
    model = FilePemesanan
    template_name = "app/detail.html"
    # queryset = Pemesanan.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pesans']=FilePemesanan.objects.filter(pemesanan_id=self.kwargs['pk'])
        context['setors']=Pemesanan.objects.filter(id=self.kwargs['pk'])
        obj = super(PemesananDetailView, self).get_object(queryset = context['setors'])
        print(obj)
        if obj.jilid == 'Ya':
            total = FilePemesanan.objects.filter(pemesanan_id=self.kwargs['pk']).aggregate(Sum('harga'))['harga__sum'] or 0.00
            context['total'] = total + 3000
            obj.harga_bayar = context['total']
            obj.save()
        else:
            context['total'] = FilePemesanan.objects.filter(pemesanan_id=self.kwargs['pk']).aggregate(Sum('harga'))['harga__sum'] or 0.00  
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







def create_to_feed(request,*args, **kwargs):
    # user = request.user
    if request.method == 'POST':
        form = PemesananForm(request.POST)
        file_form = FilePemesananForm(request.POST, request.FILES)
        files = request.FILES.getlist('file') #field name in model
        if form.is_valid() and file_form.is_valid():
            feed_instance = form.save(commit=False)
            feed_instance.pengguna_id = request.user.id
            feed_instance.save()
            for f in files:
                file_instance = FilePemesanan(file=f, pemesanan_id=feed_instance)
                file_instance.save()
            return redirect(reverse('app-detail',kwargs = {'pk': file_instance.pemesanan_id.id}))
    else:
        form = PemesananForm()
        file_form = FilePemesananForm()

    context = {
        'form':form,
        'file_forms': file_form,
    }
    return render(request, 'app/create.html', context)







