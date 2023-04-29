import datetime
import random
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import qrcode
from PIL import Image, ImageFont, ImageDraw, ImageOps
from django.core.files.base import ContentFile
from django.http import HttpResponse
from .forms import StudentForm
from .models import Student
from datetime import date, timedelta


def create_student_id(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            # Extracting form data
            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            last_name = form.cleaned_data['last_name']
            dob = form.cleaned_data['date_of_birth']
            institution = form.cleaned_data['institution']
            logo = form.cleaned_data['logo']
            photo = form.cleaned_data['photo']

            # Generate a unique 11-digit student ID
            while True:
                student_id = str(random.randint(10000000000, 99999999999))
                if not Student.objects.filter(student_id=student_id).exists():
                    break
            
            # Set issuance and expiry dates
            issuance_date = datetime.date.today()
            expiry_date = issuance_date + datetime.timedelta(days=4*365)
            
            # Creating Image object
            image1 = Image.new('RGB', (500, 700), (255, 255, 255))  # creating a plain image
            font = ImageFont.truetype('Helvetica', size=35)  
            write = ImageDraw.Draw(image1)

            # Adding Institution logo
            logo_image = Image.open(logo)
            logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
            image1.paste(logo_image, (10, 10))

            # Adding Institution name
            color = 'rgb(64,64,64)'
            write.text((120, 45), institution, fill=color, font=ImageFont.truetype('Helvetica', size=35))

            # Adding Photo
            pic1 = Image.open(photo)
            pic1 = pic1.resize((200, 230), Image.ANTIALIAS)
            pic = ImageOps.expand(pic1, border=4, fill='gray')
            image1.paste(pic, (150, 130))

            # Adding Name
            color = 'rgb(0,0,0)'
            full_name = f"{first_name} {middle_name} {last_name}"
            write.text((50, 400), f'Name: {full_name}', fill=color, font=font)
            
            # Adding Student ID
            write.text((50, 480), f"ID: {student_id}", fill=color, font=font)

            # Adding DOB
            dob = dob.strftime("%Y-%m-%d")
            write.text((50, 440), f"DOB: {dob}", fill=color, font=font)
            
            # Adding expiry date
            expiry_date_str = expiry_date.strftime("%Y-%m-%d")
            write.text((50, 520), f"EXPIRY DATE: {expiry_date_str}", fill=color, font=font)

            # Adding QR Code
            qr_string = f"name: {full_name}\nDOB: {dob}\nInstitution: {institution}\nId: {student_id}\nExpiry date: {expiry_date_str}"
            qrc = qrcode.make(qr_string)  # generating qrcode with details like name, contact number and address
            qrcod = qrc.resize((100, 100), Image.ANTIALIAS)
            image1.paste(qrcod, (380, 610))

            # Saving Image
            response = HttpResponse(content_type='image/png')
            image1.save(response, 'PNG')
            response['Content-Disposition'] = f'attachment; filename="{full_name}_id.png"'
            
            # Save the image to the model
            student = form.save(commit=False)
            student.student_id = student_id
            student.id_card.save(f'{full_name}_id.png', ContentFile(response.getvalue()), save=True)
            student.save()
            return response
    else:
        form = StudentForm()

    context = {'form': form}
    return render(request, 'idgenerator/generate_id_card.html', context)

def edit_student_id(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect(reverse('generate', args=[student.id]))
        else:
            # handle form errors
            context = {'form': form}
            return render(request, 'idgenerator/generate_id_card.html', context=context, status=400)
    else:
        form = StudentForm(instance=student)
        context = {'form': form, 'edit': True}
        return render(request, 'idgenerator/generate_id_card.html', context=context)


def delete_student_id(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('all-student')
    
def get_all_students_id(request):
    try:
        students = Student.objects.all()
    except Exception as e:
        # handle database errors
        context = {'error': str(e)}
        return render(request, 'idgenerator/error.html', context=context, status=500)
    return render(request, 'idgenerator/all-student-id.html', {'students': students})


def get_student_id(request, id):
    try:
        student = get_object_or_404(Student, id=id)
    except Exception as e:
        # handle database errors
        context = {'error': str(e)}
        return render(request, 'idgenerator/error.html', context=context, status=500)
    return render(request, 'idgenerator/student-id.html', {'student': student})



# def generate_id_card(request):
#     if request.method == "POST":
#         form = StudentForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Extracting form data
#             first_name = form.cleaned_data['first_name']
#             middle_name = form.cleaned_data['middle_name']
#             last_name = form.cleaned_data['last_name']
#             dob = form.cleaned_data['date_of_birth']
#             institution = form.cleaned_data['institution']
#             logo = form.cleaned_data['logo']
#             photo = form.cleaned_data['photo']

#             # Creating Image object
#             image1 = Image.new('RGB', (500, 700), (255, 255, 255))  # creating a plain image
#             font = ImageFont.truetype('arial.ttf', size=20)  # you can use other fonts (calibre for example), but make sure you have it installed on your pc
#             write = ImageDraw.Draw(image1)

#             # Adding Institution logo
#             logo_image = Image.open(logo)
#             logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
#             image1.paste(logo_image, (10, 10))

#             # Adding Institution name
#             color = 'rgb(64,64,64)'
#             write.text((120, 45), institution, fill=color, font=ImageFont.truetype('arial.ttf', size=35))

#             # Adding Photo
#             pic1 = Image.open(photo)
#             pic1 = pic1.resize((200, 230), Image.ANTIALIAS)
#             pic = ImageOps.expand(pic1, border=4, fill='gray')
#             image1.paste(pic, (150, 130))

#             # Adding Name
#             color = 'rgb(0,0,0)'
#             full_name = f"{first_name} {middle_name} {last_name}"
#             write.text((50, 400), full_name, fill=color, font=font)

#             # Adding DOB
#             dob = dob.strftime("%Y-%m-%d")
#             write.text((50, 440), f"DOB: {dob}", fill=color, font=font)

#             # Adding QR Code
#             qr_string = f"{full_name}\n{dob}\n{institution}"
#             qrc = qrcode.make(qr_string)  # generating qrcode with details like name, contact number and address
#             qrcod = qrc.resize((100, 100), Image.ANTIALIAS)
#             image1.paste(qrcod, (380, 610))

#             # Saving Image
#             response = HttpResponse(content_type='image/png')
#             image1.save(response, 'PNG')
#             response['Content-Disposition'] = f'attachment; filename="{full_name}_id.png"'
#             return response

#     else:
#         form = StudentForm()

#     context = {'form': form}
#     return render(request, 'idgenerator/generate_id_card.html', context)



