function openNav() {
    const navClass = document.getElementsByClassName("sidenav")[0];
    navClass.style.right = "0px"
    document.getElementById("overlay").style.display = "block";;
    
}

function closeNav() {
    const navClass = document.getElementsByClassName("sidenav")[0];
    navClass.style.right = "-420px"
    document.getElementById("overlay").style.display = "none";
}