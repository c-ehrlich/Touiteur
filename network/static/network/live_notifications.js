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
    if (first === "user") {
        second = path.split('/')[2];
        context.username = second;
    }
    if (first === "") {
        context.location = "index";
    }
    console.log(context.location);
    fetch('/new_posts', {
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
        if (response.status === 201) {
            return response.json();
        }
        else {
            throw new Error('Error fetching notifications');
        }
    })
    .then(json => {
        const newPostsDiv = document.querySelector('#new-posts-inner');
        if (json.new_post_count > 0) {
            if (json.new_post_count === 1) {
                newPostsDiv.innerHTML = '<i class="fas fa-redo-alt"></i> There is 1 new post. Click to refresh.';
            } else {
                newPostsDiv.innerHTML = `<i class="fas fa-redo-alt"></i> There are ${json.new_post_count} new posts. Click to refesh.`;
            }
            newPostsDiv.removeAttribute('hidden');
        }
        else {
            newPostsDiv.innerHTML = '0';
            newPostsDiv.setAttribute('hidden', 'hidden');
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
