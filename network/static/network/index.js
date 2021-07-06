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
});


// Edits a post
function edit_post(post_id) {
  console.log(`editing post ${post_id}`);
}


// Likes a post
function like_post(post_id) {
  console.log(`liking post ${post_id}`);
}


// Sends a post
function send_post() {
  text = document.querySelector('#post-text').value;
  console.log(text);
  fetch('/compose', {
    method: 'POST',
    body: JSON.stringify({
      text: text
    })
  })
  // .then(response => response.json());
}
