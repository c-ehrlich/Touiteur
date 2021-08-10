document.addEventListener('DOMContentLoaded', () => {
  // add eventListener (once?) to all reply buttons
  document.querySelectorAll('.post-reply-button').forEach(button => {
    button.addEventListener('click', event => {
      postId = button.id.split('-')[1];
      showReplyUI(postId);
    })
  })
  document.querySelectorAll('.post-reply-cancel-button').forEach(button => {
    button.addEventListener('click', event => {
      postId = button.id.split('-')[1];
      hideReplyUI(postId);
    })
  })
  // Add eventListener to each send reply button
  document.querySelectorAll('.post-reply-submit').forEach(button => {
    button.addEventListener('click', () => {
      postId = button.id.split('-')[1];
      sendReply(postId);
    })
  })
  // Add eventListener to each post where user has blocked the author to show that post
  document.querySelectorAll('.blocked-by-user-reveal').forEach(button => {
    button.addEventListener('click', event => {
      postId = button.id.split('-')[1];
      console.log(`show ${postId}`);
      // hide stuff that needs to be hidden
      document.querySelectorAll(`.blk-info-${postId}`).forEach(item => {
        item.setAttribute('hidden', 'hidden');
      })
      // show stuff that needs to be shown
      document.querySelectorAll(`.blk-hidden-${postId}`).forEach(item => {
        // item.removeAttribute('hidden');
        item.classList.remove('blocked-by-user-hidden');
      })
    })
  })
})

function showReplyUI(postId) {
  document.querySelector(`#prd-${postId}`).removeAttribute('hidden');
  document.querySelector(`#rb-${postId}`).setAttribute('hidden', 'hidden');
  document.querySelector(`#rcb-${postId}`).removeAttribute('hidden');
  // const newHeight = document.querySelector(`#prd-${postId}`).style.height + 24;
  const div = document.querySelector(`#prd-${postId}`);
  const computedStyle = window.getComputedStyle(div);
  const newHeight = computedStyle.getPropertyValue('height');
  console.log(newHeight);
  document.querySelector(`#prslide-${postId}`).style.height = adjustPixelValueString(newHeight, 12);
  const textArea = document.querySelector(`#pri-${postId}`);
  textArea.focus();
  textArea.setSelectionRange(textArea.value.length, textArea.value.length);
}

function hideReplyUI(postId) {
  document.querySelector(`#prslide-${postId}`).style.height = 0;
  document.querySelector(`#prd-${postId}`).setAttribute('hidden', 'hidden');
  document.querySelector(`#rcb-${postId}`).setAttribute('hidden', 'hidden');
  document.querySelector(`#rb-${postId}`).removeAttribute('hidden');
}

function sendReply(postId) {
  // make a fetch request
  // if successful, clear the textbox, hide the reply UI, re-add the reply icon/eventListener,
    // and make some kind of indication (animation?) that the reply was sent successfully
  // if unsuccessful, keep the UI and show an error message?
  const postText = document.querySelector(`#pri-${postId}`).value;
  fetch(`/reply/${postId}`, {
    method: 'PUT',
    body: JSON.stringify({
      "text": postText,
    }),
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then(response => response.json())
  .then(json => {
    replyCount = json.reply_count;
    if (document.querySelector(`#prsd-${postId}`)) {
      document.querySelector(`#prsd-${postId}`).removeAttribute('hidden');

      const data = {'count': replyCount};
      const formats = ngettext(
        '%(count)s reply. Click to view.',
        '%(count)s replies. Click to view.',
        replyCount
      );
      const string = interpolate(formats, data, true);
      document.querySelector(`prl-${postId}`).innerHTML = string;

      new Notify({
        status: 'success',
        // title: 'Notify Title',
        text: gettext('Reply successfully posted.'),
        effect: 'fade',
        speed: 300,
        customClass: null,
        customIcon: null,
        showIcon: true,
        showCloseButton: true,
        autoclose: true,
        autotimeout: 3000,
        gap: 20,
        distance: 20,
        type: 1,
        position: 'x-center top'
      })
    } else {
      location.reload();
    }
    document.querySelector(`#pri-${postId}`).value = "";
    hideReplyUI(postId);
  })
}

//////
//////
//////
function adjustPixelValueString(input, change) {
  // input: a pixel value as a string, example: "20px"
  // input: an integer describing how many pixels to add or subtract, example: -5
  // output: a new pixel value as a string, example: "15px"
  let pixelValue = parseInt(input);
  pixelValue += change;
  return pixelValue + "px";
}
