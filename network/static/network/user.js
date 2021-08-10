document.addEventListener('DOMContentLoaded', () => {
  const view_user_id = document.querySelector('#user-id').innerHTML;
  if (document.querySelector('#follow-button')) {
    document.querySelector('#follow-button').addEventListener('click', event => {
      user_view_follow();
    })
  }
  if (document.querySelector('#unfollow-button')) {
    document.querySelector('#unfollow-button').addEventListener('click', event => {
      user_view_unfollow();
    })
  }
  if (document.querySelector('#block-button')) {
    document.querySelector('#block-button').addEventListener('click', event => {
      user_view_block();
    })
  }
  if (document.querySelector('#unblock-button')) {
    document.querySelector('#unblock-button').addEventListener('click', event => {
      user_view_unblock();
    })
  }
  if (document.querySelector('#share-profile-button')) {
    document.querySelector('#share-profile-button').addEventListener('click', event => {
      user_view_share_profile();
    })
  }
  if (document.querySelector('#user-profile-dropdown-button')) {
    document.querySelector('#user-profile-dropdown-button').addEventListener('click', event => {
      user_view_show_dropdown();
    })
  }
  window.addEventListener('click', event => {
    if (!(event.target.matches('.dropbtn')) && !(event.target.matches('.user-profile-hover-menu-icon'))) {
      if (document.querySelector('#user-profile-dropdown-content').classList.contains('show')) {
        document.querySelector('#user-profile-dropdown-content').classList.remove('show');
      }
    }
  })
})


function user_view_show_dropdown() {
  document.querySelector("#user-profile-dropdown-content").classList.toggle("show");
}


function user_view_block() {
  const view_user_id = document.querySelector('#user-id').innerHTML;
  block(view_user_id);
}


function user_view_unblock() {
  const view_user_id = document.querySelector('#user-id').innerHTML;
  unblock(view_user_id);
}


function user_view_share_profile() {
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
    text: gettext('User link copied to clipboard.'),
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


function user_view_follow() {
  const view_user_id = document.querySelector('#user-id').innerHTML;
  follow(view_user_id);
  const unfollow_button = document.createElement('button');
  unfollow_button.innerHTML = "Unfollow";
  unfollow_button.id = "unfollow-button";
  unfollow_button.classList.add('hero-button-bad');
  unfollow_button.addEventListener('click', user_view_unfollow);
  const follow_button_div = document.querySelector('#follow-button-div');
  follow_button_div.innerHTML = "";
  follow_button_div.append(unfollow_button);
  if (document.querySelector('#user-profile-follower-count') !== null) {
    follower_count_div = document.querySelector('#user-profile-follower-count');
    follower_count_div.innerHTML = parseInt(follower_count_div.innerHTML) + 1;
  }
}


function user_view_unfollow() {
  const view_user_id = document.querySelector('#user-id').innerHTML;
  unfollow(view_user_id);
  const follow_button = document.createElement('button');
  follow_button.innerHTML = "Follow";
  follow_button.id = "follow-button";
  follow_button.classList.add('hero-button-default');
  follow_button.addEventListener('click', user_view_follow);
  const follow_button_div = document.querySelector('#follow-button-div');
  follow_button_div.innerHTML = "";
  follow_button_div.append(follow_button);
  if (document.querySelector('#user-profile-follower-count') !== null) {
    follower_count_div = document.querySelector('#user-profile-follower-count');
    follower_count_div.innerHTML = parseInt(follower_count_div.innerHTML) - 1;
  }
}


console.log("loaded user.js");
