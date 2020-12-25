from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.views.generic import TemplateView,ListView, CreateView, UpdateView
from django.http import HttpResponse
from ..models import User,FestImage,FestClubModel,IndividualProfile,InstitutionProfile,City,State,EventModel,EventImage,Category,ApplyEventModel,SeatsEventModel
from django.urls import reverse_lazy
from ..forms import IndividualProfileForm,IndividualSignUpForm,ApplyEventForm,SeatsEventForm,SearchForm
import datetime


class IndividualSignUpView(CreateView):
    model = User
    form_class = IndividualSignUpForm
    template_name = 'individual/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Individual'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/individual_profile')


def IndividualProfileView(request):
    if request.method == "POST":
        form=IndividualProfileForm(request.POST)
        if form.is_valid() :
            profile = form.save(commit = False)
            profile.user_id=request.user.id
            profile.save()
            return redirect('/')

    else:
        form = IndividualProfileForm()
    return render(request, "individual/profile.html",{"form":form})

def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'individual/city_drop_list.html', {'cities': cities})


# def IndividualDashboardView(request):
#     return render(request,'individual/individual_home.html')


def ApplyEvent(request, event_id):
    uid=request.user.id
    ev_type=EventModel.objects.get(id=event_id)
    evimg=EventImage.objects.filter(event_id=event_id)
    evinst=InstitutionProfile.objects.get(user_id=ev_type.user_id)
    city=City.objects.get(id=ev_type.city_id)
    state=State.objects.get(id=ev_type.state_id)
    category=Category.objects.get(id=ev_type.category_id)
    check=ApplyEventModel.objects.filter(event_id=ev_type.id,user_id=uid)
    sev=SeatsEventModel.objects.get(event_id=event_id)
    upcoming = EventModel.objects.all().order_by('start_date')[:3]
    inst_pro = User.objects.get(id=uid)
    clen=len(check)
    print(upcoming)
    if request.method == "POST":
        form=ApplyEventForm(request.POST)
        if form.is_valid():
            apply = form.save(commit = False)
            apply.user_id=request.user.id
            apply.event_id=event_id
            if ev_type.fee == 0:
                apply.is_confirm == True
            if not check:
                apply.save()
                a=int(sev.available_seats)
                a=a-1
                sev.available_seats=a
                sev.save()
            else:
                print("error")
            #return redirect('/techei/eventimage/')
        else:
            print(form.errors)
    else:
        form = ApplyEventForm()
    return render(request, "individual/applyevent.html",{"form":form,"event_id":event_id,"evimg":evimg,"evinst":evinst,"ev_type":ev_type,"city":city,"state":state,"category":category,"sev":sev,"clen":clen,"upcoming":upcoming,"inst_pro":inst_pro})


def EnrolledView(request):
    uid=request.user.id
    today = datetime.datetime.now().date()
    eimg=[]
    print(today)
    event=ApplyEventModel.objects.filter(user_id=uid)
    for eve in event:
        uei=EventImage.objects.filter(event_id=eve.event.id)[:1]
        eimg.append(uei)
    return render(request, "individual/enrolled.html")


def ExploreView(request):
    uid=request.user.id
    if request.user.is_authenticated and request.user.is_individual:
        user_obj=IndividualProfile.objects.filter(user_id=uid)
        cid=user_obj[0].city_id
        event=EventModel.objects.filter(city_id=cid)
        upcoming = EventModel.objects.all().order_by('start_date')
        ueimg=[]
        einst=[]
        eimg=[]
        inst=[]
        for eve in upcoming:
            uei=EventImage.objects.filter(event_id=eve.id)
            eins=InstitutionProfile.objects.filter(user_id=eve.user_id)
            if len(einst)>0:
                for a in einst:
                    if a[0].id!=eins[0].id:
                        einst.append(eins)
            else:
                einst.append(eins)
            ueimg.append(uei)
        for e in event:
            ei=EventImage.objects.filter(event_id=e.id)
            ins=InstitutionProfile.objects.filter(user_id=e.user_id)
            if len(inst)>0:
                for a in inst:
                    if a[0].id!=ins[0].id:
                        inst.append(ins)
            else:
                inst.append(ins)
            eimg.append(ei)
    form=SearchForm()
    venevent=""
    festevent=""
    titlevent=""
    v=""
    f=""
    t=""
    que=""
    feimg=FestImage.objects.all()
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #now in the object cd, you have the form as a dictionary.
            que = cd.get('que')
            print(que)
            venevent=EventModel.objects.filter(venue__startswith=que)
            festevent=FestClubModel.objects.filter(name__startswith=que)
            titlevent=EventModel.objects.filter(title__startswith=que)
            v=len(venevent)
            f=len(festevent)
            t=len(titlevent)
    return render(request, "individual/explore.html",{"venevent":venevent,"festevent":festevent,"titlevent":titlevent,"vlen":v,"flen":f,"tlen":t,"que":que,"fim":feimg,'eimg':eimg, 'event':event, 'inst':inst,'upcoming':upcoming,'ueimg':ueimg,'einst':einst})
