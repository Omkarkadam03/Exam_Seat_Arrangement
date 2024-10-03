from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from PyPDF2 import PdfReader
import math
import re
# Create your views here.

#def autoGen(request):
    #return render( request, "autoGen.html")

# functionality/views.py

def autoGen(request):
    seating_plan = None

    if request.method == 'POST':
        num_classrooms = int(request.POST['num_classrooms'])
        num_rows = int(request.POST['num_rows'])
        benches_per_row = int(request.POST['benches_per_row'])

        # Handle file upload
        uploaded_file = request.FILES['student_list']
        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)
        
        # Extract student numbers and names from the PDF
        file_url = fs.path(file_path)
        student_list = extract_student_enrollment_and_names(file_url)

        # Generate seating arrangement
        seating_plan = generate_seating_plan(student_list, num_classrooms, num_rows, benches_per_row)

    return render(request, 'autoGen.html', {'seating_plan': seating_plan})

def extract_student_enrollment_and_names(pdf_path):
    student_list = []
    pdf_reader = PdfReader(pdf_path)

    # Regular expression to capture enrollment number and name
    pattern = re.compile(r"(CM\d+)\s+(\d{8,})\s+([A-Za-z\s]+)")

    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            lines = text.splitlines()
            for line in lines:
                match = pattern.match(line)
                if match:
                    enrollment_number = match.group(2)
                    student_name = match.group(3).strip()
                    student_list.append(f"{enrollment_number} {student_name}")

    return student_list

def generate_seating_plan(student_list, num_classrooms, num_rows, benches_per_row):
    # Generate seating plan for all classrooms
    seating_plan = {}
    student_index = 0

    for classroom in range(1, num_classrooms + 1):
        seats = []
        for row in range(num_rows):
            row_seats = []
            for bench in range(benches_per_row):
                if student_index < len(student_list):
                    row_seats.append(student_list[student_index])
                    student_index += 1
                else:
                    row_seats.append('Empty')
            seats.append(row_seats)
        seating_plan[classroom] = seats

    return seating_plan
