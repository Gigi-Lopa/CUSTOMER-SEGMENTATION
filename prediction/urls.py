from django.urls import path
import prediction.views as vs

urlpatterns = [
    path("", vs.render_login),
    path("home/", vs.render_home),
    path("predict/csv/", vs.render_results),
    path("create/account/", vs.render_createAccount),
    path("user/login/", vs.loginUser),
    path("create/343/account/", vs.createAccount)
]