from django.shortcuts import render


def HomeView(request):
    template_name = 'vk_app/index.html'
    return render(request, template_name, {})
