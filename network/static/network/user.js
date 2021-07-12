document.addEventListener('DOMContentLoaded', () => {
  const view_user_id = document.querySelector('#user-id').innerHTML;
  if (document.querySelector('#follow-button')) {
    document.querySelector('#follow-button').addEventListener('click', event => {
      user_view_follow(view_user_id);
    })
  }
  if (document.querySelector('#unfollow-button')) {
    document.querySelector('#unfollow-button').addEventListener('click', event => {
      user_view_unfollow(view_user_id);
    })
  }
})


function user_view_follow() {
  const view_user_id = document.querySelector('#user-id').innerHTML;
  follow(view_user_id);
  const unfollow_button = document.createElement('button');
  unfollow_button.innerHTML = "Unfollow";
  unfollow_button.id = "unfollow-button";
  unfollow_button.addEventListener('click', event => { user_view_unfollow() });
  follow_button_div = document.querySelector('#follow-button-div');
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
  follow_button.addEventListener('click', event => { user_view_follow() });
  follow_button_div = document.querySelector('#follow-button-div');
  follow_button_div.innerHTML = "";
  follow_button_div.append(follow_button);
  if (document.querySelector('#user-profile-follower-count') !== null) {
    follower_count_div = document.querySelector('#user-profile-follower-count');
    follower_count_div.innerHTML = parseInt(follower_count_div.innerHTML) - 1;
  }
}


console.log("loaded user.js");
