let post_changer = {
    enabled: false,
    posts: [],
    current: undefined
}

// let post_changing_mode = false

document.addEventListener("keydown", (event) => {
    if (event.ctrlKey) {
        switch (event.key) {
            case "ArrowRight": {
                let next = document.getElementById("page-next").getAttribute("href");
                if (next === null) {
                    return;
                }
                window.location.href = next;
                console.log("right")
                return;
            }
            case "ArrowLeft": {
                let prev = document.getElementById("page-prev").getAttribute("href");
                if (prev === null) {
                    return;
                }
                window.location.href = prev;
                console.log("left")
                return;
            }
        }
    }
    if (event.ctrlKey && event.altKey) {
        switch (event.key) {
            case "l": {
                // enter post selection mode (navigate with arrow up/down)
                let posts = document.querySelectorAll("#posts .card[tabindex='-1']")
                console.log('l')
                // get first visible post
                let first_post = undefined
                let idx = undefined
                for(let i = 0; i < posts.length; i++) {
                    if (posts[i].getBoundingClientRect().top < 0) {
                        
                    } else {
                        first_post = posts[i+1];
                        idx = i+1;
                        break;
                    }
                }

                first_post.focus()
                post_changer.enabled = true
                post_changer.posts = posts
                post_changer.current = idx
            }
        }
    }
    if (post_changer.enabled) {
        switch (event.key) {
            case "ArrowDown": {
                if (post_changer.current != post_changer.posts.length) {
                    post_changer.posts[post_changer.current].nextElementSibling.nextElementSibling.focus()
                    post_changer.current += 1
                }
                break;
            }
            case "ArrowUp": {
                if (post_changer.current != 0) {
                    post_changer.posts[post_changer.current].previousElementSibling.previousElementSibling.focus()
                    post_changer.current -= 1
                }
            }
        }
    }
})
