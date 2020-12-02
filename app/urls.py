from django.urls import path
# current directory
from . import views
from django.conf.urls import url



urlpatterns = [

    url(r'^$', views.index, name="index"),
    url(r'^add_results/', views.add_results, name="add_results"),
    url(r'^validate_email/', views.validate_email, name="validate_email"),
    url(r'^admin/', views.admin_home, name="admin_home"),
    url(r'^ttn/', views.ttn, name="ttn"),
    path(r'^<id>/delete_ttn_no/', views.delete_ttn_no, name="delete_ttn_no"),
    path(r'^<id>/delete_test_result/', views.delete_test_result, name="delete_test_result"),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^adminLogin/', views.admin_login, name="admin_login"),
    url(r'^get_results/', views.get_results, name="get_results"),
    url(r'^get_positive_by_age/', views.get_positive_by_age, name="get_positive_by_age"),
    url(r'^get_infection_by_age/', views.get_infection_by_age, name="get_infection_by_age"),
    url(r'^get_infection_by_postcode/', views.get_infection_by_postcode, name="get_infection_by_postcode"),
    url(r'^get_positive_by_postcode/', views.get_positive_by_postcode, name="get_positive_by_postcode"),
    url(r'^test_results/', views.test_results, name="test_results"),



]