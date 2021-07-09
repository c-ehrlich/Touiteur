function follow(user_id) {
  fetch(`/follow/${user_id}`, {
    method: 'PUT',
  })
  .then(response => response.json())
  .then(json => {
    console.log(json);
  })
}


// TODO temp test
function testfn() {
console.log("test");
}

console.log("utils.js loaded");
