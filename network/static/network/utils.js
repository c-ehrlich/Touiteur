function follow(user_id) {
  fetch(`/follow/${user_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      "intent": "follow"
    }),
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then(response => response.json())
  .then(json => {
    console.log(json);
  })
}


function unfollow(user_id) {
  fetch(`/follow/${user_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      "intent": "unfollow"
    }),
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then(response => response.json())
  .then(json => {
    console.log(json);
  })
}


function getCookie(name) {
  // based on getCookie(name) function from django docs
  // but replaced jQuery.trim(string) with javascript string.trim() to eliminate dependency
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;}


console.log("utils.js loaded");
