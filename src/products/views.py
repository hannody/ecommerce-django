from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404


from .models import Product


class ProductFeaturedListView(ListView):

    teampalte_name  = "products/product_list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()

class ProductFeaturedDetailView(DetailView):

    teampalte_name  = "products/featured-detail.html"

    def get_context_data(self, *args, **kwargs):
        return Product.objects.featured()


class ProductListView(ListView):

    teampalte_name  = "products/product_list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


class ProductDetailView(DetailView):

    teampalte_name  = "products/detail.html"

    def get_context_data(self, *args, **kwargs):

        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        #print(context)
        return context

    def get_queryset(self, *args, **kwargs):
        #this function is replacing the det_object()..
        request = self.request

        pk      = self.kwargs.get('pk')

        instance = Product.objects.get_by_id(pk)

        if instance is None:
            raise Http404("Product does not exist!")

        return Product.objects.filter(pk=pk)







