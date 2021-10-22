from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate
from .models import korisnici
from .models import predmeti
from .models import upis
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.

def register(request):
    context = {}
    if(request.POST):
        form = RegistrationForm(request.POST)
        if(form.is_valid()):
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request,'users/register.html',context)


@staff_member_required()
def courses(request):
    context = {}
    courses = predmeti.objects.all()
    if(request.POST):
        if request.POST.get("Details"):
            predmet_kod = request.POST.get("course_kod")
            predmet = predmeti.objects.all().filter(kod = predmet_kod).first()
            context['predmet'] = predmet
            return render(request, 'users/details.html', context)

        if request.POST.get("Edit"):
            predmet_kod = request.POST.get("course_kod")
            predmet = predmeti.objects.all().filter(kod = predmet_kod).first()
            context['predmet'] = predmet
            return render(request, 'users/edit.html', context)

        if request.POST.get("edited"):
            predmet_kod = request.POST.get("kod")
            predmet = predmeti.objects.all().filter(kod = predmet_kod).first()
            predmet.ime = request.POST.get("ime")
            predmet.kod = request.POST.get("kod")
            predmet.program = request.POST.get("program")
            predmet.bodovi = request.POST.get("bodovi")
            predmet.sem_redovni = request.POST.get("redovni")
            predmet.sem_izvanredni = request.POST.get("izvanredni")
            predmet.izborni = request.POST.get("izborni")
            predmet.save()
            return redirect('courses')

    context['courses'] = courses
    return render(request,'users/courses.html', context)


def students(request):
    context = {}
    current_user = request.user
    flag = 0
    context['flag'] = flag
    users = korisnici.objects.all()
    if current_user.role == "student":
        context['users'] = current_user
        flag = 1
        context['flag'] = flag
        return render(request,'users/students.html',context)
    context['users'] = users
    return render(request,'users/students.html',context)

def redirect_to_upisni_list():
    pass

student_email = ''
@login_required()
def upisni_list(request):
    context = {}
    studenti = []
    if (request.POST):

        if request.POST.get("add_predmet"):
            neupisan_predmet_id = request.POST.get('neupisan_predmet', '')
            predmet = predmeti.objects.all().filter(id = neupisan_predmet_id).first()
            student_id = request.POST.get('student_id', '')
            student = korisnici.objects.all().filter(id = student_id).first()
            student_email = student.email
            lista_upisa = upis.objects.all()
            for upis1 in lista_upisa:
                if upis1.student_id_id == student.id and upis1.predmet_id_id == predmet.id:
                    messages.error(request,f'Predmet već upisan')
                    return redirect('students')
            upisni_list = upis(status = "enrolled", predmet_id_id = neupisan_predmet_id, student_id_id = student_id)
            upisni_list.save()
            return redirect('students')

        if request.POST.get("remove_predmet"):
            upisan_predmet_id = request.POST.get('upisan_predmet_id', '')
            student_id = request.POST.get('student_id', '')
            print("STUDENT ID:", student_id)
            print("PREDMET ID: ", upisan_predmet_id)
            upis.objects.filter(student_id_id = student_id, predmet_id_id = upisan_predmet_id).delete()
            return redirect("students")

        if request.POST.get("polozen_predmet"):
            upisan_predmet_id2 = request.POST.get('upisan_predmet_id', '')
            student_id2 = request.POST.get('student_id', '')
            predmet_upis = upis.objects.filter(student_id_id = student_id2, predmet_id_id = upisan_predmet_id2).first()
            predmet_upis.status = "passed"
            predmet_upis.save()
            return redirect("students")
            
        return redirect('students')

    #GET REQUEST    
    if (request.GET):
        upisani = []
        neupisani = []
        student_email1 = request.GET.get('name')
        student = korisnici.objects.all().filter(email = student_email1).first()
        #print("STUDENTOVO IME:", student_email)
        upisni_list_studenta = upis.objects.all().filter(student_id_id = student.id)
        for row in upisni_list_studenta:
            try:
                if( row.status == "enrolled" or  row.status == "passed"):
                    upisani.append(predmeti.objects.all().filter(id = row.predmet_id_id).first())
                #else:
                   # neupisani.append(predmeti.objects.all().filter(id = row.predmet_id_id).first())
            except:
                pass
        get_predmeti = predmeti.objects.all()
        for g_pred in get_predmeti:
            if(g_pred not in upisani):
                neupisani.append(g_pred)
        if student.status == 'redovni':
            broj_semestara = [1,2,3,4,5,6]
        if student.status == 'izvanredni':
            broj_semestara = [1,2,3,4,5,6,7,8]
        context['upisni_list_studenta'] = upisni_list_studenta
        context['broj_semestara'] = broj_semestara
        context['student'] = student
        context['upisani'] = upisani
        context['neupisani'] = neupisani
        return render(request,'users/upisni_list.html', context)

def details(request):
    return render(request, 'users/details.html')

def edit(request):
    pass

def student_upisni_list(request):
    context = {}
    upisani = []
    neupisani = []
    current_student = request.user
    upisni_list_studenta = upis.objects.all().filter(student_id_id = current_student.id)
    for row in upisni_list_studenta:
        try:
            if( row.status == "enrolled" or  row.status == "passed"):
                upisani.append(predmeti.objects.all().filter(id = row.predmet_id_id).first())
        except:
            pass
    get_predmeti = predmeti.objects.all()
    for g_pred in get_predmeti:
        if(g_pred not in upisani):
            neupisani.append(g_pred)
    if current_student.status == 'redovni':
        broj_semestara = [1,2,3,4,5,6]
    if current_student.status == 'izvanredni':
        broj_semestara = [1,2,3,4,5,6,7,8]
    context['upisni_list_studenta'] = upisni_list_studenta
    context['broj_semestara'] = broj_semestara
    context['student'] = current_student
    context['upisani'] = upisani
    context['neupisani'] = neupisani    
    return render(request, 'users/student_upisni_list.html',context)