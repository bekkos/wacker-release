let menuState = true;
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

