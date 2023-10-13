document.addEventListener("DOMContentLoaded", function() {
    var currentURL = window.location.href;
    var path = new URL(currentURL).pathname;

    document.getElementById("pathInput").value = path;


});


var refreshButton = document.getElementById("reload_btn");
refreshButton.addEventListener("click", function () {
    window.location.reload();
});


let accuracy = document.getElementById("accuracy_value").value
a = parseInt(accuracy)
b = 100 - a
let pie = new ej.charts.AccumulationChart({
    // Initializing Series
    series: [
        {
            dataSource: [
                { y: a }, {y: b },

            ],
            dataLabel: {
                visible: true,
                position: 'Inside',
            },
            xName: 'x',
            yName: 'y',
            radius: '100%',
            legendSettings: {
                visible: false,
            }
        }
    ],
});
pie.appendTo('#accuracy');

$(document).ready(function () {
    $("#myForm").submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "/post/",
            data: $(this).serialize(), 
            success: function (response) {
                var formattedHtml = '<h2 style="color: rgb(78, 78, 78);">Predicted Ressult</h2><h3>' + response.message + '</h3>';
                $("#response").html(formattedHtml);
            },
            error: function (xhr, errmsg, err) {
                $("#response").html("Error: " + xhr.status + " " + errmsg);
            }
        });
    });
});



// $(document).ready(function () {
//     $("#myForm").submit(function (event) {
//         event.preventDefault();

//         // Create an empty object to store form data
//         var formData = {};

//         // Iterate through form elements and add them to the formData object
//         $(this).find(":input").each(function () {
//             formData[this.name] = $(this).val();
//         });

//         // Convert formData object to JSON
//         var jsonData = JSON.stringify(formData);

//         // Send the JSON data in the AJAX request
//         $.ajax({
//             type: "POST",
//             url: "/post/",
//             data: jsonData,  // Send JSON data
//             contentType: "application/json", // Set content type to JSON
//             success: function (response) {
//                 console.log(response)
//                 var formattedHtml = '<h2 style="color: rgb(78, 78, 78);">Predicted Result</h2><h3>' + response.message + '</h3>';
//                 $("#response").html(formattedHtml);
//             },
//             error: function (xhr, errmsg, err) {
//                 $("#response").html("Error: " + xhr.status + " " + errmsg);
//             }
//         });
//     });
// });
