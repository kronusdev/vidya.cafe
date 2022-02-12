// NOTE: Taken from https://stackoverflow.com/a/4770179
// left: 37, up: 38, right: 39, down: 40,
// spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36
var keys = {32:1, 37: 1, 38: 1, 39: 1, 40: 1};

function preventDefault(e) {
  e.preventDefault();
}

function preventDefaultForScrollKeys(e) {
  if (keys[e.keyCode]) {
    preventDefault(e);
    return false;
  }
}

// modern Chrome requires { passive: false } when adding event
var supportsPassive = false;
try {
  window.addEventListener("test", null, Object.defineProperty({}, 'passive', {
    get: function () { supportsPassive = true; } 
  }));
} catch(e) {}

var wheelOpt = supportsPassive ? { passive: false } : false;
var wheelEvent = 'onwheel' in document.createElement('div') ? 'wheel' : 'mousewheel';

// call this to Disable
function disableScroll() {
  window.addEventListener('DOMMouseScroll', preventDefault, false); // older FF
  window.addEventListener(wheelEvent, preventDefault, wheelOpt); // modern desktop
  window.addEventListener('touchmove', preventDefault, wheelOpt); // mobile
  window.addEventListener('keydown', preventDefaultForScrollKeys, false);
}

// call this to Enable
function enableScroll() {
  window.removeEventListener('DOMMouseScroll', preventDefault, false);
  window.removeEventListener(wheelEvent, preventDefault, wheelOpt); 
  window.removeEventListener('touchmove', preventDefault, wheelOpt);
  window.removeEventListener('keydown', preventDefaultForScrollKeys, false);
}

let navigation = {
    enabled: false,
    type: "",
    enabled_this_press: false,
    targets: [],
    current: undefined,
    parent: undefined,

    current_obj(offset) {
        if(offset) {
            return navigation.targets[navigation.current + offset]
        } else {
            return navigation.targets[navigation.current]
        }
    }
}

function focus_centered(element) {
    element.focus()
    element.scrollIntoView({block: "center", behavior:"smooth"})
}

/* 

How to expand the keyboard navigation system:
- To mark an element as focusable without doing anything special, give it the `focusable-target` class
- To mark it as a child element give it the `data-focus-level` attribute with a number higher than 1.  Higher number <=> lower priority
- To make an element redirect focus to another element when interacted with (pressed enter), give it the `data-redirect-focus` attribute with the `focus-id` of the element to redirect to
- To set an objects focus-id, give it a `data-focus-id`
- To make the element focusable ONLY via redirect, give it the `data-weak-focus` attribute

*/


// let post_changing_mode = false

document.addEventListener("keydown", (event) => {

    if (navigation.enabled) {
        switch (event.key) {
            case "ArrowDown": {

                // up/down focuses only top level comments
                for (let i = navigation.current+1; i < navigation.targets.length; i++) {
                    if (
                        (navigation.targets[i].getAttribute("data-focus-level") == 1 
                        || !navigation.targets[i].hasAttribute("data-focus-level"))
                        && !navigation.targets[i].getAttribute("data-weak-focus")
                        ) {
                        navigation.current = i
                        focus_centered(navigation.targets[i])
                        break;    
                    }
                }
                
                
                navigation.enabled_this_press = false
                break;
            }
            case "ArrowUp": {
                
                // up/down focuses only top level comments
                for (let i = navigation.current-1; i > -1; i--) {
                    if (
                        (navigation.targets[i].getAttribute("data-focus-level") == 1
                        || !navigation.targets[i].hasAttribute("data-focus-level"))
                        && !navigation.targets[i].getAttribute("data-weak-focus")
                        ) {
                        navigation.current = i
                        focus_centered(navigation.targets[i])
                        break;    
                    }
                }
                
                navigation.enabled_this_press = false
                break;
            }
            case "ArrowRight": {
                
                if (navigation.current_obj().getAttribute("data-focus-level") == 1 
                || !navigation.current_obj().hasAttribute("data-focus-level")) {
                    
                    if (navigation.current_obj().hasAttribute("data-focus-redirect")) {
                        navigation.parent = navigator.targets.find( (t) => {return t.getAttribute("data-focus-id") == navigator.current_obj().getAttribute("data-focus-redirect")})
                    } else {
                        navigation.parent = navigation.current
                    }
                    
                }
                console.log(navigation.parent)
                for (let i = navigation.current+1; i < navigation.targets.length; i++) {
                    if (navigation.targets[i].getAttribute("data-focus-level") > 1 
                        && navigation.targets[navigation.parent].contains(navigation.targets[i])) {
                        
                        navigation.current = i
                        focus_centered(navigation.targets[i])
                        break;    
                    }
                }
                
                break;
            }
            case "ArrowLeft": {
                
                for (let i = navigation.current-1; i > 0; i--) {
                    if (navigation.targets[i].hasAttribute("data-focus-level")
                    && navigation.targets[navigation.parent].contains(navigation.targets[i])) {
                        navigation.current = i
                        focus_centered(navigation.targets[i])
                        break;
                    }
                }
                
                break;
            }
            case " ": {
                let up_arrow = navigation.current_obj().querySelector(".arrow-up")
                if (up_arrow != null) {
                    up_arrow.click()
                } 
                //else {
                //     // navigation.current_obj().click()
                //     navigation.current = navigation.targets.findIndex( (t) => {
                //         return t.getAttribute("data-focus-id") == navigation.current_obj().getAttribute("data-focus-redirect")
                //     });
                //     console.log(`redirecting to id ${navigation.current_obj().getAttribute("data-focus-id")}`)
                //     navigation.current_obj().focus()
                //     navigation.parent = navigation.current
                // }
                break;
            }

            case "Enter": {
                if (navigation.type == "frontpage") {
                    let pid = navigation.current_obj().getAttribute("id").replace('post-', '')
                    window.location.href = `/post/${pid}`
                }
                break;
            }
            default: {
                if (!navigation.enabled_this_press) {
                    navigation.enabled = false
                    enableScroll()
                    navigation.current_obj().blur()  
                } else {
                    navigation.enabled_this_press = false
                }
                break;
            }
        }
        return;
    }

    if (event.ctrlKey && event.altKey) {
        switch (event.key) {

            case "l": {

                let targets = Array.from(document.querySelectorAll(".focusable-target"))
                navigation.type = document.body.id

                console.log(targets)
                console.log('l')

                // enter post selection mode (navigate with arrow up/down)
                // get first visible post
                let idx_to_focus = undefined
                

                idx_to_focus = targets.findIndex( (t) => {
                    return t.getBoundingClientRect().top > 50 && (t.getAttribute("data-focus-level") == 1 || !t.hasAttribute("data-focus-level")) 
                });
                console.log(idx_to_focus)

                // for(let i = 0; i < targets.length; i++) {
                    
                //     if (!(targets[i].getBoundingClientRect().top < 0) && !targets[i].getAttribute("data-focus-weak")) {
                //         to_focus = targets[i+1];
                //         idx = i+1;
                //         break;
                //     }

                // }
                    
                navigation.current = idx_to_focus
                navigation.targets = targets
                navigation.enabled = true
                navigation.enabled_this_press = true
                disableScroll()
                focus_centered(navigation.current_obj())
                break;
                
            }

            case ",": {
                window.history.go(-1)
                break;
            }
            case ".": {
                window.history.go(1)
                break;
            }
        }
        return;
    }

    if (event.ctrlKey) {
        switch (event.key) {
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
        return;
    }

    // switch(event.key) {

    // }
})
