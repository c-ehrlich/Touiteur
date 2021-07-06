console.log("loading js")

document.addEventListener('DOMContentLoaded', function() {
  // add eventlistner to sent email
  document.querySelector('#compose-form').onsubmit = send_post; 
  load_public_posts()
  document.querySelectorAll('.like-post-button').forEach(item => {
    item.addEventListener('click', event => {
      test_print();
    })
  })
});


function add_post(post) {
  const post_div = document.createElement('div');
  post_div.innerHTML = `${post}`;
  document.querySelector('#posts-view').append(post_div);
}


// Likes a post
function like_post(post_id) {
  
}


function load_public_posts() {
  fetch('/posts_public')
  .then(response => response.json())
  .then(posts => {
    // posts.forEach(post => add_post(post));
    console.log(posts);
  });
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


// TODO temp
function test_print() {
  console.log("test_print");
}