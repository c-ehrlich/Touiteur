document.addEventListener('DOMContentLoaded', function() {
  // add eventlistner to send tweet
  document.querySelector('#compose-form').onsubmit = send_post; 
});


console.log("loaded index.js")
