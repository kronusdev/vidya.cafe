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
    targets: [], // elements
    current: undefined, // idx
    parent: undefined, // idx
    keymap: {
        up: ["ArrowUp", "k"],
        down: ["ArrowDown", "j"],
        left: ["ArrowLeft", "h"],
        right: ["ArrowRight", "l"],
        upvote: " ",
        interact: ["Enter", "f"]
    },

    current_obj(offset) {
        if(offset) {
            return navigation.targets[navigation.current + offset]
        } else {
            return navigation.targets[navigation.current]
        }
    },

    get parent_obj() {
        return this.targets[this.parent]
    },

    update_parent() {
        if (this.current_obj().getAttribute("data-focus-level") == 1 
        || !this.current_obj().hasAttribute("data-focus-level")) {
            
            if (this.current_obj().hasAttribute("data-focus-redirect")) {
                this.parent = this.targets.findIndex( (t) => {return t.getAttribute("data-focus-id") == this.current_obj().getAttribute("data-focus-redirect")})
            } else {
                this.parent = this.current
            }
            
        }
    },
    goDown() {
        for (let i = this.current+1; i < this.targets.length; i++) {
            if (
                (this.targets[i].getAttribute("data-focus-level") == 1 
                || !this.targets[i].hasAttribute("data-focus-level"))
                ) {
                    this.current = i
                focus_centered(this.targets[i])
                break;    
            }
        }
        
        
        this.enabled_this_press = false
    },

    goUp() {
        for (let i = this.current-1; i > -1; i--) {
            if (
                (this.targets[i].getAttribute("data-focus-level") == 1
                || !this.targets[i].hasAttribute("data-focus-level"))
                ) {
                this.current = i
                focus_centered(this.targets[i])
                break;    
            }
        }
        
        this.enabled_this_press = false   
    },

    goRight() {
        this.update_parent();

        for (let i = this.current+1; i < this.targets.length; i++) {
            if (this.targets[i].getAttribute("data-focus-level") > 1 
                && this.parent_obj.contains(this.targets[i])) {
 
                this.current = i
                focus_centered(this.current_obj())
                console.log(this.current)
                return;    
            }
        }
        // jump to beginning if at the end of secondary elements
        for (let i = this.parent+1; i < this.targets.length; i++) {
            if (this.targets[i].getAttribute("data-focus-level") > 1 
                && this.parent_obj.contains(this.targets[i])) {
 
                this.current = i
                focus_centered(this.current_obj())
                console.log(this.current)
                return;    
            }
        }
    },

    goLeft() {
        this.update_parent();
        for (let i = this.current-1; i > 0; i--) {
            if (this.targets[i].hasAttribute("data-focus-level")
            && this.parent_obj.contains(this.targets[i])) {
                this.current = i
                focus_centered(this.current_obj())
                return;
            }
        }
    }


}

function wrap_number(number, max) {
    console.log(number, max, (number % max + max)%max)
    return (number % max + max)%max
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
- To make the element be ignored during the initial focusing, give it the `data-focus-skip` attribute

*/


// let post_changing_mode = false








document.addEventListener("keydown", (event) => {

    if (navigation.enabled) {
        switch (event.key) {
            case navigation.keymap.down[0]: 
            case navigation.keymap.down[1]:{

                // up/down focuses only top level comments
                navigation.goDown();
                break;
            }
            case navigation.keymap.up[0]: 
            case navigation.keymap.up[1]: {
                
                // up/down focuses only top level comments
                navigation.goUp();
                break;
            }
            case navigation.keymap.right[0]: 
            case navigation.keymap.right[1]: {
                
                navigation.goRight();
                break;
            }
            case navigation.keymap.left[0]: 
            case navigation.keymap.left[1]: {
                
                navigation.goLeft();
                break;
            }
            case navigation.keymap.upvote: {
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

            case navigation.keymap.interact[0]: 
            case navigation.keymap.interact[1]: {
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
                    return t.getBoundingClientRect().top > 50 && (t.getAttribute("data-focus-level") == 1 || !t.hasAttribute("data-focus-level") && !t.hasAttribute("data-focus-skip")) 
                });
                console.log(idx_to_focus)
                    
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
