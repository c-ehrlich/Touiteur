document.addEventListener('DOMContentLoaded', () => {
  const accountTab = document.querySelector('#account-tab');
  const blocklistTab = document.querySelector('#blocklist-tab');
  const preferencesTab = document.querySelector('#preferences-tab');
  
  const accountForm = document.querySelector('#account-form');
  const blocklistForm = document.querySelector('#blocklist-form');
  const preferencesForm = document.querySelector('#preferences-form');

  accountTab.addEventListener('click', event => {
    accountTab.classList.add('active-settings-tab');
    blocklistTab.classList.remove('active-settings-tab');
    preferencesTab.classList.remove('active-settings-tab');

    accountForm.removeAttribute('hidden')
    blocklistForm.setAttribute('hidden', 'true');
    preferencesForm.setAttribute('hidden', 'true');
  })

  blocklistTab.addEventListener('click', event => {
    accountTab.classList.remove('active-settings-tab');
    blocklistTab.classList.add('active-settings-tab');
    preferencesTab.classList.remove('active-settings-tab');

    accountForm.setAttribute('hidden', 'true');
    blocklistForm.removeAttribute('hidden');
    preferencesForm.setAttribute('hidden', 'true');
  })

  preferencesTab.addEventListener('click', event => {
    accountTab.classList.remove('active-settings-tab');
    blocklistTab.classList.remove('active-settings-tab');
    preferencesTab.classList.add('active-settings-tab');

    accountForm.setAttribute('hidden', 'true');
    blocklistForm.setAttribute('hidden', 'true');
    preferencesForm.removeAttribute('hidden');
  })

  const startTab = document.querySelector('#account-page-tab-start-value').innerHTML;
  if (startTab === 'account') {
    accountTab.classList.add('active-settings-tab');
    blocklistTab.classList.remove('active-settings-tab');
    preferencesTab.classList.remove('active-settings-tab');

    accountForm.removeAttribute('hidden')
    blocklistForm.setAttribute('hidden', 'true');
    preferencesForm.setAttribute('hidden', 'true');
  }
  if (startTab === 'blocklist') {
    accountTab.classList.remove('active-settings-tab');
    blocklistTab.classList.add('active-settings-tab');
    preferencesTab.classList.remove('active-settings-tab');

    accountForm.setAttribute('hidden', 'true');
    blocklistForm.removeAttribute('hidden');
    preferencesForm.setAttribute('hidden', 'true');;
  }
  if (startTab === 'preferences') {
    accountTab.classList.remove('active-settings-tab');
    blocklistTab.classList.remove('active-settings-tab');
    preferencesTab.classList.add('active-settings-tab');

    accountForm.setAttribute('hidden', 'true');
    blocklistForm.setAttribute('hidden', 'true');
    preferencesForm.removeAttribute('hidden');
  }

  document.querySelectorAll('.settings-unblock-button').forEach(button => {
    button.addEventListener('click', event => {
      let userId = button.getAttribute('userid');
      let userName = button.getAttribute('username');
      unblock(userId);
      unblockSettingsDOMManipulation(userId, userName);
    })
  })

  document.querySelector('#add-to-blocklist-button').addEventListener('click', event => {
    let userName = document.querySelector('#add-to-blocklist-input').value;
    blockUserFromUsername(userName);
  })
})


function blockUserFromUsername(userName) {
  fetch(`/block_toggle_username/${userName}`, {
    method: 'PUT',
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    credentials: 'same-origin',
    body: JSON.stringify({
      "intent": "block",
    })
  })
  .then(response => response.json())
  .then(json => {
    console.log(json);

  })
}


function unblockSettingsDOMManipulation(userId, userName) {
  document.querySelector(`#unblock-row-${userId}`).remove();
  new Notify({
    status: 'success',
    title: 'Blocklist',
    text: `Successfully removed @${userName}`,
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
  // TODO if there are no blocked users, show the "empty" thing
}