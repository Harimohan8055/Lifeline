from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.views.generic import TemplateView,ListView, CreateView, UpdateView
from django.http import HttpResponse
from ..models import User,IndividualProfile,InstitutionProfile,City,State,EventModel,ApplyEventModel,FestClubModel,FestImage,EventImage,SeatsEventModel
from django.urls import reverse_lazy
from ..forms import InstitutionProfileForm,InstitutionSignUpForm,AddEventForm,AddFestClubForm,FestImageForm,EventImageForm,SeatsEventForm

# Create your views here.

class InstitutionSignUpView(CreateView):
    model = User
    form_class = InstitutionSignUpForm
    template_name = 'institution/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Institution'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/institution_profile')


def InstitutionProfileView(request):
    if request.method == "POST":
        form=InstitutionProfileForm(request.POST)
        if form.is_valid() :
            profile = form.save(commit = False)
            profile.user_id=request.user.id
            profile.save()
            return redirect('/')

    else:
        form = InstitutionProfileForm()
    return render(request, "institution/profile.html",{"form":form})

def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'individual/city_drop_list.html', {'cities': cities})


def InstitutionDashboardView(request):
    return HttpResponse('<h1>Institution</h1>')


class EventType(TemplateView):
    template_name = 'institution/event_type.html'


def AddEvent(request, type):
    uid=request.user.id
    fe=FestClubModel.objects.filter(user_id=uid)
    print("hiii")
    if request.method == "POST":
        form=AddEventForm(request.POST)
        sform=SeatsEventForm(request.POST)
        if form.is_valid() :
            event = form.save(commit = False)
            event.user_id=request.user.id
            event.event_type=type
            event.save()
            request.session['event_id'] = event.id
            if sform.is_valid():
                seat=sform.save(commit = False)
                seat.event_id=event.id
                seat.total_seats=event.seats
                seat.available_seats=event.seats
                seat.user_id=request.user.id
                seat.save()
                return redirect('/techei/eventimage/')
        else:
            print(form.errors)
            print(sform.errors)
    else:
        form = AddEventForm()
        sform=SeatsEventForm()
    return render(request, "institution/addevent.html",{"form":form,"sform":sform ,"type":type,"fest":fe})



def AddFestClubView(request):
    uid=request.user.id
    feimg=FestImage.objects.filter(user_id=uid)
    if request.method == "POST":
        form=AddFestClubForm(request.POST)
        if form.is_valid() :
            fest = form.save(commit = False)
            fest.user_id=request.user.id
            fest.save()
            request.session['fest_id'] = fest.id
            return redirect('/techei/festimage/')
    else:
        form = AddFestClubForm()
    return render(request, "institution/addfestclub.html",{"form":form, "fim":feimg})


def FestImageView(request):
    fid=request.session.get('fest_id')
    fimg = FestImage.objects.filter(fest_id=fid)
    if request.method == "POST":
        form=FestImageForm(request.POST,  request.FILES)
        if form.is_valid() :
            count = FestImage.objects.filter(fest_id=fid).count()
            if count<1:
                festimg = form.save(commit = False)
                festimg.user_id=request.user.id
                festimg.fest_id=request.session.get('fest_id')
                festimg.save()
                return redirect('/techei/festimage/')
            else:
                return redirect('/techei/festimage/')
    else:
        form = FestImageForm()
    return render(request, "institution/fest_image.html",{"form":form,'fest_images' : fimg})


def EventImageView(request):
    eid=request.session.get('event_id')
    eimg = EventImage.objects.filter(event_id=eid)
    if request.method == "POST":
        form=EventImageForm(request.POST,  request.FILES)
        if form.is_valid() :
            count = EventImage.objects.filter(event_id=eid).count()
            if count<3:
                eventimg = form.save(commit = False)
                eventimg.user_id=request.user.id
                eventimg.event_id=request.session.get('event_id')
                eventimg.save()
                return redirect('/techei/eventimage/')
            else:
                return redirect('/techei/eventimage/')
    else:
        form = FestImageForm()
    return render(request, "institution/add_event_image.html",{"form":form,'event_images' : eimg})

def ResponseView(request):
    uid=request.user.id
    fes=FestClubModel.objects.filter(user_id=uid)
    ineve=EventModel.objects.filter(user_id=uid)
    ureg=[]
    for ine in ineve:
        uapp=ApplyEventModel.objects.filter(event_id=ine.id)
        ureg.append(uapp)
    return render(request, "institution/response.html",{"fest":fes,"ureg":ureg})


def FestDetails(request,fest_id):
    fesdetail=FestClubModel.objects.get(id=fest_id)
    return render(request, "institution/festdetail.html",{"fest":fesdetail})
