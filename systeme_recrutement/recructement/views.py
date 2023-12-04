from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
# from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm,DemandeForm,DemandegererForm,AForm,RForm,etapesForm
from .models import Offre,demande,architect,decision,projet,architect,realisation,User,etapes


@login_required
def pagerecruteur(request):
    return render(request, 'app_recrutement/dashrecruteur.html')


def inscription(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')

        else:
            messages.error(request, form.errors)
    return render(request, 'app_recrutement/signup.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
           if  user.username=='admin1':
               return redirect('dashadmin')
           elif user.is_superuser:
                login(request, user)
                return redirect('ArchitectVerification')
           else:
                login(request, user)
                return redirect('indexclient')
        else:
             messages.error(request, "Mot de passe ou userneme incorrecte")
    return render(request, 'app_recrutement/signin.html')

def tableaubord(request):
     user = request.user
     if user is not None and user.is_active:
            if user.is_superuser:
                return redirect('indexarchitecte')
            else:
                return redirect('indexclient')
    







@login_required
def ajouter_offre(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = OffreForm(request.POST,request.FILES)
            if form.is_valid():
                offre = form.save(commit=False)
                offre.recruteur = request.user
                offre.save()
                return redirect('listes')
        else:
            form = OffreForm()
        return render(request, 'app_recrutement/ajouter_offre.html', {'form': form})

@login_required
def lister_offres(request):
    if request.user.is_authenticated:
        offres = Offre.objects.filter(recruteur_id=request.user)
        return render(request, 'app_recrutement/listes_offres.html', {'offres': offres})



@login_required
def interface_user(request):
    if request.user.is_authenticated:
        offres = Offre.objects.all()
        user = request.user
        return render(request,'app_recrutement/baseclient.html',{'offres':offres,'user':user})



def index(request):
    offres = demande.objects.all()
    return render(request, 'app_recrutement/index1.html',{'offres':offres})


def UserInstance(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'app_recrutement/baserecruteur.html', {'user': user})


@login_required
def Deconnexion(request):
    logout(request)
    return redirect('index')


@login_required
def UpdateOffre(request,id):
    offre = Offre.objects.get(id=id)
    if request.method == "POST":
        update_offre = OffreForm(request.POST,request.FILES,instance=offre)
        if update_offre.is_valid():
            update_offre.save()
            return redirect('listes')

    else:
        update_offre = OffreForm(instance=offre)
    return render(request,'app_recrutement/update_offre.html',{'update_offre':update_offre})


@login_required
def SupprimerOffre(request,id):
    offre = Offre.objects.get(id=id)
    offre.delete()
    return redirect('listes')

@login_required
def Stats(request):
    if request.user.is_authenticated:
        offres = Offre.objects.filter(recruteur_id=request.user)
        nbres_offres = len(offres)
        print(nbres_offres)
        return render(request,'app_recrutement/dashrecruteur.html',{'nbres_offres':nbres_offres})



@login_required
def pageajoutdemande(request):
    return render(request, 'app_recrutement/Ajouter_demande.html')




@login_required
def pageajoutdemande(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DemandeForm(request.POST,request.FILES)
            if form.is_valid():
                demande = form.save(commit=False)
                demande.client = request.user
                demande.etat="traitement"
                demande.save()
                return redirect('listedemandeclient')
        else:
            form = DemandeForm()
        return render(request, 'app_recrutement/Ajouter_demande.html', {'form': form})



@login_required
def indexarchitecte(request):
    demandes = demande.objects.exclude(Etat="Accepter")
    nbres_demande = len(demandes)
    context = {'demandes': demandes,'nbres_demande':nbres_demande}
    return render(request, 'app_recrutement/dasharchitecte.html',context)



def dashadmin(request):
    return render(request, 'app_recrutement/dashadmin.html')




@login_required
def Acepeterdemande(request,id):
    demandes = demande.objects.get(id=id)
    archi=request.user
    decision.objects.create(architect=archi,decisionA=1, demade=demandes)
    return redirect('indexarchitecte')

@login_required
def Refuserdemande(request,id):
    canditature = decision.objects.get(id=id)
    canditature.decisioncli=200
    return redirect('demandeindividuel')


@login_required
def demandeindividuel(request):
    if request.user.is_authenticated:
        dem=demande.objects.all()
        alldem= demande.objects.exclude(Etat="Accepter")
        demandes = decision.objects.exclude(demade__Etat="Accepter")
        
        nbres_demande = len(demandes)
        context = {'alldem': alldem,'demandes': demandes,'nbres_demande':nbres_demande,'dem':dem}
        return render(request, 'app_recrutement/historiqueprojet.html',context )  

@login_required
def gererprojet(request):
      if request.user.is_authenticated:
         projets = projet.objects.filter(architecte=request.user)
         nbres_demande = len(projets)
         context = {'projets': projets,'nbres_demande':nbres_demande}
         return render(request, 'app_recrutement/gerer_demande.html',context )
   
    
@login_required
def Decisionprojet(request):
      if request.user.is_authenticated:
         des = decision.objects.filter(architect=request.user)
         return render(request, 'app_recrutement/candidature.html', {'des': des})
   
    



@login_required
def gererprojetid(request,id):
    demand = projet.objects.get(id=id)
    if request.method == "POST":
        gerer_demande = DemandegererForm(request.POST,instance=demand)
        if gerer_demande.is_valid():
            gerer_demande.save()
            return redirect('gererprojet')

    else:
        gerer_demande =  DemandegererForm(instance=demand)


    return render(request, 'app_recrutement/gerepar_id.html',{'gerer_demande':gerer_demande})


@login_required
def statutprojetclient(request):
    if request.user.is_authenticated:
        projetcli = projet.objects.filter(demande__client=request.user)
        
        nbres_demande = len(projetcli)
        return render(request, 'app_recrutement/historiqueavancement.html',{'projetcli':projetcli,'nbres_demande':nbres_demande}) 




def appelofre(request):
    demandes =demande.objects.exclude(Etat="Accepter")
    return render(request, 'app_recrutement/appeloffre.html',{'demandes':demandes})



@login_required
def AcepterdemandeCLI(request,id):
    alldem= demande.objects.all()
    demandes = demande.objects.get(id=id)
    demand= decision.objects.filter(demade=demandes)
    if request.method == 'POST':
        candidature_id = request.POST.get('candidature_id')
        candidature = decision.objects.get(id=candidature_id)
        candidature.decisioncli=100
        candidature.save()
        demandes.Etat="Accepter"
        demandes.save()
        if candidature.decisioncli==100:
             projet.objects.create(demande=demandes,architecte=candidature.architect,date_debut="2023-01-01",date_fin="2023-01-01",statut="nouveau projet",rapport="nouveau")
             return redirect('statutprojetclient')
    
   





def listedemandeclient(request):
     if request.user.is_authenticated:
        demandes = demande.objects.filter(client=request.user).order_by('-id')
        nbres_demande = len(demandes)
        context = {'nbres_demande': nbres_demande,'demandes':demandes}
        return render(request, 'app_recrutement/listedesdemande.html',context)
    

@login_required
def SupprimerDemande(request,id):
    demandes = demande.objects.get(id=id)
    demandes.delete()
    return redirect('listedemandeclient')





@login_required
def profileA(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AForm(request.POST,request.FILES)
            if form.is_valid():
                P=form.save(commit=False)
                P.profile = request.user
                P.save()
                return redirect('indexarchitecte')
        else:
            form = AForm()
    
        return render(request, 'app_recrutement/architecteprofile.html', {'form': form})


@login_required
def voirp(request):
     if request.user.is_authenticated:
        architecte = architect.objects.get(profile=request.user)     
        return render(request, 'app_recrutement/profistatic.html',{'architecte':architecte})
    

@login_required
def Updateprofil(request,id):
    p = architect.objects.get(id=id)
    if request.method == "POST":
        update_p = AForm(request.POST,request.FILES,instance=p)
        if update_p.is_valid():
            update_p.save()
            return redirect('voirp')

    else:
        update_p = AForm(instance=p)
    return render(request,'app_recrutement/updatep.html',{'update_p':update_p})


 





@login_required
def ajouterR(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form =  RForm(request.POST,request.FILES)
            if form.is_valid():
                P=form.save(commit=False)
                P.architect = request.user
                P.save()
                return redirect('voirRealisation')
        else:
            form = RForm()
    
        return render(request, 'app_recrutement/AjouterRealisation.html', {'form': form})

def voirRealisation(request):
     if request.user.is_authenticated:
        realisations = realisation.objects.filter(architect=request.user)
        nbres_demande = len(realisations )
        context = {'realisations':realisations,'nbres_demande':nbres_demande}
        return render(request, 'app_recrutement/mesrealisation.html',context)



@login_required
def SupprimerRealisation(request,id):
    realisations =realisation.objects.get(id=id)
    realisations.delete()
    return redirect('voirRealisation')


@login_required
def Supprimerprofil(request,id):
    architecte = architect.objects.get(id=id)
    architecte.delete()
    return redirect('voirp')



def allrealisaion(request):
     realisations = realisation.objects.all()
     return render(request, 'app_recrutement/Projetinspire.html',{'realisations':realisations})



def detailrealisaion(request,id):
     realisations=realisation.objects.get(id=id)
     return render(request, 'app_recrutement/detailsprojet.html',{'realisations':realisations})



def desArchitecte(request,id):
      architecte= architect.objects.get(profile=id)
      realisations=realisation.objects.filter(architect=id)
      context = {'architecte': architecte, 'realisations': realisations}
      return render(request, 'app_recrutement/descriptionArchitecte.html',context)

@login_required
def indexclient(request):
     demandes = demande.objects.filter(client=request.user)
     projets = projet.objects.filter(demande__client=request.user)
     nbres_demande = len(demandes)
     nbres_projet = len(projets)
     context = {'nbres_demande': nbres_demande,'nbres_projet':nbres_projet}
     return render(request, 'app_recrutement/indexclient.html',context)


def gererclient(request):
    client = User.objects.filter(is_superuser=False)
    nbres_client = len(client)
    context = {'nbres_client': nbres_client,'client':client}
    return render(request, 'app_recrutement/gererclient.html',context)


def gererarchitecte(request):
    architecte = architect.objects.exclude(verification ="oui")
    nbres_architecte = len(architecte)
    context = {'nbres_architecte': nbres_architecte,'architecte':architecte}
    return render(request, 'app_recrutement/gérerarchitectes.html',context)


def allarchitecte(request):
    architecte = architect.objects.filter(verification ="oui")
    nbres_architecte = len(architecte)
    context = {'nbres_architecte': nbres_architecte,'architecte':architecte}
    return render(request, 'app_recrutement/listeallarchitectes.html',context)


@login_required
def newarchitecte(request):
      if request.user.is_authenticated:
            if request.method == 'POST':
                form = AForm(request.POST,request.FILES)
                if form.is_valid():
                     P=form.save(commit=False)
                     P.profile = request.user
                     P.save()
                return redirect('voirpn')
            else:
                form = AForm()
    
            return render(request, 'app_recrutement/newarchitecte.html', {'form': form})


@login_required
def voirpn(request):
     if request.user.is_authenticated:
        architect_exists = architect.objects.filter(profile=request.user).exists()
        if architect_exists:  
            Architect = architect.objects.get(profile=request.user)
            return render(request, 'app_recrutement/newprofil.html',{'architecte':Architect})
        else:
          return redirect('newarchitecte')



"""def ArchitectVerification(request):
    user = request.user
    if  user.is_authenticated:
        Architect = architect.objects.get(profile=user)
        if Architect:
           if Architect.verification == 'non':
               return redirect('newarchitecte')
           elif Architect.verification == 'oui':  
               return redirect('indexarchitecte')
        else:
            return redirect('newarchitecte') """

        

def ArchitectVerification(request):
    user = request.user
    if user.is_authenticated:
        architect_exists = architect.objects.filter(profile=user).exists()
        if architect_exists:
            Architect = architect.objects.get(profile=user)
            if Architect.verification == 'non':
                return redirect('newarchitecte')
            elif Architect.verification == 'oui':
                return redirect('indexarchitecte')
        else:
            return redirect('newarchitecte')

    return redirect('connexion')




def Accepterarchitecte(request,id):
    Architecte = architect.objects.get(id=id)
    Architecte.verification="oui"
    Architecte.save()
    return redirect('gererarchitecte')

@login_required
def gestionD(request):
     if request.user.is_authenticated:
        projets = projet.objects.filter(architecte=request.user)  
        return render(request, 'app_recrutement/gestion_détail.html',{'projets': projets})




@login_required
def etapesprojet(request,id):
    etapes_projet = etapes.objects.filter(projet=id)
    context = {'etapes_projet': etapes_projet}
    return render(request, 'app_recrutement/pageetape.html',context)

@login_required
def ajouter_etape(request,id):
    if request.user.is_authenticated:
        projet_instance = projet.objects.get(id=id)
        if request.method == 'POST':
            form = etapesForm(request.POST,request.FILES)
            if form.is_valid():
                etape = form.save(commit=False)
                etape.projet= projet_instance
                etape.save()
                return redirect('gestionD')
        else:
            form = etapesForm()
        return render(request, 'app_recrutement/ajouter_etape.html', {'form': form})





@login_required
def SupprimerEtapes(request,id):
    etap =etapes.objects.get(id=id)
    etap.delete()
    return redirect('gestionD')


@login_required
def UpdateEtapes(request,id):
    etap =etapes.objects.get(id=id)
    if request.method == "POST":
        update_etapes = etapesForm(request.POST,request.FILES,instance=etap)
        if update_etapes.is_valid():
            update_etapes.save()
            return redirect('gestionD')

    else:
        update_etapes = etapesForm(instance=etap)
    return render(request,'app_recrutement/update_etapes.html',{'update_etapes':update_etapes})


@login_required
def historiqueappelf(request):
    offres = decision.objects.filter(demade__client=request.user)
    context = {'offres': offres}
    return render(request, 'app_recrutement/historiqueappel.html',context)


def Supprimerclient(request,id):
    etap = User.objects.get(id=id)
    etap.delete()
    return redirect('gererclient')



def Supprimerarchitecte(request,id):
    etap =User.objects.get(id=id)
    etap.delete()
    return redirect('allarchitecte')


@login_required
def  etapespcli(request,id):
     etap = etapes.objects.filter(projet=id)
     context = {'etap': etap}
     return render(request, 'app_recrutement/etapesprojet.html',context)


@login_required
def Supprimerprojet(request,id):
    etap = projet.objects.get(id=id)
    etap.delete()
    return redirect('gererprojet')


@login_required
def UpdateR(request,id):
    R = realisation.objects.get(id=id)
    if request.method == "POST":
        update_etapes = RForm(request.POST,request.FILES,instance=R)
        if update_etapes.is_valid():
            update_etapes.save()
            return redirect('voirRealisation')

    else:
        update_etapes = RForm(instance=R)
    return render(request,'app_recrutement/update_realisation.html',{'update_etapes':update_etapes})


@login_required
def Updateappel(request,id):
    R = demande.objects.get(id=id)
    if request.method == "POST":
        update_etapes = DemandeForm(request.POST,request.FILES,instance=R)
        if update_etapes.is_valid():
            update_etapes.save()
            return redirect('listedemandeclient')

    else:
        update_etapes = RForm(instance=R)
    return render(request,'app_recrutement/update_demande.html',{'update_etapes':update_etapes}) 