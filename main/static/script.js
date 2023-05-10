console.log('hello');
document.querySelectorAll(".copy-link").forEach((copyLinkParent) => {
    const inputField = copyLinkParent.querySelector(".copy-link-input");
    const copyButton = copyLinkParent.querySelector(".copy-link-button");
    const text = inputField.value;

    inputField.addEventListener("focus", () => inputField.select());

    copyButton.addEventListener("click", () => {
        inputField.select();
        navigator.clipboard.writeText(text);

        inputField.value = "Copied!";
        setTimeout(() => (inputField.value = text), 2000);
    });
});


// x.addEventListener("click", () => {
//     console.log("hello")
// })




function getFullscreenElement() {
    return document.fullscreenElement || document.webkitFullscreenElement || document.mozFullscreenElement || document.msFullscreenElement;
}
document.fullscreenElement


function toggleFullscreen() {
    if (getFullscreenElement()) {
        document.exitFullscreen();

    }
    else {
        document.documentElement.requestFullscreen().catch(console.log);
    }
}

let x = document.getElementById("exit");
let y = document.getElementById("full");
x.addEventListener('onclick',func);
y.addEventListener('onclick',func);
function func() {
    toggleFullscreen();
}

$(window).blur(function() {
    alert('You are not allowed to leave page blah blah');
    //do something else
 });

 

