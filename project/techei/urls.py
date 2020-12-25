from django.urls import path
from techei.views import register,institution,individual

urlpatterns =[
    path('eventtype', institution.EventType.as_view(), name='event_type'),
    path('addevent/<int:type>/', institution.AddEvent, name='add_event'),
    path('addfest/', institution.AddFestClubView, name='add_fest'),
    path('festimage/',institution.FestImageView, name='add_fest_image'),
    path('eventimage/',institution.EventImageView, name='add_event_image'),
    path('apply/<int:event_id>/', individual.ApplyEvent, name='apply_event'),
    path('response/',institution.ResponseView, name='response'),
    path('enrolledevents/',individual.EnrolledView, name='enrolled_events'),
    path('explore/',individual.ExploreView, name='explore'),
    path('festdetails/<int:fest_id>/', institution.FestDetails, name='festdetails'),
]
