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
})