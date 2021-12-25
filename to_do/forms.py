# Модуль для работы с формами
from django import forms
# Импортирование созданных моделей
from .models import Schedule
from .models import Task


# Форма для модели "списка"
class ScheduleForm(forms.ModelForm):
	class Meta:
		# Определение модели для формы
		model = Schedule
		# Определение полей, которые будут использоваться в форме
		fields = ['title', 'slug']
		# Установка виджетов для полей и присваивание им специфичных атрибутов
		widgets = {
			'title': forms.TextInput(attrs = {'placeholder': 'Название списка'})
		}


# Форма для модели "задания"
class TaskForm(forms.ModelForm):
	class Meta:
		# Определение модели для формы
		model = Task
		# Определение полей, которые будут использоваться в форме
		fields = ['title', 'priority', 'slug']
		# Установка виджетов для полей и присваивание им специфичных атрибутов
		widgets = {
			'title': forms.TextInput(attrs = {'placeholder': 'Название задачи'}),
			'priority': forms.TextInput(),
			'slug': forms.TextInput()
		}