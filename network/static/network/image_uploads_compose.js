document.addEventListener('DOMContentLoaded', () => {
  // check if an #id-avatar element exists
    if (document.getElementById('post-image-upload')) {
      console.log("found it!");
    }

    if (document.querySelector('#post-image-upload') !== null) {

      document.querySelector('#id_avatar').addEventListener('click', event => {
        document.querySelector('#id_avatar').value = null;
        console.log("set #id_avatar to null");
      });

      // when a file is uploaded to the #id-avatar input
      document.querySelector('#id_avatar').addEventListener('change', function(event) {
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