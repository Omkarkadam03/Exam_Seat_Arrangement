from django.shortcuts import render, redirect
from django.http import HttpResponse
from PyPDF2 import PdfReader
import math
import re
# Create your views here.

# functionality/views.py

def autoGen(request):
    seating_plan = None

    if request.method == 'POST':
        num_classrooms = int(request.POST['num_classrooms'])
        num_rows = int(request.POST['num_rows'])
        benches_per_row = int(request.POST['benches_per_row'])

        # Handle multiple file uploads
        student_list = []
        uploaded_files = request.FILES.getlist('student_list')
        
        for uploaded_file in uploaded_files:
            student_list.extend(extract_student_data(uploaded_file))

        # Generate column-wise seating arrangement
        seating_plan = generate_seating_plan(student_list, num_classrooms, num_rows, benches_per_row)

    return render(request, 'autoGen.html', {'seating_plan': seating_plan})

def extract_student_data(pdf_file):
    student_list = []
    pdf_reader = PdfReader(pdf_file)

    # Regular expression to capture student details (only name and enrollment number)
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
                    student_list.append((enrollment_number, student_name))

    return student_list

def generate_seating_plan(student_list, num_classrooms, num_rows, benches_per_row):
    seating_plan = {}
    student_index = 0

    for classroom in range(1, num_classrooms + 1):
        seats = []

        # Column-wise seating arrangement
        for row in range(num_rows):
            row_seats = []
            for bench in range(benches_per_row):
                if student_index < len(student_list):
                    enrollment_number, student_name = student_list[student_index]
                    row_seats.append(f"Bench-{bench + 1}: {student_name} ({enrollment_number})")
                    student_index += 1
                else:
                    row_seats.append(f"Bench-{bench + 1}: Empty")
            seats.append(row_seats)
        seating_plan[classroom] = seats

    return seating_plan





