document.addEventListener("keydown", (event) => {
    if(event.ctrlKey) {
        switch(event.key) {
            case "ArrowRight": {
                let next = document.getElementById("page-next").getAttribute("href");
                if (next === null) {
                    break;
                }
                window.location.href = next;
                console.log("right")
                break; 
            }
            case "ArrowLeft": {
                let prev = document.getElementById("page-prev").getAttribute("href");
                if (prev === null) {
                    break;
                }
                window.location.href = prev;
                console.log("left")
                break;
            }
        }
    }
})
