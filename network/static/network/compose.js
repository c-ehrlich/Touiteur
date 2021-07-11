document.addEventListener('DOMContentLoaded', function() {
  // add eventlistner to send tweet
  document.querySelector('#compose-form').onsubmit = send_post; 
});


// Sends a post
function send_post() {
  console.log("hello");
  text = document.querySelector('#compose-form-post-text').value;
  fetch('/compose', {
    method: 'POST',
    body: JSON.stringify({
      text: text
    }),
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  })
  // .then(response => response.json());
}


console.log("loaded index.js");
