def show_navbar(request):
    show_navbar = request.user.is_authenticated
    return {'show_navbar': show_navbar}