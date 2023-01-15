from django.urls import path 
from . import views
urlpatterns = [
	path("", views.view_function, name="home"),
	path("joined", views.joined, name="joined"),
	path("projects", views.projects, name="projects"),
	path("index", views.index, name="index"),
	path("logout", views.logout_view, name="logout"),
	path("signup", views.sign_up, name="signup"),
	path("login", views.login_view, name="login"),
	path("aboutus", views.aboutus_view, name="aboutus"),
	path("allideas/<str:category_id>", views.allideas, name="allideas"),
	path("newidea", views.newidea_view, name="newidea"),
	path("<int:post_id>", views.show_idea, name="idea"),
	path("parse/<int:post_id>", views.parse_idea, name="parse_idea"),
	path("editDescription/<int:post_id>", views.edit_description, name="edit_description"),
	path("NewThread/<int:post_id>", views.new_thread, name="new_thread"),
	path("getThread/<int:thread_id>", views.get_thread, name="get_thread"),
	path("getThreadFile/<int:file_id>", views.get_file, name="get_file"),
	path("reply/<int:tr_id>", views.reply, name="reply"),
	path("joinedProjects/<str:category_id>", views.joinedProjects, name="joined_projects"),
	path("profile/myProjects/<str:category_id>", views.myProjects, name="my_projects"),
	path("myProjects/<str:category_id>", views.myProjects, name="my_projects"),
	path("profile/<str:profile_id>", views.profile, name="view_profile"),
	path("profile/profile_projects/<str:profile_id>", views.profile_projects, name="v_profile"),
	path("close/<str:idea_id>", views.close, name='close'),
	
]