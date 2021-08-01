document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('#compose-pic-preview-img') !== null) {
    const uploadDiv = document.querySelector('#compose-form-image');

    uploadDiv.addEventListener('click', event => {
      uploadDiv.value = null;
    });

    // when a file is uploaded to the #id-avatar input
    uploadDiv.addEventListener('change', function(event) {
      // create a temp path to the file, and then put that file in #profile-pic-preview-img
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        document.querySelector('#compose-pic-preview-img').src = reader.result;
        document.querySelector('#compose-pic-preview-img').removeAttribute('hidden');
      }
      reader.readAsDataURL(file);
    });
  }
});

console.log("loaded image_uploads_compose.js");