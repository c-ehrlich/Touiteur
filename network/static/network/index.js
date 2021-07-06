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
  .then(() => {
    // update post like count
    // switch to unlike button
  })
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
  fetch(`/unlike/${post_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      like: false
    })
  })
  .then(() => {
    // update post like count
    // switch to unlike button
  })
}
