from django.shortcuts import render
from django.http import HttpResponse
from PyPDF2 import PdfReader
import re
from home.views import logout_view, sign_up

def autoGen(request):
    seating_plan = None
    bench_range = []  # Default empty list for bench_range to avoid UnboundLocalError

    if request.method == 'POST':
        try:
            # Get inputs from form and ensure they are integers
            num_classrooms = int(request.POST.get('num_classrooms', 0))
            num_columns = int(request.POST.get('num_columns', 0))
            benches_per_column = int(request.POST.get('benches_per_column', 0))

            # Ensure the input values are valid
            if num_classrooms <= 0 or num_columns <= 0 or benches_per_column <= 0:
                return HttpResponse("Error: All form fields must be positive integers.", status=400)

            # Handle multiple file uploads and extract student data
            student_list = []
            uploaded_files = request.FILES.getlist('student_list')
            for uploaded_file in uploaded_files:
                student_list.extend(extract_student_data(uploaded_file))

            if student_list:
                # Generate column-wise seating arrangement based on inputs
                seating_plan = generate_seating_plan(student_list, num_classrooms, num_columns, benches_per_column)
                bench_range = list(range(benches_per_column))  # Set range only if seating plan is generated

        except ValueError:
            return HttpResponse("Error: Invalid input. Please enter valid numbers for classrooms, columns, and benches.", status=400)

    return render(request, 'autoGen.html', {'seating_plan': seating_plan, 'bench_range': bench_range})

def extract_student_data(pdf_file):
    student_list = []
    pdf_reader = PdfReader(pdf_file)
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

def generate_seating_plan(student_list, num_classrooms, num_columns, benches_per_column):
    seating_plan = {}
    student_index = 0
    total_capacity_per_classroom = num_columns * benches_per_column  # Calculate capacity for each classroom

    for classroom in range(1, num_classrooms + 1):
        seats = [[] for _ in range(benches_per_column)]  # Initialize rows for each column
        bench_number = 1

        # Check if there are enough students remaining
        if student_index >= len(student_list):
            break

        # Fill each column vertically within the classroom
        for column in range(num_columns):
            column_benches = ["Empty"] * benches_per_column  # Initialize empty seats for the column

            if column % 2 == 0:  # Odd-numbered columns in ascending order
                for bench in range(benches_per_column):
                    if student_index < len(student_list):
                        enrollment_number, student_name = student_list[student_index]
                        column_benches[bench] = f"Bench-{bench_number}: {student_name} ({enrollment_number})"
                        student_index += 1
                    bench_number += 1
            else:  # Even-numbered columns in descending order
                for bench in range(benches_per_column - 1, -1, -1):
                    if student_index < len(student_list):
                        enrollment_number, student_name = student_list[student_index]
                        column_benches[bench] = f"Bench-{bench_number}: {student_name} ({enrollment_number})"
                        student_index += 1
                    bench_number += 1

            # Place the filled column in the seats arrangement
            for row in range(benches_per_column):
                if row < len(seats):
                    seats[row].append(column_benches[row])  # Add each bench to its corresponding row

            # Move to next classroom if this one is full
            if student_index >= len(student_list) or (column + 1) * benches_per_column >= total_capacity_per_classroom:
                break

        # Store the completed classroom arrangement
        seating_plan[classroom] = seats

    return seating_plan



