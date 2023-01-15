document.addEventListener('DOMContentLoaded', function(){
 var idea = JSON.parse(document.getElementById("post_id").textContent);
 var user = JSON.parse(document.getElementById("signed_user").textContent);
 var user_username = JSON.parse(document.getElementById("user_username").textContent);
	console.log("Showing idea #" + idea['post_id']);
	fetch('parse/'+idea['post_id'])
	.then(response => response.json())
	.then(idea => {
		idea.forEach((idea)=>{
			var status = document.createTextNode(idea.proj_status);
			if(idea.proj_status == "Active"){
				document.getElementById('status').style.color = "Green";
			}
			else if(idea.proj_status == "Planning"){
				document.getElementById('status').style.color = "Yellow";
			}
			else if(idea.proj_status == "On Hold"){
				document.getElementById('status').style.color = "red";
			}
			else if(idea.proj_status == "Cancelled"){
				document.getElementById('status').style.color = "red";
			}
			else{
				document.getElementById('status').style.color = "orangered";
			};

			idea.thread.forEach((thread) => {
				fetch('getThread/' + thread)
				.then(response => response.json())
				.then(thr => {
					console.log(thr);
					thr.forEach((thr) => {
						if(idea.proj_status != "Closed"){
							
							var thr_id = thr.id
							console.log(thr.id);
							var profile = document.createTextNode(thr.profile);
							var content = document.createTextNode(thr.content);
							var datePosted = document.createTextNode(thr.datePosted);
							var o_reply = document.createTextNode("Show Thread");
							var c_reply = document.createTextNode("Close Thread");
							var uploaded_files_text = document.createTextNode("Uploaded files: ")
							
							const thread_div = document.createElement('div');
							const username = document.createElement('h2');
							const cont = document.createElement('p');
							const date = document.createElement('h5');
							const open_reply_button = document.createElement('button');
							const close_reply_button = document.createElement('button');
							const file_div = document.createElement('div');
							const uploaded_files = document.createElement('h3');

							const files = thr.files;
							files.forEach((file) => {
								//console.log(file)
								fetch('getThreadFile/' + file)
								.then(response => response.json())
								.then(file => {
									file.forEach((f) => {
										var filename = f.filename;
										var length = filename.length
										var new_filename = "Download: " + filename.substring(38,length)
										var path = filename.substring(7, length);
										//var path = "static/files/2023/01/14/Updated_01_13_2022.png";
										//console.log(path);
										const show_file = document.createElement('a');
										show_file.setAttribute('class' , 'thread_file');
										show_file.href = path;
										show_file.innerHTML = new_filename;
										file_div.appendChild(show_file);

										show_file.setAttribute('download', filename);
									})
								})
							})

							//Reply form
							const reply_div = document.createElement('div');
							const reply_input = document.createElement('input');
							const reply_submit = document.createElement('button');
							reply_input.setAttribute("name", "reply");
							reply_input.setAttribute("id", "reply");
							reply_input.setAttribute("placeholder", "Post your reply");
							reply_input.setAttribute("required", "");
							reply_submit.setAttribute("id", "reply_submit");
							reply_submit.innerHTML = "Post";

							reply_div.appendChild(reply_input);
							reply_div.appendChild(reply_submit);

							close_reply_button.style.display = "None";
							reply_div.style.display = "None";

							open_reply_button.addEventListener('click', function(){
								close_reply_button.style.display = "Block";
								reply_div.style.display = "Block";
								open_reply_button.style.display = "None";
							})
							close_reply_button.addEventListener('click', function(){
								close_reply_button.style.display = "None";
								reply_div.style.display = "None";
								open_reply_button.style.display = "Block";
							})
							
							reply_submit.addEventListener('click', () => reply(reply_input.value, thr.id));
							reply_submit.addEventListener('click', function(event){
								if(reply_input.value != ""){
									
									var uname = document.createTextNode(user_username);
									var u_rep = document.createTextNode(reply_input.value);

									const div_reply = document.createElement('div');
									const use = document.createElement('h4');
									const rep = document.createElement('p');

									use.setAttribute('class', 'reply_username');
									rep.setAttribute('class', 'reply_content');
									div_reply.setAttribute('class', 'div_reply')

									use.appendChild(uname);
									rep.appendChild(u_rep);

									div_reply.appendChild(use);
									div_reply.appendChild(rep);

									reply_div.appendChild(div_reply);
									reply_input.value = "";
								}
							})

							//Gets the replies of every thread
							const replies = thr.replies;
							replies.forEach((reply) => {
								console.log("Reply" + reply)
								fetch('/reply/' + reply)
								.then(response => response.json())
								.then(reply => {
									//console.log("Showing reply" + reply.id)
									reply.forEach((r) => {
										var username = document.createTextNode(r.username);
										var reply = document.createTextNode(r.reply);
										//console.log("Showing" + " " + username + " " + reply)

										const div_reply = document.createElement('div');
										const use = document.createElement('h4');
										const rep = document.createElement('p');

										use.setAttribute('class', 'reply_username');
										rep.setAttribute('class', 'reply_content');
										div_reply.setAttribute('class', 'div_reply')

										use.appendChild(username);
										rep.appendChild(reply);

										div_reply.appendChild(use);
										div_reply.appendChild(rep);

										reply_div.appendChild(div_reply)
									})
								})
							})

							username.appendChild(profile);
							date.appendChild(datePosted);
							cont.appendChild(content);
							open_reply_button.appendChild(o_reply);
							close_reply_button.appendChild(c_reply);
							uploaded_files.appendChild(uploaded_files_text);

							thread_div.setAttribute('class', 'thread_div');
							username.setAttribute('class', 'thread_uname');
							date.setAttribute('class', "thread_date");
							cont.setAttribute('class', "thread_cont");
							open_reply_button.setAttribute('class', 'open_reply_button')
							close_reply_button.setAttribute('class', 'close_reply_button')
							file_div.setAttribute('class', 'file_div');

							thread_div.appendChild(username);
							thread_div.appendChild(date);
							thread_div.appendChild(cont);
							thread_div.appendChild(uploaded_files);
							thread_div.appendChild(file_div);
							thread_div.appendChild(open_reply_button);
							thread_div.appendChild(close_reply_button);
							thread_div.appendChild(reply_div);

							document.querySelector("#show-threads").append(thread_div);
						}
					});
				});
			});
		});
	});
	document.getElementById('edit_description').style.display="None";
	document.getElementById('open_edit_description_button').addEventListener('click', () => show_edit_description());
	document.getElementById('close_edit_description_button').style.display="None";
	document.getElementById('close_edit_description_button').addEventListener('click', () => unshow_edit_description());

	document.getElementById('description_submit').addEventListener('click', () => update_description(idea['post_id']));
});


