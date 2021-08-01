document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('#id_avatar') !== null) {
    const uploadDiv = document.querySelector('#id_avatar');

    uploadDiv.addEventListener('click', event => {
      uploadDiv.value = null;
    });

    // when a file is uploaded to the #id-avatar input
    uploadDiv.addEventListener('change', function(event) {
      // create a temp path to the file, and then put that file in #profile-pic-preview-img
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        document.querySelector('#profile-pic-preview-img').src = reader.result;
      }
      reader.readAsDataURL(file);

      // set the element '#custom-file-upload-helper-text' to display: block
      document.querySelector('#custom-file-upload-helper-text').style.display = 'block';
    });
  }
});

console.log("loaded image_uploads.js");