document.addEventListener('DOMContentLoaded', () => {
  // add eventListener (once?) to all reply buttons
  document.querySelectorAll('.post-reply-button').forEach(button => {
    button.addEventListener('click', event => {
      postId = button.id.split('-')[1];
      showReplyUI(postId);
    })
  })
  document.querySelectorAll('.post-reply-cancel-button').forEach(button => {
    button.addEventListener('click', event => {
      postId = button.id.split('-')[1];
      hideReplyUI(postId);
    })
  })
  // Add eventListener to each send reply button
  document.querySelectorAll('.post-reply-submit').forEach(button => {
    button.addEventListener('click', () => {
      // form.preventDefault();
      postId = button.id.split('-')[1];
      sendReply(postId);
    })
  })
})

function showReplyUI(postId) {
  document.querySelector(`#prd-${postId}`).removeAttribute('hidden');
  document.querySelector(`#rb-${postId}`).setAttribute('hidden', 'hidden');
  document.querySelector(`#rcb-${postId}`).removeAttribute('hidden');
  document.querySelector(`#pri-${postId}`).focus();
}

function hideReplyUI(postId) {
  document.querySelector(`#prd-${postId}`).setAttribute('hidden', 'hidden');
  document.querySelector(`#rcb-${postId}`).setAttribute('hidden', 'hidden');
  document.querySelector(`#rb-${postId}`).removeAttribute('hidden');
}

function sendReply(postId) {
  // make a fetch request
  // if successful, clear the textbox, hide the reply UI, re-add the reply icon/eventListener,
    // and make some kind of indication (animation?) that the reply was sent successfully
  // if unsuccessful, keep the UI and show an error message?
  const postText = document.querySelector(`#pri-${postId}`).value;
  console.log("hi there");
  fetch(`/reply/${postId}`, {
    method: 'PUT',
    body: JSON.stringify({
      "text": postText,
    }),
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then(response => response.json())
  .then(json => {
    // update post reply count status (maybe the python function sends that to us?
    document.querySelector(`#pri-${postId}`).value = "";
    hideReplyUI(postId);
  })
  
  console.log("sending reply");
}