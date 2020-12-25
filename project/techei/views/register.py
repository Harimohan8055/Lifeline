from django.shortcuts import redirect, render
from django.views.generic import TemplateView,CreateView
from django.contrib.auth import login
from django.db.models import Prefetch
from ..models import User,IndividualProfile,EventModel,EventImage,InstitutionProfile
from django.urls import reverse_lazy


class SignUpView(TemplateView):
    template_name = 'individual/signup.html'

class LoginView(TemplateView):
    template_name = 'individual/login.html'

def HomeView(request):
    if request.user.is_authenticated and request.user.is_individual:
        uid=request.user.id
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
        return render(request, "home.html",{'eimg':eimg, 'event':event, 'inst':inst,'upcoming':upcoming,'ueimg':ueimg,'einst':einst})

    if request.user.is_authenticated == False:
        upcoming = EventModel.objects.all().order_by('start_date')
        ueimg=[]
        einst=[]
        for eve in upcoming:
            uei=EventImage.objects.filter(event_id=eve.id)
            eins=InstitutionProfile.objects.filter(user_id=eve.user_id)
            if len(einst)>0:
                for a in einst:
                    if a[0].id!=eins[0].id:
                        einst.append(eins)
            else:
                einst.append(eins)
            print(uei[1].name)
            ueimg.append(uei)
            return render(request, "home.html",{'upcoming':upcoming,'ueimg':ueimg,'einst':einst})

    elif request.user.is_authenticated and request.user.is_institution:
        return render(request, "home.html")

    else:
        return render(request, "home.html")
