console.log("loading js")

document.addEventListener('DOMContentLoaded', function() {
  // add eventlistner to sent email
  document.querySelector('#compose-form').onsubmit = send_post; 
});


// Sends a post
function send_post() {
  text = document.querySelector('#post_text').value;
  console.log(text);
  fetch('/compose', {
    method: 'POST',
    body: JSON.stringify({
      text: text
    })
  })
  .then(response => response.json());
}
