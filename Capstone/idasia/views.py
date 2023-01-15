from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from .models import User, Profile, idea, category, thread, proj_files, replies
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.http import JsonResponse
from django.urls import reverse
import json
from django.utils.timezone import datetime
from .forms import UploadFileForm

def view_function(request):
    if request.user.is_authenticated:
        # User is authenticated, so render the template for authenticated users
        return render(request, 'idasia/index.html')
    else:
        # User is not authenticated, so render the template for anonymous users
        return render(request, 'idasia/about_us.html')
def index(request):
	categories = category.objects.all()
	return render(request, "idasia/index.html", 
		{"categories" : categories})

def joined(request):
	categories = category.objects.all()
	return render(request, "idasia/joined.html", 
		{"categories" : categories})

def projects(request):
	categories = category.objects.all()
	return render(request, "idasia/projects.html", 
		{"categories" : categories})

def aboutus_view(request):
	return render(request, "idasia/about_us.html")

def profile(request, profile_id):
	profile = Profile.objects.get(pk=profile_id)
	return render(request, "idasia/profile.html", {
		"profile" : profile
		})

def joinedProjects(request, category_id):
	p = Profile.objects.get(user = request.user)
	if category_id == "all":
		allideas = idea.objects.all().filter(proj_collaborator = p)
		allideas = allideas.order_by("-dateCreated").all()
		return JsonResponse([idea.serialize() for idea in allideas], safe=False,)
	else:
		c = category.objects.get(pk=category_id)
		allideas = idea.objects.all().filter(proj_collaborator = p).filter(proj_category = c)
		allideas = allideas.order_by("-dateCreated").all()
		return JsonResponse([idea.serialize() for idea in allideas], safe=False,)

def myProjects(request, category_id):
	p = Profile.objects.get(user = request.user)
	if category_id == "all":
		allideas = idea.objects.all().filter(proj_author = p)
		allideas = allideas.order_by("-dateCreated").all()
		return JsonResponse([idea.serialize() for idea in allideas], safe=False,)
	else:
		c = category.objects.get(pk=category_id)
		allideas = idea.objects.all().filter(proj_author = p).filter(proj_category = c)
		allideas = allideas.order_by("-dateCreated").all()
		return JsonResponse([idea.serialize() for idea in allideas], safe=False,)

def profile_projects(request, profile_id):
	p = Profile.objects.get(user = profile_id)
	allideas = idea.objects.all().filter(proj_author = p)
	allideas = allideas.order_by("-dateCreated").all()
	return JsonResponse([idea.serialize() for idea in allideas], safe=False,)

def allideas(request, category_id):
	if category_id == "all":
		allideas = idea.objects.all()
		allideas = allideas.order_by("-dateCreated").all()
		return JsonResponse([idea.serialize() for idea in allideas], safe=False,)
	else:
		c = category.objects.get(pk=category_id)
		allideas = idea.objects.all().filter(proj_category = c)
		allideas = allideas.order_by("-dateCreated").all()
		return JsonResponse([idea.serialize() for idea in allideas], safe=False,)

def show_idea(request, post_id):
	show_idea = idea.objects.get(pk=post_id)
	if request.method == "POST":
		js = json.loads(request.body)
		new_status = js["status"]
		idea.objects.filter(pk=post_id).update(proj_status = new_status)
		
		return JsonResponse({"result" : True}, status = 200)
	return render(request,"idasia/show_idea.html",{
		"idea" : show_idea,
		"categories" : show_idea.proj_category.all(),
		"collaboratos" : show_idea.proj_collaborator.all(),
		"status" : show_idea.proj_status,
		})

def close(request, idea_id):
	categories = category.objects.all()
	idea.objects.filter(pk=idea_id).update(proj_status = "Closed")
	return HttpResponseRedirect(reverse("index"))
def get_thread(request, thread_id):
	t = thread.objects.get(pk=thread_id)
	return JsonResponse([t.serialize()], safe=False,)

def get_file(request, file_id):
	f = proj_files.objects.get(pk = file_id)
	return JsonResponse([f.serialize()], safe=False)

def edit_description(request, post_id):
	if request.method == "POST":
		js = json.loads(request.body)
		new_description = js['description']
		idea.objects.filter(pk=post_id).update(proj_content = new_description)
		return JsonResponse({"result" : True}, status = 200)
