document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('#follow-button')) {
    document.querySelector('#follow-button').addEventListerner('click', post_view_follow);
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
  if (document.querySelector('#share-profile-button')) {
    document.querySelector('#share-profile-button').addEventListener('click', post_view_show_profile);
  }
  if (document.querySelector('#post-view-dropdown-button')) {
    document.querySelector('#post-view-dropdown-button').addEventListener('click', post_view_show_dropdown);
  }
})