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




// Button Click
// let mapHandler = document.querySelector("#full");
// mapHandler.addEventListener("click", () => {
//       document.querySelector("iframe").requestFullscreen();
// });

// let exitButton = document.querySelector("#exit");
// exitButton.addEventListener("click", () => {
//       document.exitFullscreen();
// });


// let toggler = document.querySelector(".toggler");
// toggler.addEventListener("click", () => {
//     toggleFullscreen();
// });
// //Keyboard Key Press
// document.addEventListener("keydown", (e) => {
//   if (e.key === "Enter") {
//       toggleFullscreen();
//   }
// });


// toggleFullscreen = () => {
//     if (document.fullscreenEnabled) {
//       if (document.fullscreenElement) {
//         document.exitFullscreen();
//       } else {
//         document.documentElement.requestFullscreen();
//       }
//     } else {
//       alert("Fullscreen is not supported!");
//     }
//   }



