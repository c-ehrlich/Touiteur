document.addEventListener('DOMContentLoaded', () => {
  // send a request to make the thread 'read'
  const thread_id = document.querySelector('#thread-id');
  setMessagesRead(thread_id);
});

function setMessagesRead(thread_id) {
  /*
  * Mark all relevant messages in the thread as read
  */
  fetch(`/thread_read_status/${thread_id}`, {
    method: 'PUT',
    headers: {
      "X-CSRFToken": getCookie('csrftoken'),
    },
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Error marking thread as read');
  })
  .catch(error => {
    console.log(error);
  });
}