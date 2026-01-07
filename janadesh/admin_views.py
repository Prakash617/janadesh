from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def filehub_embed(request):
    return render(request, "filehub_embed.html")


# from django.shortcuts import redirect

# def filehub_embed(request):
#     # Redirect or embed FileHub in iframe
#     return redirect("/filehub/")  # or render iframe template