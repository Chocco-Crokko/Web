from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models import Count
import datetime

class QuestionManager(models.Manager):
	def newest(self):
		return self.order_by('-created')

	def hot(self):
		return self.order_by('-rating')

	def tag_search(self, input_tag):
		return self.filter(tags__text = input_tag)

	def published(self):
		return self.filter(is_published=True)

	def user_questions(self, user_name):
		return self.filter(user__username = user_name)

class ProfileManager(models.Manager):
    def best_users(self):
        return self.order_by('-rating')
    def get_by_name(self, user_name):
        return self.filter(user__username = user_name)

class TagManager(models.Manager):
    def with_question_count(self):
        return self.annotate(questions_count=Count('question'))

    def order_by_question_count(self):
        return self.with_question_count().order_by('-questions_count')

    def get_popular_tags(self):
        return self.order_by_question_count().all()[:10]

class Tag(models.Model):
    class Meta:
        verbose_name = u'Тэг'
        verbose_name_plural = u'Тэги'

    text = models.CharField(max_length=50, verbose_name='Тэг', unique=True)
    style_number = models.IntegerField(default=1, verbose_name=u'Номер')
    objects = TagManager()
    def __unicode__(self):
        return self.text

class Question(models.Model):
    class Meta:
        verbose_name = u'Вопрос'
        verbose_name_plural = u'Вопросы'

    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    title = models.CharField(max_length = 255, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')
    rating = models.IntegerField(default=0, verbose_name=u'Рейтинг')
    is_published = models.BooleanField(default=False, verbose_name=u'Опубликована')
    created = models.DateTimeField(default=datetime.datetime.now)
    tags = models.ManyToManyField(Tag, verbose_name=u'Тэг')
    id = models.IntegerField(unique=True, primary_key=True)
    objects = QuestionManager()

    def get_absolute_url(self):
        return '/question/id%d/' % self.id
    def __unicode__(self):
       return self.title

class Profile(models.Model):
    class Meta:
        verbose_name = u'Профиль'
        verbose_name_plural = u'Профили'

    user = models.OneToOneField(User, verbose_name=u'Пользователь')
    avatar = models.ImageField(upload_to='uploads', default="uploads/avatar2.jpg")
    information = models.TextField(verbose_name=u'Информация')
    rating = models.IntegerField(default=0, verbose_name=u'Рейтинг')
    objects = ProfileManager()

    def __unicode__(self):
	    return unicode(self.user)

class Answer(models.Model):
    class Meta:
	    verbose_name = u'Ответ'
	    verbose_name_plural = u'Ответы'

    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    question = models.ForeignKey(Question, verbose_name=u'Вопрос')
    text = models.TextField(verbose_name=u'Текст')
    rating = models.IntegerField(default = 0, verbose_name=u'Рейтинг')
    created = models.DateTimeField(default = datetime.datetime.now)
    is_correct = models.BooleanField(default = False, verbose_name=u'Корректность')

