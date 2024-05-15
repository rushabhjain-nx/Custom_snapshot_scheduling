from django.urls import path
from . import views
urlpatterns = [
   
    path('pc/',views.index,name='index'),
    path('snapshot-schedules/', views.snapshot_schedule_list, name='snapshot_schedule_list'),
    path('snapshot-schedules/<int:schedule_id>/delete/', views.delete_snapshot_schedule, name='delete_snapshot_schedule'),
    path('process_form/', views.process_form, name='process_form'),
    path('pe_creds/', views.pe_creds, name='pe_creds'),
    path('', views.home, name='home'),
    path('process_pe/', views.process_pe, name='process_pe'),
    path('display_vms/', views.display_vms, name='display_vms'),
    path('submit_vms/', views.submit_vms, name='submit_vms'),
    path('save_ss/', views.save_ss, name='save_ss'),
    path('past_snapshots/', views.past_snapshots, name='past_snapshots'),
    path('past_snapshots/<int:schedule_id>/delete/', views.delete_past_schedule, name='delete_past_schedule'),

]