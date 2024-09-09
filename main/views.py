from django.shortcuts import render

def show_main(request):
    context = {
        'project_name': 'Loom and Harvest',
        'app_name': 'main',
        'developer_name': 'Alano Davin Mandagi Awuy',
        'class_name': 'KKI'
    }
    return render(request, 'main.html', context)
