from django.db import models
from django.contrib.auth.models import AbstractUser
import mimetypes

# Create your models here.

class User(AbstractUser):
	pass

class Profile(models.Model):
	REQUIRED_FIELDS = ('user')
	user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True, related_name="user")
	description = models.CharField(max_length=500)
	profession = models.CharField(max_length=50)
	Highest_edu_attain = models.CharField(max_length=75, default="")
	contact_number = models.IntegerField()

class proj_files(models.Model):
	uploader = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="u_profile")
	file = models.FileField(upload_to='./idasia/static/idasia/files/%Y/%m/%d', blank=True)
	def getFile(self):
		return self.file
	def serialize(self):
		return{
			"uploader" : self.uploader.user.username,
			"file_path" : self.file.path,
			"filename" : self.file.name,
			"mime" : mimetypes.guess_type(self.file.name)
		}
class replies(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="r_profile")
	reply = models.CharField(max_length=900)
	def serialize(self):
		return{
			"id" : self.id,
			"username" : self.profile.user.username,
			"reply" : self.reply
		}
class thread(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="t_profile")
	content = models.CharField(max_length=500)
	datePosted = models.DateTimeField()
	thread_files = models.ManyToManyField(proj_files, blank=True, related_name="t_proj_files")
	replies = models.ManyToManyField(replies, blank=True, related_name="replies")
	def serialize(self):
		return{
			"id" : self.id,
			"profile" : self.profile.user.username,
			"content" : self.content, 
			"datePosted" : self.datePosted.strftime("%b %d %Y"),
			"files" : [file.id for file in self.thread_files.all()],
			"replies" : [reply.id for reply in self.replies.all()]
		}
class category(models.Model):
	category_name = models.CharField(max_length=500)

class idea(models.Model):
	proj_author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="i_profile")
	proj_title = models.CharField(max_length=50, default="")
	proj_content = models.CharField(max_length=500)
	dateCreated = models.DateTimeField()
	thread = models.ManyToManyField(thread, blank=True, related_name="thread")
	proj_category = models.ManyToManyField(category, blank=True, related_name="i_category")
	proj_collaborator = models.ManyToManyField(Profile, blank=True, related_name="collaborator")
	proj_objective = models.CharField(max_length=1000)
	proj_location = models.CharField(max_length=30)
	proj_background = models.CharField(max_length=1000)
	proj_status = models.CharField(max_length=20)
	proj_image = models.CharField(max_length=800, default="")
	proj_cost = models.IntegerField(blank=True, default=0)
	def serialize(self):
		return{
			"id" : self.id,
			"proj_author" :  self.proj_author.user.username,
			"proj_author_id" : self.proj_author.user.id,
			"proj_title" : self.proj_title,
			"proj_content" : self.proj_content,
			"dateCreated" : self.dateCreated.strftime("%b %d %Y"),
			"thread" : [thread.id for thread in self.thread.all()],
			"proj_category" : [category.category_name for category in self.proj_category.all()],
			"proj_collaborator" : [collaborator.user.username for collaborator in self.proj_collaborator.all()],
			"proj_objective" : self.proj_objective,
			"proj_location" : self.proj_location,
			"proj_background" : self.proj_background,
			"proj_status" : self.proj_status,
			"proj_image" : self.proj_image,
			"proj_cost" : self.proj_cost,
		}