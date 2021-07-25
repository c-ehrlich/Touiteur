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
  document.querySelectorAll('.post-reply-form').forEach(form => {
    form.addEventListener('submit', () => {
      // form.preventDefault();
      postId = form.id.split('-')[1];
      sendReply(postId);
    })
  })
})

function showReplyUI(postId) {
  document.querySelector(`#prd-${postId}`).removeAttribute('hidden');
  document.querySelector(`#rb-${postId}`).setAttribute('hidden', 'hidden');
  document.querySelector(`#rcb-${postId}`).removeAttribute('hidden');
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
  console.log("sending reply");
  document.querySelector(`#pri-${postId}`).value = "";
  hideReplyUI(postId);
}