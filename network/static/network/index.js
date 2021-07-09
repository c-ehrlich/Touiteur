document.addEventListener('DOMContentLoaded', function() {
  // add eventlistner to sent email
  document.querySelector('#compose-form').onsubmit = send_post; 
  document.querySelectorAll('.post-edit-button').forEach(button => {
    button.addEventListener('click', event => {
      post_id = button.id.split("-")[1];
      edit_post_text(post_id);
    }, { once: true } );
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


// Attempts to submit edited post
function edit_post_submit(post_id, original_text) {
  console.log(`submit edit on post ${post_id}`);
  const save_button = document.querySelector(`#eb-${post_id}`);
  const text_edit_input = document.querySelector(`#post-edit-input-${post_id}`);
  new_text = text_edit_input.value;
  fetch(`/edit/${post_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      new_text: new_text
    }),
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then(response => response.json())
  .then(json => {
    console.log(json);
    if (json.edited === true) {
      document.querySelector(`#post-text-${post_id}`).innerHTML = new_text;
    } else {
      document.querySelector(`#post-text-${post_id}`).innerHTML = original_text;
    }
    let save_button = document.querySelector(`#eb-${post_id}`);
    save_button.innerHTML = "Edit";
    save_button.addEventListener('click', event => {
      edit_post_text(post_id);
    }, { once: true } );
  })
  // TODO: do this without 'original_text' variable - use JSON from backend instead
}


// Edits a post
function edit_post_text(post_id) {
  console.log("edit post");
  const text_field = document.querySelector(`#post-text-${post_id}`);
  const original_text = text_field.innerHTML;
  text_field.innerHTML = "";
  const text_edit_input = document.createElement('textarea');
  text_edit_input.setAttribute('rows', 1);
  text_edit_input.setAttribute('maxlength', 500);
  // TODO set textArea cols? Or give it a class and then do it in CSS?
  // TODO give this textArea some classes
  text_edit_input.value = original_text;
  text_edit_input.id = `post-edit-input-${post_id}`;
  // TODO this eventListener doesn't work because enter makes a newline. Investigate.
  text_edit_input.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
      edit_post_submit(post_id, original_text);
    }
  }, { once: true } );
  text_field.append(text_edit_input);
  text_edit_input.focus();
  // Turn the edit button into save button
  let save_button = document.querySelector(`#eb-${post_id}`);
  save_button.innerHTML = "Save";
  save_button.addEventListener('click', event => {
    edit_post_submit(post_id, original_text);
  }, { once: true } );
  // add edit_post_save function eventListener to button and textfield
}


// Likes a post
function like_post(post_id) {
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
}


// Unlikes a post
function unlike_post(post_id) {
  // TODO create a condition to ensure 1. the user is logged in 2. they're not trying to like their own post
  // OR just do this in the django route
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

console.log("loaded index js")
