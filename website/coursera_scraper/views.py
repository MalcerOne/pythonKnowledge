from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def category(request):
    return render(request, 'category.html', {})

# def get_category(request):
#     if request.method == 'POST':
#         form = CategoryForm()
#         if form.is_valid():
#             form.save()
#             return render(request, 'index.html', {})
#     else:
#         form = CategoryForm()
#     return render(request, 'index.html', {'form': form})

# def cookies_test(request):
#     template_name = 'cookies.html'
#     current_name = "Rigatoni"  # default name
#     if request.method == 'GET':
#         if 'name' in request.COOKIES:
#             current_name = request.COOKIES['name']
#     elif request.method == 'POST':
#         current_name = request.POST.get('name')
#     response = render(request, 'test.html', {
#         "current_name": current_name
#     })
#     response.set_cookie('name', current_name)
#     return response