def parse_idea(request, post_id):
	show_idea = idea.objects.get(pk=post_id)
	return JsonResponse([show_idea.serialize()], safe=False,)

def login_view(request):
	if request.method == "POST":
		username = request.POST['uname']
		password = request.POST['pass']

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "idasia/Log_in.html", {
				"message" : "Invalid credentials"
				})
	else:
		return render(request, "idasia/Log_in.html")

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("aboutus"))

def sign_up(request):
	if request.method == "POST":
		username = request.POST['uname']
		email = request.POST["email"]

		password = request.POST['pass']
		c_password = request.POST['c_pass']

		description = request.POST['desc']
		profession = request.POST['prof']
		Highest_edu_attain = request.POST['educ']
		contact_number = request.POST['cont']
		if password != c_password:
			return render(request, "idasia/sign_up.html", {
				"message" : "Passwords must match."
				})

		try:
			user = User.objects.create_user(username, email, password)
			profile = Profile.objects.create(user = user, description = description, profession = profession, Highest_edu_attain = Highest_edu_attain, contact_number = contact_number)
			user.save()
			profile.save()
		except IntegrityError:
			return render(request, "idasia/sign_up.html", {
				"message" : "Username is already taken"
				})
		login(request,user)
		return HttpResponseRedirect(reverse("index"))

	else:
		return render(request, "idasia/sign_up.html") 

@login_required
def new_thread(request, post_id):
	if request.method == "POST":
		form = UploadFileForm(request.POST, request.FILES)
		profile = Profile.objects.get(user=request.user)
		print("Valid form")
		g_idea = idea.objects.get(pk=post_id)
		content = request.POST['new_thread_content']
		datePosted = datetime.now()
		new_thread = thread(profile = profile, content = content, datePosted = datePosted)
		new_thread.save()
		if form.is_valid():
			for f in request.FILES.getlist('file'):
				print("One file ")
				p = proj_files.objects.create(uploader = profile, file = f)
				p.save()
				new_thread.thread_files.add(p)
		g_idea.thread.add(new_thread)
		if profile != g_idea.proj_author:
			if profile in g_idea.proj_collaborator.all():
				return HttpResponseRedirect(reverse("index"))
			else:
				g_idea.proj_collaborator.add(profile)
		return HttpResponseRedirect(reverse("idea", args=[post_id])) 
	form = UploadFileForm()
	return render(request, "idasia/new_thread.html", {
		"post_id":post_id,
		'form' : form
		})

@login_required
def newidea_view(request):
	categories = category.objects.all()
	if request.method == "POST":
		proj_author = Profile.objects.get(user=request.user)
		proj_title = request.POST["proj_title"]
		proj_content = request.POST["proj_content"]
		dateCreated = datetime.now()
		proj_category = request.POST.getlist('category')
		proj_objective = request.POST["proj_objective"]
		proj_location = request.POST["proj_location"]
		proj_background = request.POST["proj_background"]
		proj_status = request.POST["proj_status"]
		proj_image = request.POST["proj_image"]
		proj_cost = request.POST["proj_cost"]
		new_idea = idea(proj_author = proj_author, proj_title = proj_title, proj_content = proj_content, dateCreated = dateCreated, proj_objective = proj_objective, proj_location = proj_location, proj_background = proj_background, proj_status = proj_status, proj_image = proj_image, proj_cost = proj_cost)
		new_idea.save()

		for c_cat in proj_category:
			for cat in categories:
				if c_cat == cat.category_name:
					n = new_idea.proj_category.add(cat)
		return HttpResponseRedirect(reverse("index"))
	return render(request, "idasia/NewIdea.html", 
		{"categories" : categories})



@login_required
def reply(request, tr_id):
	if request.method == "POST":
		t = thread.objects.get(pk = tr_id)
		profile = Profile.objects.get(user = request.user)
		js = json.loads(request.body)
		reply = js['reply']
		r = replies(profile = profile, reply=reply)
		r.save()
		t.replies.add(r)
		return JsonResponse({"result" : True}, status = 200)
	else:
		r = replies.objects.get(pk = tr_id)
		return JsonResponse([r.serialize()], safe=False,)