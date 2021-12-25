# Модуль для создания своих обработчиков get- и post-запросов
from django.views.generic import View
# Модуль для отображения страницы
from django.shortcuts import render
# Модуль для использования автоматического редиректа
from django.shortcuts import redirect

# Импортирование моделей "списка" и "заданий"
from .models import Schedule
from .models import Task

# Импортирование форм моделей "списка" и "заданий"
from .forms import ScheduleForm
from .forms import TaskForm


# Класс для вывода всех текущих списков
class AllSchedule(View):

	def get(self, request):
		# Выборка из базы данных всех текущих списков
		all_schedule = Schedule.objects.all()
		# Создание формы для списка
		schedule_form = ScheduleForm()
		# Отображение страницы
		return render(request, 'all_schedule.html', context={'all_schedule': all_schedule, 'schedule_form': schedule_form})

	def post(self, request):
		# Получение данных с формы
		new_schedule = ScheduleForm(request.POST)
		# Сохранение формы как объекта в базе данных
		new_schedule.save()
		# Выборка текущих списков (+ добавленный)
		all_schedule = Schedule.objects.all()
		# Создание формы для нового списка
		schedule_form = ScheduleForm()
		# Отображение страницы
		return render(request, 'all_schedule.html', context={'all_schedule': all_schedule, 'schedule_form': schedule_form})


# Класс для отображение всех текущих заданий выбранного списка
class DetailSchedule(View):

	def get(self, request, slug):
		# Извлечений из базы данных объекта "списка" по переданному slug
		schedule = Schedule.objects.get(slug__iexact = slug)
		# Получение всех "заданий" и создание промежуточного массива
		tasks_plug = Task.objects.all()
		# Создание массива для передачи в context
		tasks = []
		# Перебор все объектов "заданий" 
		for task in tasks_plug:
			# Обноружение "заданий" с таким же slug как у выбранного "списка"
			if task.slug == slug:
				# Вывод в целевом массиве только тех "заданий",
				# которые соответствуют текущему "списку"
				tasks.append(task)
		# Создание формы для создания нового "задания"
		task_form = TaskForm()
		# Отображение страницы
		return render(request, 'detail_schedule.html', context={
			'schedule': schedule,
			'tasks': tasks,
			'task_form': task_form})

	def post(self, request, slug):
		# Извлечений из базы данных объекта "списка" по переданному slug
		schedule = Schedule.objects.get(slug__iexact = slug)
		# Создание нового "задания" на основе переданных данных
		# post-запроса + текущий slug
		new_task = Task.objects.create(title = request.POST['title'],
			priority = request.POST['priority'],
			slug = slug)
		# Сохранение нового задания
		new_task.save()
		# Получение всех "заданий" и создание промежуточного массива
		tasks_plug = Task.objects.all()
		# Создание массива для передачи в context
		tasks = []
		# Перебор все объектов "заданий" 
		for task in tasks_plug:
			# Обноружение "заданий" с таким же slug как у выбранного "списка"
			if task.slug == slug:
				# Вывод в целевом массиве только тех "заданий",
				# которые соответствуют текущему "списку"
				tasks.append(task)
		# Создание формы для создания нового "задания"
		task_form = TaskForm()
		# Отображение страницы
		return render(request, 'detail_schedule.html', context={
			'schedule': schedule,
			'tasks': tasks,
			'task_form': task_form})


# Класс для удаления объекта "списка"
class DeleteSchedule(View):

	def get(self, request, slug):
		# Собираем все "задания" текущего "списка"
		tasks = Task.objects.all()
		for task in tasks:
			if task.slug == slug:
				# Удаляем задания с таким же slug как у целевого "списка"
				task.delete()
		# Обнаруживаем объект "списка" по slug
		schedule_for_delete = Schedule.objects.get(slug__iexact=slug)
		# Удаляем выбранный элемент
		schedule_for_delete.delete()
		# Собираем новый массивы для отображения всех текущих "списков"
		all_schedule = Schedule.objects.all()
		# Создание формы для создания нового "списка"
		schedule_form = ScheduleForm()
		# Отображение страницы
		return render(request, 'all_schedule.html', context={'all_schedule': all_schedule, 'schedule_form': schedule_form})


# Класс для удаления объекта "задания"
class DeleteTask(View):
	
	def get(self, request, slug, id):
		# Выбираем объект "задания" для удаления по id
		task_for_delete = Task.objects.get(id=id)
		# Удаляем выбранный объект
		task_for_delete.delete()
		# Находим текущий список
		schedule = Schedule.objects.get(slug__iexact = slug)
		# Перенаправляем пользователя на страницу текущего "списка"
		return redirect(schedule)
