from django.http import HttpResponse,JsonResponse

def hello_world(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})
