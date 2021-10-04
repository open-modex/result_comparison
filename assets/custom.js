
//function timer() {
//    check = document.getElementById("refresh_scalars");
//    if (check) {
//        document.getElementById("refresh_scalars").addEventListener("click", unsetRefresh);
//        document.getElementById("refresh_timeseries").addEventListener("click", unsetRefresh);
//        clearInterval(timerID);
//    }
//}
//
//function unsetRefresh() {
//    this.classList.remove("update");
//}
//
//let timerID = setInterval(timer, 250);


// Clientside callbacks can be triggered from python
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_refresh_elements: function() {
            document.getElementById("refresh_scalars").classList.add("update");
            return "btn btn--refresh update"
        }
    }
});