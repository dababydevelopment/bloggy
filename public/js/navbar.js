//define variable to store the ACTIVE id
let active;
//define variable (array/list) to store INACTIVE ids
let inactive = "";
const nav_click = (id) => {
    //first, find another "tab" that has the "active" class, and remove it.
    Array.from(document.getElementsByClassName("tab")).forEach((e) => {
        if (e.id != id) {
            inactive+=e.id+",";
            e.classList.remove("active");
        }
    });
    //next, set the tab with the provided id to class "active"
    let tab = document.getElementById(id);
    tab.classList.add("active");
    //set the variable (active_id) to equal "id"
    active = tab.id;
    //create cookies containing active and inactive
    document.cookie = "selected=" + active;
    document.cookie = "inactive=" + inactive;
}

const get_cookie = (name) => {
    let end_t = "";
    (document.cookie.split(';')).some((n) => {
        if (n.includes(name)) {
            //here: name
            end_t = n.split('=')[1];
        }
    });
    return end_t;
}
document.getElementById(get_cookie('selected')).classList.add('active');

(get_cookie('inactive')).split(',').forEach((e) => {
    if (e != "") {
        e.replace(",", "");
        document.getElementById(e).classList.remove('active');
    }
});