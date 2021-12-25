# Модуль для работы с моделями
from django.db import models
# Модуль для создания ссылки из значений name (url) 
# и дополнительный данных к примеру slug или id
from django.shortcuts import reverse
# Модуль для преобразования текста в slug
from django.utils.text import slugify
# Модуль для работы со временем
from time import time


# Функция для преобразования строки в slug
def gen_slug(s):
	new_slug = slugify(s,allow_unicode=True)
	# Для уникализации поля slug к нему прибавляеться значение time()
	return new_slug + '-' + str(int(time()))


# Модель объекта для хранения "списков"
class Schedule(models.Model):
	title = models.CharField(max_length=150, db_index=True)
	slug = models.SlugField(max_length=150, blank=True)

	# Получение ссылки на страницу, которая отображает все "задания"
	# выбранного "списка"
	def get_absolute_url(self):
		return reverse('detail_schedule_url', kwargs={'slug': self.slug})

	# Получение ссылки для удаления объекта из базы данных
	def get_delete_url(self):
		return reverse('delete_schedule_url', kwargs={'slug': self.slug})

	# Перед сохранение необходимо сгенерировать значение поля slug
	def save(self, *args, **kwargs):
		# Проверка - создается ли объект в первый раз
		if not self.id:
			# Если да, то генерируется slug на основе поля title данного
			# "списка"
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)

	# Если необходимо вывести объект - вывеедеться его поле title
	def __str__(self):
		return self.title
		

# Модель объекта для хранения "заданий"
class Task(models.Model):
	title = models.CharField(max_length=300, db_index=True)
	priority = models.CharField(max_length=50, blank=True)
	slug = models.SlugField(max_length=150, blank=True)

	# Получение ссылки для удаления выбранного "задания"
	def get_delete_url(self):
		return reverse('delete_task_url', kwargs={'slug': self.slug, 'id': self.id})

	# Если необходимо вывести объект - выведется значение его поля title
	def __str__(self):
		return self.title