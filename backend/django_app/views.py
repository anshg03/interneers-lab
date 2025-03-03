from django.http import HttpResponse,JsonResponse
import re

def error(message,status=400):
    return JsonResponse({"error":message},status=status)

def success(message,status=200):
    return JsonResponse({"message":message},status=status)


def hello_world(request):
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    #our name is only going to support letters with siz less than 10 and not empty
    if len(name) >=10:
        return error("Invalid name. Length must be less than 10.")
    
    if not re.match(r"^[A-Za-z]+$", name):
        return error("Invalid name. Only letters are allowed.")

    return success( f"Hello, {name}!")
