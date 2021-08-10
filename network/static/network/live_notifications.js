// How often the client should check for new notifications
const refreshTimeMS = 5000;

time = Date.now();

function checkForNotifications() {
  context = {};
  // get the path from the current url
  var path = window.location.pathname;
  // get the first alphanumeric string from the path
  var first = path.split('/')[1];
  context.location = first;
  if (first === "user" || first === "likes") {
    second = path.split('/')[2];
    context.username = second;
  }
  if (first === "") {
    context.location = "index";
  }
  // console.log(context.location);
  fetch('/notifications', {
    method: 'PUT',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      "timestamp": time,
      "context": context,
    }),
  })
  .then(response => {
    if (response.status === 200) {
      return response.json();
    }
    else {
      throw new Error('Error fetching notifications');
    }
  })
  .then(json => {
    const newPostsDiv = document.querySelector('#new-posts-inner');
    if (json.new_post_count > 0) {
      let data = {'count': json.new_post_count}
      const formats = ngettext(
        'There is %(count)s new post. Click to refresh.',
        'There are %(count)s new posts. click to refesh.',
        data.count
      );
      const string = interpolate(formats, data, true);
      newPostsDiv.innerHTML = `<i class="fas fa-redo-alt"></i>  ${string}`;
      newPostsDiv.removeAttribute('hidden');
    }
    else {
      newPostsDiv.innerHTML = '0';
      newPostsDiv.setAttribute('hidden', 'hidden');
    }
    if (json.hasOwnProperty('new_mention_count')) {
      if (json.new_mention_count > 0) {
        // update mention count in header
        const newMentionsCountDiv = document.querySelector('#new-mentions-count');
        newMentionsCountDiv.innerHTML = json.new_mention_count;
        newMentionsCountDiv.removeAttribute('hidden');
        // TODO temp hack because I can't figure out what sets this div to style display none
        newMentionsCountDiv.style.display = 'flex';
      }
    }
    if (json.hasOwnProperty('new_dm_count')) {
      if (json.new_dm_count > 0) {
        // update dm count in header
        const newDMsCountDiv = document.querySelector('#new-DMs-count');
        newDMsCountDiv.innerHTML = json.new_dm_count;
        newDMsCountDiv.removeAttribute('hidden');
      }
    }
  })
  .catch(error => {
    console.log(error);
  });

  // once completed, run again after refreshTimeMS
  setTimeout(checkForNotifications, refreshTimeMS);
}

// Start the check for notifications
var notification_interval = setTimeout(checkForNotifications, refreshTimeMS);
