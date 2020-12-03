Dropzone.autoDiscover = false;

Dropzone.options.myDropzone= {
    url: 'upload/',
    autoProcessQueue: false,
    uploadMultiple: true,
    parallelUploads: 5,
    maxFiles: 5,
    // maxFilesize: 1,
    // acceptedFiles: 'image/*',
    // addRemoveLinks: true,
    init: function() {
        dzClosure = this; // Makes sure that 'this' is understood inside the functions below.

        // for Dropzone to process the queue (instead of default form behavior):
        document.getElementById("submit-all").addEventListener("click", function(e) {
            // Make sure that the form isn't actually being sent.
            e.preventDefault();
            e.stopPropagation();
            dzClosure.processQueue();
        });

        //send all the form data along with the files:
        this.on("sendingmultiple", function(data, xhr, formData) {
            formData.append("firstname", jQuery("#firstname").val());
            formData.append("lastname", jQuery("#lastname").val());
        });
    }
}

// Dropzone.options.myDropzone = {

//     // Prevents Dropzone from uploading dropped files immediately
//     autoProcessQueue : false,
//     paramName: "files",

//     init : function() {
//         var submitButton = document.querySelector("#submit-all")
//         myDropzone = this;

//         submitButton.addEventListener("click", function() {
//             myDropzone.processQueue();
//             // Tell Dropzone to process all queued files.
//         });

//         // You might want to show the submit button only when
//         // files are dropped here:
//         this.on("addedfile", function() {
//             // Show submit button here and/or inform user to click it.
//         });

//     }
// };

// Dropzone.options.myDropzone = {
//     autoProcessQueue : false,
//     uploadMultiple: true,
  
//     init : function() {
//       myDropzone = this;
  
//       this.element.querySelector("input[type='submit']").addEventListener('click', function(event) {
//         event.preventDefault();
//         event.stopPropagation();
//         myDropzone.processQueue();
//       });
//     }
//   }
// Dropzone.options.myDropzone= {
//     url: 'upload/',
//     autoProcessQueue: false,
//     uploadMultiple: true,
//     parallelUploads: 5,
//     maxFiles: 5,
//     maxFilesize: 1,
//     acceptedFiles: 'image/*',
//     addRemoveLinks: true,
//     init: function() {
//         dzClosure = this; // Makes sure that 'this' is understood inside the functions below.

//         // for Dropzone to process the queue (instead of default form behavior):
//         document.getElementById("submit-all").addEventListener("click", function(e) {
//             // Make sure that the form isn't actually being sent.
//             e.preventDefault();
//             e.stopPropagation();
//             dzClosure.processQueue();
//         });

//         //send all the form data along with the files:
//         this.on("sendingmultiple", function(data, xhr, formData) {
//             formData.append("firstname", jQuery("#firstname").val());
//             formData.append("lastname", jQuery("#lastname").val());
//         });
//     }
// }

function overlay() {
	el = document.getElementById("overlay");
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}