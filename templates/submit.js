var zip = new JSZip();

function CreateZip() {
console.log("Create zip function is called");

// Assuming you have a form with the ID "SubmitForm"
  var form = document.getElementById("SubmitForm");

  // Prevent the default form submission
  form.addEventListener('submit', function (event) {
      event.preventDefault();

      zip.generateAsync({ type: "blob", compression: "default" }).then(function (content) {
          // Create a Blob from the content
          var zipBlob = new Blob([content], { type: "application/zip" });

          // Create FormData and append the Blob
          var formData = new FormData();
          formData.append('zipped_files', zipBlob, "name.zip");

          // Use jQuery AJAX for the request
          $.ajax({
              data: formData,
              url: 'http://localhost:5000/filesend',
              type: 'POST',
              processData: false,
              contentType: false,
              success: function (response) {
                  alert("success");
              }
          });
      });
  });
}