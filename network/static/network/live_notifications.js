// How often the client should check for new notifications
const refreshTimeMS = 3000;

function checkForNotifications() {
    fetch('/get_notifications', {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
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
        const newMentionsCount = document.querySelector('#new-mentions-count');
        if (json.mention_count > 0) {
            newMentionsCount.innerHTML = json.mention_count;
            newMentionsCount.removeAttribute('hidden');
        }
        else {
            newMentionsCount.innerHTML = '0';
            newMentionsCount.setAttribute('hidden', 'hidden');
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
