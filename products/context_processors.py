from .models import Category

def categories(request):
    return {
        "categories_for_header": Category.objects.all()[0:5],
        "categories_for_featured": Category.objects.all()[0:3],
    }