let menuState = false;
const toggleMenu = () => {
    if(menuState) {
        document.getElementById('hb-menu').style.display = "block";
        document.getElementById('bm-toggle-btn-open').style.display = "none";
        document.getElementById('bm-toggle-btn-close').style.display = "inline";
    } else {
        document.getElementById('hb-menu').style.display = "none";
        document.getElementById('bm-toggle-btn-open').style.display = "inline";
        document.getElementById('bm-toggle-btn-close').style.display = "none";
    }
    menuState = !menuState;
}

let updated = false;
setInterval(() => {
    if(screen.width > 1024) {
        document.getElementById('bm-toggle-btn-close').style.display = "none";
        document.getElementById('bm-toggle-btn-open').style.display = "none";
        updated = true;
    } else if(screen.width < 1024 && updated) {
        document.getElementById('bm-toggle-btn-open').style.display = "inline";
        updated = false;
    }

    if(screen.width > 1024 && document.getElementById('hb-menu').style.display == "block") {
        document.getElementById('hb-menu').style.display = "none";
        menuState = !menuState;
    }
    
},5);
