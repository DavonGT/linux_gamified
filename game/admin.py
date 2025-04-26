from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Question
from openpyxl import load_workbook

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('task', 'difficulty')  # Display task and difficulty
    change_list_template = "admin/game/question_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.upload_excel, name='upload_excel'),
        ]
        return custom_urls + urls

    def upload_excel(self, request):
        if request.method == "POST":
            excel_file = request.FILES["excel_file"]
            try:
                # Load the Excel file
                workbook = load_workbook(excel_file)
                sheet = workbook.active

                # Ensure the required columns exist
                headers = [cell.value for cell in sheet[1]]
                required_columns = {'task', 'correct_commands', 'difficulty'}
                if not required_columns.issubset(headers):
                    messages.error(request, "Excel file must contain 'task', 'correct_commands', and 'difficulty' columns.")
                    return redirect("..")

                # Map column headers to indices
                header_indices = {header: idx for idx, header in enumerate(headers)}

                # Iterate through rows and create Question objects
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    Question.objects.create(
                        task=row[header_indices['task']],
                        correct_commands=row[header_indices['correct_commands']],
                        difficulty=row[header_indices['difficulty']]
                    )

                messages.success(request, "Tasks have been successfully uploaded!")
                return redirect("..")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect("..")

        return render(request, "admin/game/upload_excel.html")