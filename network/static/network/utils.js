function block(user_id) {
  console.log("running block(user_id in utils.js");
  fetch(`/block_toggle/${user_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      "intent": "block",
    }),
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then(response => response.json())
  .then(json => {
    console.log(json);
    location.reload();
  })
}


function unblock(user_id, refresh_page) {
  // makes a backend request to unblock a user
  // the page will refresh by default
  // if false is passed to the optional refresh_page parameter, the page will not refresh
  refresh_page = (typeof refresh_page !== 'undefined') ? refresh_page : true;
  console.log("running unblock(user_id) in utils.js");
  console.log(refresh_page)
  fetch(`/block_toggle/${user_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      "intent": "unblock",
    }),
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then(response => response.json())
  .then(json => {
    console.log(json);
    if (!refresh_page) {
      location.reload();
    }
  })
}


/**
 * Determines how many lines to make the height of a Textarea for editing a tweet
 *
 * @param  {String} input_string     The text of a tweet
 * @return {int}    number_of_lines  The number of lines to make the textbox to edit that tweet
 */
function get_number_of_lines(input_string) {
    split_string = input_string.split(/\r\n|\r|\n/);
    number_of_lines = split_string.length;
    split_string.forEach(element => {
        number_of_lines += Math.floor(element.length / 55);
    })
    return number_of_lines;
}


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
  return cookieValue;
}


console.log("loaded utils.js");
