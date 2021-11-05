
// Clientside callbacks can be triggered from python
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_refresh_elements: function() {
            document.getElementById("refresh_scalars").classList.add("update");
            document.getElementById("refresh_timeseries").classList.add("update");
            return ["btn btn--refresh update", "btn btn--refresh update"]
        }
    }
});