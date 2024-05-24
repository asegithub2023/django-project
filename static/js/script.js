
document.addEventListener("DOMContentLoaded", function() {
    // Add event listener to profile image
    document.querySelector('.profile-image-container img').addEventListener('click', function() {
        // Redirect user to profile image update page when clicking on the image
        window.location.href = "{% url 'tutor_profile_update' %}";
    });
});
    



        