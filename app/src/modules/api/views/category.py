from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_GET
from django.shortcuts import render

from ..models import Category


@require_GET
def catalog(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.prefetch_related("product_set").all()
    context = {"categories": categories}
    return render(request, "api/product/catalog.html", context)


@require_GET
def category_detail(request: HttpRequest, category_id: int) -> HttpResponse:
    try:
        category = Category.objects.get(id=category_id)
        context = {"category": category}
        return render(request, "api/product/category.html", context)
    except Category.DoesNotExist:
        return HttpResponseNotFound("Category not found")
