from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductCreateForm, ImageCreateForm
from .models import Product


def home(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'shop/index.html', context)


class HomeListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    ordering = ['-list_date']


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    ordering = ['-list_date']
    paginate_by = 3


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "shop/product_form.html"
    fields = ['product_name', 'product_description', 'product_price', 'product_image', 'product_rating']

    # def get(self, request, *args, **kwargs):
    #     p_form = ProductCreateForm()
    #     i_form = ImageCreateForm()
    #     context = {'form1': p_form, 'form2': i_form}
    #     return render(request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
    #     p_form = ProductCreateForm(request.POST)
    #     i_form = ImageCreateForm(request.POST, request.FILES)
    #     if p_form.is_valid() and i_form.is_valid():
    #         p_form.instance.product_seller = self.request.user
    #         p_form.save()
    #         i_form.save()
    #         messages.success(request, f'Product has been Created!')
    #         return redirect('product-detail')
    #
    #     context = {'form1': p_form, 'form2': i_form}
    #     return render(request, self.template_name, context)
    #
    def form_valid(self, form):
        form.instance.product_seller = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['product_name', 'product_description', 'product_price', 'product_rating']

    def form_valid(self, form):
        form.instance.product_seller = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.product_seller:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.product_seller:
            return True
        return False


def about(request):
    return render(request, 'shop/about.html')
