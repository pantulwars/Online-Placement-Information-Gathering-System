import email
from multiprocessing import AuthenticationError
from django.shortcuts import render, HttpResponse,redirect
from home.models import student,alumni,company,Notification,Feedback, Personal_Notification, Application, Feedback_to_Companies
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import white
from reportlab.lib.colors import black
import os
import subprocess
import cgi, os
import cgitb
cgitb.enable()
from django.http import FileResponse
import io


is_login = 0
stud_name = "nil"
alum_name = "nil"
comp_name = "nil"
stud_username = "nil"
alum_username = "nil"
comp_username = "nil"
st_username="nil"
c_username="nil"

def index(request):
    return render(request,'index.html')

def make_resume(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    if request.method == "POST":
        user_name=stud_username
        name=stud_name
        s=student.objects.filter(username=user_name)
        email=s[0].email
        phone=s[0].phone
        department=request.POST.get('department')
        cgpa=request.POST.get('cgpa')
        desc=request.POST.get('desc')
        skills=request.POST.get('skills')
        canvas = Canvas("Resumes/"+user_name+".pdf", pagesize=A4)
        s2 = "Email          : "+email
        s3 = "Phone          : "+phone
        s4 = "Department     : "+department
        s5 = "Cgpa               : "+cgpa
        boundary = ImageReader('Images\Resume_boundary.png')
        width = 600; height = 844; y=0; x=0
        canvas.drawImage(boundary,x,y,width,height,anchor='sw',anchorAtXY=True,showBoundary=False)
        x=60
        canvas.setFont("Times-Bold", 50, leading = None)
        canvas.setFillColor(white)
        canvas.drawString(x, 700, name) 
        canvas.setFillColor(black)
        canvas.setFont("Times-Roman", 20, leading = None)
        canvas.drawString(x+5, 530, s2) 
        canvas.drawString(x+5, 500, s3) 
        canvas.setFont("Times-Roman", 20, leading = None)
        canvas.drawString(x+5, 390, s4) 
        canvas.drawString(x+5, 360, s5) 
        canvas.setFont("Times-Roman", 20, leading = None)
        canvas.drawString(x+5, 250, skills) 
        canvas.setFont("Times-Roman", 20, leading = None)
        canvas.drawString(x+5, 130, desc) 
        canvas.save()
       
    return render(request,'makeresume.html')


def view_resume(request):
    with open("Resumes/"+stud_username+".pdf", 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response

    
    
 


def upload_resume(request):
    fileitem = form['filename']
    if fileitem.filename:
        fn = os.path.basename(fileitem.filename)
        open('Resumes/'+fn, 'wb').write(fileitem.file.read())
     
        
        
def student_page(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    context = {
        'name' : stud_name
    }
    return render(request,'student.html', context)

def alumni_page(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    if request.method == "POST":
        companies=request.POST.get('comp_list')
        alu=alumni.objects.get(username=alum_username)
        alu.companies_worked_in=companies
        alu.save()
        return redirect("/Alumni")
    context = {
        'name' : alum_name
    }
    return render(request,'alumni.html', context)


'''
def alumni_add_company(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    if request.method == "POST":
        feedback=request.POST.get('feedback')
        f=Feedback.objects.get(alum_user_id=alum_username,stud_user_id=st_username)
        f.feedback=feedback
        f.save()
        return redirect("/Alumni")
    return render(request,'alumni_add_company.html')
    '''

    
def company_page(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    context = {
        'name' : comp_name
    }
    return render(request,'Company.html', context)


def Login(request):
    if request.method == "POST":
        User_id = request.POST.get('User_id')
        Pass1 = request.POST.get('Password')
        User_type = request.POST.get('User_type')
        print(User_id,Pass1,User_type)
        global is_login
        if(User_type == 'Student'):
            if(student.objects.filter(username=User_id)):
                stud = student.objects.filter(username=User_id)[0]
                if(stud.password==Pass1):
                    is_login=1 
                    print(is_login)
                    global stud_name
                    stud_name = stud.name
                    global stud_username
                    stud_username = stud.username
                    return redirect('/Student')
                    
                else:
                    messages.error(request, "Passwords/User_Id didn't matched!!")
                    return redirect('/Login')

        if(User_type == 'Alumni'):
            if(alumni.objects.filter(username=User_id)):
                alum = alumni.objects.filter(username=User_id)[0]
                if(alum.password==Pass1):
                    is_login=1
                    global alum_name
                    alum_name = alum.name
                    global alum_username
                    alum_username = alum.username
                    return redirect('/Alumni')
                else:
                    messages.error(request, "Passwords/User_Id didn't matched!!")
                    return redirect('/Login')

        if(User_type == 'Company'):
            if(company.objects.filter(username=User_id)):
                comp = company.objects.filter(username=User_id)[0]
                if(comp.password==Pass1):
                    is_login=1
                    global comp_name
                    comp_name = comp.name
                    global comp_username
                    comp_username = comp.username
                    return redirect('/Company')
                else:
                    messages.error(request, "Passwords/User_Id didn't matched!!")
                    return redirect('/Login')

        else:
            messages.error(request, "Passwords!")
            return redirect('/Login')

    return render(request,'Login.html')

def Logout(request):
    global is_login
    is_login=0
    return redirect('/Login')

def job_posting(request):
    if request.method == "POST":
        jd=request.POST.get('jd')
        c=company.objects.get(username=comp_username)
        c.job_details=jd
        c.save()
        return redirect("/Company")

    


def Signup(request):
    if request.method == "POST":
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Phone = request.POST.get('phone')
        User_id = request.POST.get('User_id')
        Pass1 = request.POST.get('Password')
        Pass2 = request.POST.get('Password2')
        User_type = request.POST.get('User_type')
        if ((student.objects.filter(username=User_id)) or(alumni.objects.filter(username=User_id)) or (company.objects.filter(username=User_id)) ):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('/Signup')
        if ((student.objects.filter(email=Email)) or(alumni.objects.filter(email=Email)) or (company.objects.filter(email=Email))  ):
            messages.error(request, "Email Already Registered!!")
            return redirect('/Signup')
        if len(User_id)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('/Signup')
        
        if Pass1 != Pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('/Signup')
        
        if not User_id.isalnum():
            messages.error(request, "User-id must be Alpha-Numeric!!")
            return redirect('/Signup')
        if(User_type == 'Student'):
            Student = student(name=Name, email=Email, phone=Phone, username=User_id, password = Pass1)
            Student.save()
            messages.success(request, 'User is registered now you can login')
            return redirect('/Signup')
        elif(User_type == 'Alumni'):
            Alumni = alumni(name=Name, email=Email, phone=Phone, username=User_id, password = Pass1)
            Alumni.save()
            messages.success(request, 'User is registered now you can login')
            return redirect('/Signup')
        elif(User_type == 'Company'):
            Company = company(name=Name, email=Email, phone=Phone, username=User_id, password = Pass1)
            Company.save()
            messages.success(request, 'User is registered now you can login')
            return redirect('/Signup')
        else:
            messages.error(request, 'Wrong User-type selected')
            return redirect('/Signup')

        
    return render(request,'Signup.html')

def notification_student(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    stud_list=[]
    for i in Notification.objects.filter(visible_to_student=True):
        var=[]
        var.append(i.name)
        var.append(i.notification)
        stud_list.append(var)
    context = {
        's_list' : stud_list
    }
    return render(request, 'notification_student.html', context)

def student_personal_notification(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    not_list=[]
    for i in Personal_Notification.objects.filter(receiver=stud_username):
        var=[]
        var.append(i.not_name)
        var.append(i.notification)
        not_list.append(var)
    context = {
        's_list' : not_list
    }
    return render(request, 'student_personal_notification.html', context)

def given_feedback(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    feedback_list=[]
    for i in Feedback.objects.filter(stud_user_id=stud_username):
        var=[]
        alum = alumni.objects.get(username=i.alum_user_id)
        var.append("Feed back given by " + alum.name)
        var.append(i.feedback)
        feedback_list.append(var)
    context = {
        'f_list' : feedback_list
    }
    return render(request, 'given_feedback.html', context)
    

def notification_company(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    comp_list=[]
    for i in Notification.objects.filter(visible_to_company=True):
        var=[]
        var.append(i.name)
        var.append(i.notification)
        comp_list.append(var)
    context = {
        'c_list' : comp_list
    }
    return render(request, 'notifications_company.html', context)

def company_personal_notification(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    not_list=[]
    for i in Personal_Notification.objects.filter(receiver=comp_username):
        var=[]
        var.append(i.not_name)
        var.append(i.notification)
        not_list.append(var)
    context = {
        'c_list' : not_list
    }
    return render(request, 'company_personal_notification.html', context)

def view_application(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    if request.method == "POST":
        s_username = request.POST.get('stud_username')
        with open("Resumes/"+s_username+".pdf", 'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'filename=some_file.pdf'
            return response
    app_list=[]
    print(comp_username)
    for i in Application.objects.filter(comp_user_id= comp_username ):
        var=[]
        var.append(i.app_title)
        var.append(i.application)
        var.append(i.stud_user_id)
        app_list.append(var)
        print(app_list)
    context = {
        'a_list' : app_list
    }
    return render(request, 'view_application.html', context)

def view_all_application(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    if request.method == "POST":
        s_username = request.POST.get('stud_username')
        with open("Resumes/"+s_username+".pdf", 'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'filename=some_file.pdf'
            return response
    context = {
        's_list' : student.objects.all()
    }
    return render(request, 'view_all_applications.html', context)


def notification_alumni(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    alum_list=[]
    for i in Notification.objects.filter(visible_to_alumni=True):
        var=[]
        var.append(i.name)
        var.append(i.notification)
        alum_list.append(var)
    context = {
        'a_list' : alum_list
    }
    return render(request, 'notifications_alumni.html', context)

def alumni_personal_notification(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    not_list=[]
    for i in Personal_Notification.objects.filter(receiver=alum_username):
        var=[]
        var.append(i.not_name)
        var.append(i.notification)
        var.append(i.generator)
        not_list.append(var)
    context = {
        'a_list' : not_list
    }
    return render(request, 'alumni_personal_notification.html', context)

def feedback_to_companies(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    context = {
        'c_list' : company.objects.all()
    }
    return render(request, 'feedback_to_companies.html', context)

def give_company_feedback(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    global c_username
    if request.method == "GET":
        c_username = request.GET.get('comp_username')
        print("check1")
        return render(request, 'give_company_feedback.html')
    if request.method == "POST":
        feed = request.POST.get('feedback')
        f_to_c = Feedback_to_Companies(alum_uid = alum_username, comp_uid = c_username, feedback = feed)
        f_to_c.save()
        print("check2")
        return redirect("/Feedback_to_companies")

        
def Contact_us(request):
    return render(request,'Contact_us.html')


def feedback_request(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    if request.method == "POST":
        al_username = request.POST.get('alum_username')
        if(Feedback.objects.filter(alum_user_id=al_username,stud_user_id=stud_username)):
            messages.error(request,'You have already applyed to this alumni')
            return redirect("/Feedback_Request")
        else:
            #print(stud_username,alum_username)
            f=Feedback(alum_user_id=al_username,stud_user_id=stud_username)
            f.save()
            notification = Personal_Notification(generator = stud_username, receiver = al_username, not_name = "feedback request", notification = stud_name + " has requested you to give feedback!!")
            notification.save()
    context = {
        'alu_list' : alumni.objects.all() 
    }
    return render(request,'feedback_request.html', context)

def give_feedback(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    global st_username
    if request.method == "GET":
        st_username = request.GET.get('stud_username')
    if request.method == "POST":
        feedback=request.POST.get('feedback')
        f=Feedback.objects.get(alum_user_id=alum_username,stud_user_id=st_username)
        f.feedback=feedback
        f.save()
        return redirect("/Alumni")
    return render(request,'feedback.html')

def apply_for_company(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    if request.method == "POST":
        c_username = request.POST.get('comp_username')
        if(Application.objects.filter(stud_user_id=stud_username,comp_user_id=c_username)):
            messages.error(request,'You have already applyed for this company')
            return redirect("/Apply_for_companies")
        else:
            appl = Application(stud_user_id = stud_username, comp_user_id = c_username, app_title = "Application request", application = stud_name + "has applied for this company!!")
            appl.save()
            return redirect("/Student")
    c_list = []
    for i in company.objects.filter(Verified=True).exclude(job_details="nil"):
        f_list = Feedback_to_Companies.objects.filter(comp_uid = i.username)
        print(f_list)
        var = [i.name, i.phone, i.email, i.job_details, i.username, f_list]
        c_list.append(var)
    context = {
        'com_list' : c_list
    }
    return render(request,'apply_for_company.html', context)

def job_posting(request):
    global is_login
    if is_login==0:
        return redirect('/Login')
    if request.method == "POST":
        job_post = request.POST.get('jd')
        com=company.objects.get(username=comp_username)
        com.job_details=job_post
        com.save()
        return redirect("/Company")
    return render(request,'Job_Posting.html')