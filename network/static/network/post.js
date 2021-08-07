document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('#follow-button')) {
    document.querySelector('#follow-button').addEventListener('click', post_view_follow);
  }
  if (document.querySelector('#unfollow-button')) {
    document.querySelector('#unfollow-button').addEventListener('click', post_view_unfollow);
  }
  if (document.querySelector('#block-button')) {
    document.querySelector('#block-button').addEventListener('click', post_view_block);
  }
  if (document.querySelector('#unblock-button')) {
    document.querySelector('#unblock-button').addEventListener('click', post_view_unblock);
  }
  if (document.querySelector('#share-post-button')) {
    document.querySelector('#share-post-button').addEventListener('click', post_view_share_post);
  }
  if (document.querySelector('#post-view-dropdown-button')) {
    document.querySelector('#post-view-dropdown-button').addEventListener('click', post_view_show_dropdown);
  }
  window.addEventListener('click', event => {
    if (!(event.target.matches('.dropbtn')) && !(event.target.matches('.post-view-hover-menu-icon'))) {
      if (document.querySelector('#post-view-dropdown-content').classList.contains('show')) {
        document.querySelector('#post-view-dropdown-content').classList.remove('show');
      }
    }
  })
})

function post_view_show_dropdown() {
  document.querySelector("#post-view-dropdown-content").classList.toggle("show");
}

function post_view_block() {
  const view_user_id = document.querySelector('#user-id').innerHTML;
  block(view_user_id);
}

function post_view_unblock() {
  const view_user_id = document.querySelector('#user-id').innerHTML;
  unblock(view_user_id);
}

function post_view_share_post() {
  const copy_dummy = document.createElement('input');
  const text = window.location.href;
  document.body.appendChild(copy_dummy);
  copy_dummy.value = text;
  copy_dummy.select();
  document.execCommand('copy');
  document.body.removeChild(copy_dummy);

  new Notify({
    status: 'success',
    // title: 'Notify Title',
    text: 'Post link copied to clipboard.',
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
}

function post_view_follow() {
  const view_user_id = document.querySelector('#user-id').innerHTML;
  follow(view_user_id);
  let unfollow_button = document.createElement('button');
  unfollow_button.innerHTML = "Unfollow";
  unfollow_button.id = "unfollow-button";
  unfollow_button.classList.add('hero-button-default');
  unfollow_button.addEventListener('click', post_view_unfollow);
  let follow_button_div = document.querySelector('#follow-button-div');
  follow_button_div.innerHTML = "";
  follow_button_div.appendChild(unfollow_button);
}

function post_view_unfollow() {
  const view_user_id = document.querySelector('#user-id').innerHTML;
  unfollow(view_user_id);
  let follow_button = document.createElement('button');
  follow_button.innerHTML = "Follow";
  follow_button.id = "follow-button";
  follow_button.classList.add('hero-button-default');
  follow_button.addEventListener('click', post_view_follow);
  let follow_button_div = document.querySelector('#follow-button-div');
  follow_button_div.innerHTML = "";
  follow_button_div.appendChild(follow_button);
}

console.log("loaded post.js")
