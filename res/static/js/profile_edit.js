let field_ids = ['age', 'country', 'job', 'about_user'];
let edit_butt = document.getElementById('edit');
let submit_butt = document.getElementById('submit');
let cancel_butt = document.getElementById('cancel');
let load_butt = document.getElementById('avatar');
let form = document.getElementById('form');


function enEditing() {
    field_ids.forEach((id) => {
        let elem = document.getElementById(id);
        elem.disabled = false;
    });
    edit_butt.style.visibility = 'hidden';
    edit_butt.disabled = true;
    submit_butt.style.visibility = 'visible';
    submit_butt.disabled = false;
    cancel_butt.style.visibility = 'visible';
    cancel_butt.disabled = false;
    load_butt.style.visibility = 'visible';
    load_butt.disabled = false;
}

function cancelEditing() {
    field_ids.forEach((id) => {
        let elem = document.getElementById(id);
        elem.disabled = true;
    });
    edit_butt.style.visibility = 'visible';
    edit_butt.disabled = false;
    submit_butt.style.visibility = 'hidden';
    submit_butt.disabled = true;
    cancel_butt.style.visibility = 'hidden';
    cancel_butt.disabled = true;
    load_butt.style.visibility = 'hidden';
    load_butt.disabled = true;
    form.reset();
}