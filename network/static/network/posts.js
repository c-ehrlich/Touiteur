document.addEventListener('DOMContentLoaded', function() {
  // add mention links to post text
  document.querySelectorAll('.post-text, .single-post-view-text-div').forEach(post => {
    post_text_with_mention_links = create_post_text_with_mention_links(post.innerHTML);
    post.innerHTML = post_text_with_mention_links;
  });

  document.querySelectorAll('.post-edit-button').forEach(button => {
    button.addEventListener('click', event => {
      let post_id = button.id.split("-")[1];
      edit_post_text(post_id);
    });
  });

  document.querySelectorAll('.post-save-edits-button').forEach(button => {
    button.addEventListener('click', event => {
      let post_id = button.id.split("-")[1];
      let original_text = document.querySelector(`#post-text-${post_id}`).innerText;
      edit_post_submit(post_id, original_text);
    });
  });

  document.querySelectorAll('.post-edit-cancel-button').forEach(button => {
    button.addEventListener('click', event => {
      let post_id = button.id.split("-")[1];
      let original_text = document.querySelector(`#post-text-${post_id}`).innerText;
      edit_post_cancel(post_id, original_text);
    });
  });

  document.querySelectorAll('.post-like-button').forEach(button => {
    button.addEventListener('click', event => {
      let post_id = button.id.split("-")[3];
      like_post(post_id);
    }, { once: true } );
  });

  document.querySelectorAll('.post-unlike-button').forEach(button => {
    button.addEventListener('click', event => {
      let post_id = button.id.split("-")[3];
      unlike_post(post_id);
    }, { once: true } );
  })
});


// Add links to mentions in post text
function create_post_text_with_mention_links(post_text) {
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


// Cancels post editing
function edit_post_cancel(post_id, original_text) {
  document.querySelector(`#post-text-${post_id}`).innerHTML = original_text;
  // chenge visibility back to input view style
  document.querySelector(`#post-edit-container-${post_id}`).setAttribute('hidden', 'hidden');
  document.querySelector(`#post-text-${post_id}`).removeAttribute('hidden');
  // adjust button visibility
  document.querySelector(`#ecb-${post_id}`).setAttribute('hidden', 'hidden');
  document.querySelector(`#seb-${post_id}`).setAttribute('hidden', 'hidden');
  document.querySelector(`#eb-${post_id}`).removeAttribute('hidden');
}


// Attempts to submit edited post
function edit_post_submit(post_id, original_text) {
  let text_field = document.querySelector(`#post-text-${post_id}`);
  let text_edit_input = document.querySelector(`#post-edit-input-${post_id}`);
  let new_text = text_edit_input.value;
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
      text_field.innerHTML = create_post_text_with_mention_links(new_text);
    } else {
      text_field.innerHTML = create_post_text_with_mention_links(original_text);
      new Notify({
        status: 'error',
        title: 'Edit',
        text: gettext('Post Editing Failed'),
        effect: 'fade',
        speed: 300,
        customClass: null,
        customIcon: null,
        showIcon: true,
        showCloseButton: true,
        autoclose: true,
        autotimeout: 3000,
        gap: 20,
        distance: 20,
        type: 1,
        position: 'x-center top'
      })
    }
    text_field.removeAttribute('hidden');
    document.querySelector(`#post-edit-container-${post_id}`).setAttribute('hidden', 'hidden');

    // set button attributes
    document.querySelector(`#ecb-${post_id}`).setAttribute('hidden', 'hidden');
    document.querySelector(`#seb-${post_id}`).setAttribute('hidden', 'hidden');
    document.querySelector(`#eb-${post_id}`).removeAttribute('hidden');
  })
}


// Edits a post
function edit_post_text(post_id) {
  let text_field = document.querySelector(`#post-text-${post_id}`);
  let original_text = text_field.innerText;
  let text_edit_input = document.querySelector(`#post-edit-input-${post_id}`);
  // text_edit_input.setAttribute('rows', get_number_of_lines(original_text));
  text_edit_input.setAttribute('rows', 4);
  text_edit_input.value = original_text;
  text_field.setAttribute('hidden', 'hidden');
  document.querySelector(`#post-edit-container-${post_id}`).removeAttribute('hidden');
  text_edit_input.focus();

  // set button visibility
  document.querySelector(`#ecb-${post_id}`).removeAttribute('hidden');
  document.querySelector(`#seb-${post_id}`).removeAttribute('hidden');
  document.querySelector(`#eb-${post_id}`).setAttribute('hidden', 'hidden'); 
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
    document.querySelector(`#post-like-heart-${json.post_id}`).innerHTML = '<i class="fas fa-heart"></i>';
  } else {
    // remove class "unlike-button"
    like_button.classList.remove('post-unlike-button');
    // add class "like-button"
    like_button.classList.add('post-like-button');
    // set like eventlistener
    like_button.addEventListener('click', event => { like_post(json.post_id) }, { once: true });
    // make heart plain
    document.querySelector(`#post-like-heart-${json.post_id}`).innerHTML = '<i class="far fa-heart"></i>';
  }
  // set like count
  document.querySelector(`#post-like-count-${json.post_id}`).innerHTML = json.like_count;
}

console.log(gettext("loaded posts.js"));

// check if a char is alphanumeric
function is_alphanumeric(char) {
  return /[a-zA-Z0-9]/.test(char);
}

// check if a char is alhpanumeric or underscore
function is_alphanumeric_or_underscore(char) {
  return /[a-zA-Z0-9_]/.test(char);
}
