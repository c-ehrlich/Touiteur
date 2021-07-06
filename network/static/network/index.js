console.log("loading js")

document.addEventListener('DOMContentLoaded', function() {
  // add eventlistner to sent email
  document.querySelector('#compose-form').onsubmit = send_post; 
  document.querySelectorAll('.post-edit-button').forEach(button => {
    button.addEventListener('click', event => {
      post_id = button.id.split("-")[1];
      edit_post(post_id);
    })
  })
  document.querySelectorAll('.post-like-button').forEach(button => {
    button.addEventListener('click', event => {
      post_id = button.id.split("-")[1];
      like_post(post_id);
    })
  })
  document.querySelectorAll('.post-unlike-button').forEach(button => {
    button.addEventListener('click', event => {
      post_id = button.id.split("-")[1];
      unlike_post(post_id);
    })
  })
  // TODO condense like and unlike into the same button / eventlistener
});


// Edits a post
function edit_post(post_id) {
  console.log(`editing post ${post_id}`);
}


// Likes a post
function like_post(post_id) {
  console.log(`liking post ${post_id}`);
  // TODO create a condition to ensure 1. the user is logged in 2. they're not trying to like their own post
  // TODO check if the post is currently liked
  fetch(`/like/${post_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      like: true
    })
  })
  .then(response => response.json())
  .then(json => {
    console.log(json);
    update_post_like_status(json);
  })
    // update post like count
    // switch to unlike button
}


// Sends a post
function send_post() {
  text = document.querySelector('#post-text').value;
  fetch('/compose', {
    method: 'POST',
    body: JSON.stringify({
      text: text
    })
  })
  // .then(response => response.json());
}


// Unlikes a post
function unlike_post(post_id) {
  console.log(`unliking post ${post_id}`);
  // TODO create a condition to ensure 1. the user is logged in 2. they're not trying to like their own post
  fetch(`/like/${post_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      like: false
    })
  })
  .then(response => response.json())
  .then(json => {
    update_post_like_status(json);
  })
}


// Updates a post in the view
function update_post_like_status(json) {
  document.querySelector(`#post-likes-${json.post_id}`).innerHTML = json.like_count;
  button_div = document.querySelector(`#post-like-button-div-${json.post_id}`);
  button_div.innerHTML = "";

  // create new like/unlike button
  const like_button = document.createElement('button');
  if (json.is_liked == true) {
    // create unlike button
    like_button.innerHTML = "Unlike";
    like_button.classList.add('post-unlike-button');
    like_button.id = `post-unlike-button-${json.post_id}`;
    like_button.addEventListener('click', event => { unlike_post(json.post_id) });
  } else {
    like_button.innerHTML = "Like";
    like_button.classList.add('post-like-button');
    like_button.id = `post-like-button-${json.post_id}`;
    like_button.addEventListener('click', event => { like_post(json.post_id) });
  }
  button_div.append(like_button);
}