function show_edit_description(){
	document.getElementById('project_description').style.display="None";
	document.getElementById('close_edit_description_button').style.display="Block";
	document.getElementById('edit_description').style.display="Block";
	document.getElementById('open_edit_description_button').style.display="None";
}
function unshow_edit_description(){
	document.getElementById('project_description').style.display="Block";
	document.getElementById('close_edit_description_button').style.display="None";
	document.getElementById('open_edit_description_button').style.display="Block";
	document.getElementById('edit_description').style.display="None";
}


function update_status(post_id, status){
	var status = document.getElementById('update_status').value;
	console.log(post_id + " status updated to " + status);
	document.getElementById('status').innerHTML = status
	if(status == "Active"){
		document.getElementById('status').value = "Active";
		document.getElementById('status').style.color = "Green";
	}
	else if(status == "Planning"){
		document.getElementById('status').value = "Planning";
		document.getElementById('status').style.color = "Yellow";
	}
	else if(status == "On Hold"){
		document.getElementById('status').value = "On Hold";
		document.getElementById('status').style.color = "red";
	}
	else if(status == "Cancelled"){
		document.getElementById('status').value = "Cancelled";
		document.getElementById('status').style.color = "red";
	}
	else{
		document.getElementById('status').style.color = "orangered";
	}

	fetch('/' + post_id, {
		method: "POST",
		headers:{
			'X-CSRFToken': getCookie('csrftoken')
		},
		body:body = JSON.stringify({
			post_id : post_id,
			status : status,
		})
	})
	.then(response => response.json())
	.then(result => {
		console.log(result)
	})
}

function update_description(post_id){
	var description = document.getElementById('new_description').value;
	fetch('/editDescription/' + post_id, {
		method: "POST",
		headers:{
			'X-CSRFToken': getCookie('csrftoken')
		},
		body:body = JSON.stringify({
			post_id : post_id,
			description:description,
		})
	})
	.then(response => response.json())
	.then(result => {
		console.log(result)
		unshow_edit_description();
		document.getElementById('project_description').innerHTML = description
	})
}
function reply(reply, thread_id){
	fetch('/reply/' + thread_id, {
		method: "POST",
		headers:{
			'X-CSRFToken': getCookie('csrftoken')
		},
		body:body = JSON.stringify({
			thread_id : thread_id,
			reply:reply,
		})
	})
	.then(response => response.json())
	.then(result => {
		console.log(result);
	})
}
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;
            }
        }
    }

    return cookieValue;
}