from django.shortcuts import render
from django.http import HttpResponse
from PyPDF2 import PdfReader
import math
import re

# Main view
def autoGen(request):
    seating_plan = None

    if request.method == 'POST':
        # Get inputs from form
        num_classrooms = int(request.POST.get('num_classrooms'))
        num_columns = int(request.POST.get('num_columns'))
        benches_per_column = int(request.POST.get('benches_per_column'))

        # Handle multiple file uploads and extract student data
        student_list = []
        uploaded_files = request.FILES.getlist('student_list')

        for uploaded_file in uploaded_files:
            student_list.extend(extract_student_data(uploaded_file))

        # Check if we have students and all inputs are valid
        if student_list and num_classrooms > 0 and num_columns > 0 and benches_per_column > 0:
            # Generate column-wise seating arrangement based on inputs
            seating_plan = generate_seating_plan(student_list, num_classrooms, num_columns, benches_per_column)
        else:
            return HttpResponse("Error: All form fields and student lists are required.", status=400)

    return render(request, 'autoGen.html', {'seating_plan': seating_plan})


# Extract student data from uploaded PDFs
def extract_student_data(pdf_file):
    student_list = []
    pdf_reader = PdfReader(pdf_file)

    # Regular expression to capture student details (enrollment number and name)
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


# Generate the seating plan
def generate_seating_plan(student_list, num_classrooms, num_columns, benches_per_column):
    seating_plan = {}
    total_capacity_per_classroom = num_columns * benches_per_column
    student_index = 0

    # Assign students to classrooms based on capacity
    for classroom in range(1, num_classrooms + 1):
        seats = []
        bench_number = 1
        reverse = False

        # Check if there are more students to seat
        if student_index >= len(student_list):
            break

        # Fill the classroom with students column-wise
        for column in range(1, num_columns + 1):
            column_seats = []
            if reverse:
                for bench in range(benches_per_column):
                    if student_index < len(student_list):
                        enrollment_number, student_name = student_list[student_index]
                        column_seats.insert(0, f"Bench-{bench_number}: {student_name} ({enrollment_number})")
                        student_index += 1
                    else:
                        column_seats.insert(0, f"Bench-{bench_number}: Empty")
                    bench_number += 1
            else:
                for bench in range(benches_per_column):
                    if student_index < len(student_list):
                        enrollment_number, student_name = student_list[student_index]
                        column_seats.append(f"Bench-{bench_number}: {student_name} ({enrollment_number})")
                        student_index += 1
                    else:
                        column_seats.append(f"Bench-{bench_number}: Empty")
                    bench_number += 1

            seats.append(column_seats)
            reverse = not reverse  # Toggle reverse order for next column

            # If the classroom is full, break to move to the next classroom
            if student_index >= len(student_list) or len(seats) * benches_per_column >= total_capacity_per_classroom:
                break

        seating_plan[classroom] = seats

    return seating_plan
