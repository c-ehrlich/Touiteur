function follow(user_id) {
  fetch(`/follow/${user_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      "intent": "follow"
    })
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
    })
  })
  .then(response => response.json())
  .then(json => {
    console.log(json);
  })
}

console.log("utils.js loaded");
