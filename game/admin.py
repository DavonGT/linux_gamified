from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Task, Chapter, Mission
from openpyxl import load_workbook

admin.site.register(Chapter)
admin.site.register(Mission)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'difficulty', 'category')  # Display task and difficulty
    change_list_template = "admin/game/task_changelist.html"

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

                # Ensure the required columns exist (correctly matched)
                headers = [cell.value for cell in sheet[1]]
                required_columns = {'chapter_name', 'chapter_description', 'mission_name', 'instructor_sentence', 'task', 'correct_commands', 'difficulty', 'category', 'hint', 'chapter_number'}
                missing_columns = required_columns - set(headers)

                if missing_columns:
                    messages.error(request, f"Missing columns: {', '.join(missing_columns)}. Please ensure the Excel file has all the required columns.")
                    return redirect("..")

                # Map column headers to indices
                header_indices = {header: idx for idx, header in enumerate(headers)}

                # Iterate through rows and create Task, Mission, and Chapter objects
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    chapter_number = row[header_indices['chapter_number']]  # Extract chapter_number
                    chapter_name = row[header_indices['chapter_name']]
                    chapter_description = row[header_indices['chapter_description']]
                    mission_name = row[header_indices['mission_name']]
                    instructor_sentence = row[header_indices['instructor_sentence']]
                    task_name = row[header_indices['task']]
                    correct_commands = row[header_indices['correct_commands']]
                    difficulty = row[header_indices['difficulty']]
                    category = row[header_indices['category']] if 'category' in header_indices else 'other'
                    hint = row[header_indices['hint']] if 'hint' in header_indices else ''

                    # Create or get Chapter (using chapter_number for uniqueness)
                    chapter, created = Chapter.objects.get_or_create(
                        number=chapter_number, 
                        defaults={'name': chapter_name, 'description': chapter_description}
                    )

                    # Create or get Task
                    task, created = Task.objects.get_or_create(
                        task=task_name,
                        defaults={
                            'correct_commands': correct_commands,
                            'difficulty': difficulty,
                            'category': category,
                            'hint': hint,
                        }
                    )

                    # Create or get Mission (linked to Chapter and Task, passing instructor_sentence to Mission)
                    mission, created = Mission.objects.get_or_create(
                        chapter=chapter,
                        task=task,
                        mission_name=mission_name,
                        instructor_sentence=instructor_sentence  # This should only be passed to Mission
                    )

                messages.success(request, "Tasks, Chapters, and Missions have been successfully uploaded!")
                return redirect("admin:game_task_changelist")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect("..")

        return render(request, "admin/game/upload_excel.html")
