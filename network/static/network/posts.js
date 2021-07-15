document.addEventListener('DOMContentLoaded', function() {
  // add mention links to post text
  document.querySelectorAll('.post-text, .single-post-view-text-div').forEach(post => {
    post_text_with_mention_links = create_post_text_with_mention_links(post.innerHTML);
    post.innerHTML = post_text_with_mention_links;
  });

  document.querySelectorAll('.post-edit-button').forEach(button => {
    button.addEventListener('click', event => {
      post_id = button.id.split("-")[1];
      edit_post_text(post_id);
    }, { once: true } );
  });

  document.querySelectorAll('.post-like-button').forEach(button => {
    button.addEventListener('click', event => {
      // TODO is there a better way to get the id?
      post_id = button.id.split("-")[3];
      like_post(post_id);
    }, { once: true } );
  });

  document.querySelectorAll('.post-unlike-button').forEach(button => {
    button.addEventListener('click', event => {
      post_id = button.id.split("-")[3];
      unlike_post(post_id);
    }, { once: true } );
  })
  // TODO condense like and unlike into the same button / eventlistener
});


// Add links to mentions in post text
function create_post_text_with_mention_links(post_text) {
  // TODO make sure there are no invalid characters in the username
  post_text_words = post_text.split(" ");
  post_text_with_mention_links = "";
  for (let i = 0; i < post_text_words.length; i++) {
    // check if the start of the word is a legitimate username
    if (post_text_words[i].startsWith("@") && is_alphanumeric(post_text_words[i][1]) && is_alphanumeric_or_underscore(post_text_words[i][2])) {
      // set username to characters 1 and 2 of the word
      username = post_text_words[i].substring(1, 3);
      // Keep going until you hit a chacracter that isn't alphanumeric or _, or the end of the string
      let index = 3;
      while (index < post_text_words[i].length && is_alphanumeric_or_underscore(post_text_words[i][index])) {
        username += post_text_words[i][index];
        index++;
      }
      post_text_with_mention_links += `<a href="/user/${username}">@${username}</a>`;
      // if the word continues after hitting a punctuation character, add the remainder in plaintext
      post_text_with_mention_links += post_text_words[i].substring(index) + " ";
    } else {
      post_text_with_mention_links += post_text_words[i] + " ";
    }
  }
  // remove whitespace from end of post_text_with_mention_links
  post_text_with_mention_links = post_text_with_mention_links.replace(/\s+$/, "");
  return post_text_with_mention_links;
}


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
    if (json.edited === true) {
      document.querySelector(`#post-text-${post_id}`).innerHTML = new_text;
    } else {
      document.querySelector(`#post-text-${post_id}`).innerHTML = original_text;
    }
    let save_button = document.querySelector(`#eb-${post_id}`);
    save_button.innerHTML = "Edit";
    save_button.classList.remove('post-save-edits-button');
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
  const number_of_lines = get_number_of_lines(original_text);
  text_edit_input.setAttribute('rows', number_of_lines);
  text_edit_input.setAttribute('maxlength', 500);
  // TODO set textArea cols? Or give it a class and then do it in CSS?
  // TODO give this textArea some classes
  text_edit_input.value = original_text;
  text_edit_input.id = `post-edit-input-${post_id}`;
  text_edit_input.classList.add('post-edit-input');
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
  save_button.classList.add('post-save-edits-button');
  save_button.addEventListener('click', event => {
    edit_post_submit(post_id, original_text);
  }, { once: true } );
  // add edit_post_save function eventListener to button and textfield
}


// Likes a post
function like_post(post_id) {
  fetch(`/like/${post_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      like: true
    }),
    headers: {
        "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then(response => response.json())
  .then(json => {
    // console.log(json);
    update_post_like_status(json);
  })
}


// Unlikes a post
function unlike_post(post_id) {
  fetch(`/like/${post_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      like: false
    }),
    headers: {
        "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then(response => response.json())
  .then(json => {
		// console.log(json)
    update_post_like_status(json);
  })
}


// Updates a post in the view
function update_post_like_status(json) {
  const like_button = document.querySelector(`#post-like-button-${json.post_id}`);
  if (json.is_liked == true) {
    // remove class "like-button"
    like_button.classList.remove('post-like-button');
    // add class "unlike-button"
    like_button.classList.add('post-unlike-button');
    // set unlike eventlistener
    like_button.addEventListener('click', event => { unlike_post(json.post_id) }, { once: true });
    // make heart red
    document.querySelector(`#post-like-heart-${json.post_id}`).innerHTML = '❤️'
  } else {
    // remove class "unlike-button"
    like_button.classList.remove('post-unlike-button');
    // add class "like-button"
    like_button.classList.add('post-like-button');
    // set like eventlistener
    like_button.addEventListener('click', event => { like_post(json.post_id) }, { once: true });
    // make heart plain
    document.querySelector(`#post-like-heart-${json.post_id}`).innerHTML = '‍♡'
  }
  // set like count
  document.querySelector(`#post-like-count-${json.post_id}`).innerHTML = json.like_count;
}

console.log("loaded posts.js");


// check if a char is alphanumeric
function is_alphanumeric(char) {
  return /[a-zA-Z0-9]/.test(char);
}

// check if a char is alhpanumeric or underscore
function is_alphanumeric_or_underscore(char) {
  return /[a-zA-Z0-9_]/.test(char);
}
