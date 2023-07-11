let narrowSearchYesButton = document.getElementById("narrow-search-yes-button")
let narrowSearchNoButton = document.getElementById("narrow-search-no-button")
let submitButton = document.getElementById("submit-button")

// Prevents this button from submitting the form
narrowSearchYesButton.addEventListener("click", function() {
    event.preventDefault()
    document.querySelector("#optional-song-input-section").style.display = "block"
});

// Prevents this button from submitting the form
narrowSearchNoButton.addEventListener("click", function() {
    event.preventDefault()
    document.querySelector("#optional-song-input-section").style.display = "none"
});

// Once form submitted, the optional paramters are hidden
submitButton.addEventListener("click", function() {
    document.querySelector("#optional-song-input-section").style.display = "none"
});