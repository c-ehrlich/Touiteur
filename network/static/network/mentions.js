"use-strict";

document.addEventListener('DOMContentLoaded', () => {
    // send a fetch request to /clear_mentions_count
    // This should ONLY run when the user wants to clear their mentions
    // ie when they visit their notifications page
    if (document.getElementById('new-mentions-count') !== null) {
        fetch('/clear_mentions_count', {
            method: 'PUT',
            body: JSON.stringify({
                "intent": "clear_mentions_count"
            }),
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
        })
        .then(response => {
            document.getElementById('new-mentions-count').style.display = "none";
        });
    }
});