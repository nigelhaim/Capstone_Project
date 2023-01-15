document.addEventListener('DOMContentLoaded', function(){
	console.log("Showing all ideas");
	var user = JSON.parse(document.getElementById("signed_user").textContent);
	let user_f = user['user_id'];
	console.log("Signed in user is" + user_f);
	display_ideas("all");
});

function display_ideas(id){
	document.querySelector('#show-ideas').innerHTML = '';
	fetch('myProjects/' + id)
	.then(response => response.json())
	.then(idea => {
		console.log(idea);
		idea.forEach((idea) =>{
			if(idea.proj_status != "Closed"){
				
				var proj_id = idea.id;
				var profile_username = document.createTextNode("Created by: " + idea.proj_author);
				var proj_status = document.createTextNode(idea.proj_status);
				var proj_title = document.createTextNode(idea.proj_title + "| ");
				var dateCreated = document.createTextNode("Date posted " + idea.dateCreated);
				var num_collaborator = document.createTextNode("Collaborators: " + idea.proj_collaborator.length);
				var proj_category = document.createTextNode(String("Categories: " + idea.proj_category).replaceAll(",", " | "));
				var proj_location = idea.proj_location;
				var proj_image = document.createTextNode(idea.proj_image).wholeText;

				const idea_link = document.createElement('a');
				const idea_div = document.createElement('div');
				console.log(proj_image)
				const title = document.createElement('h2');
				const date = document.createElement('p');
				const author_name = document.createElement('h5');
				const collaborators = document.createElement('p');
				const categories = document.createElement('p');
				const status = document.createElement('h2');
				const location = document.createElement('img');
				const image = document.createElement('img');
				const title_status = document.createElement('div');
				
				title_status.setAttribute("class", "title-div");
				title.setAttribute('class', 'idea_title');
				image.setAttribute('src', proj_image);
				image.setAttribute('class', 'idea_image')
				location.setAttribute('class', 'location_flag');
				status.appendChild(proj_status);
				title.appendChild(proj_title);
				title.style.color="orangered";
				if(idea.proj_status == "Active"){
					status.style.color="green";
				}
				else if(idea.proj_status == "Planning"){
					status.style.color = "yellow";
				}
				else if(idea.proj_status == "On Hold"){
					status.style.color = "red";
				}
				else{
					status.style.color="orangered"
				}
				
				title_status.appendChild(title);
				title_status.appendChild(status);
				author_name.appendChild(profile_username);
				date.appendChild(dateCreated);
				collaborators.appendChild(num_collaborator);
				categories.appendChild(proj_category);

				fetch("https://restcountries.com/v3.1/all")
				.then(response=>response.json())
				.then(data=>{
					data.forEach(country => {
						//console.log(String(country.name.common));
						//console.log(proj_location);
						if(String(country.name.common) == proj_location){
							console.log("Found");
							let flag = country.flags.png;
							location.src = flag;

						};
					});
				});

				idea_div.appendChild(image);
				idea_div.appendChild(title_status);
				idea_div.appendChild(location);
				idea_div.appendChild(author_name);
				idea_div.appendChild(date);
				idea_div.appendChild(collaborators);
				idea_div.appendChild(categories);

				idea_div.setAttribute('id' , "idea_div");
				idea_link.appendChild(idea_div);
				proj = "/" + idea.id;
				idea_link.href = proj;
				document.querySelector('#show-ideas').append(idea_link);
			}
		});
	});
};

function changeCategory(category){
	console.log("Changed to " + category);
	document.getElementById('show-ideas').innerHTML = "";
	display_ideas(category);
}
