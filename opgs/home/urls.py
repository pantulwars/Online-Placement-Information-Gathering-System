from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("",views.index, name='home'),
    path("Login",views.Login, name='home'),
    path("Logout",views.Logout, name='home'),
    path("Signup",views.Signup, name='home'),
    path("Contact_us",views.Contact_us, name='home'),
    path("Student",views.student_page,name='home'),
    path("Make_resume",views.make_resume,name='home'),
    path("notifications_company",views.notification_company,name='home'),
    path("Notification_Student",views.notification_student,name='home'),
    path("notification_alumni",views.notification_alumni,name='home'),
    #path("Feedback",views.feedback,name='home'),
    path("Feedback_Request",views.feedback_request,name='home'),
    path("Alumni",views.alumni_page,name='home'),
    #path("Alumni_add_Company",views.alumni_add_company,name='home'),
    path("Company",views.company_page,name='home'),
    path("student_personal_notification",views.student_personal_notification,name='home'),
    path("alumni_personal_notification",views.alumni_personal_notification,name='home'),
    path("company_personal_notification",views.company_personal_notification,name='home'),
    path("Give_Feedback",views.give_feedback,name='home'),
    path("Given_Feedback",views.given_feedback,name='home'),
    path("view_resume",views.view_resume,name='home'),
    path("Apply_for_companies",views.apply_for_company,name='home'),
    path("View_Application",views.view_application,name='home'),
    path("View_all_Application",views.view_all_application,name='home'),
    path("Job_Posting",views.job_posting ,name='home'),
    path("Upload_Resume",views.upload_resume ,name='home'),
    path("Feedback_to_companies",views.feedback_to_companies ,name='home'),
    path("Give_company_feedback",views.give_company_feedback ,name='home'),




]