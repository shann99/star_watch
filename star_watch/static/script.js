const hamburger = document.querySelector('.hamburger');
const navUL = document.querySelector('.nav-ul');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navUL.classList.toggle('active');
});

const acc = document.querySelector('.profile-button');
const acc_nav = document.querySelector('.login-nav');

acc.addEventListener('click', () => {
    acc_nav.classList.toggle('active');
});

const addItem = document.querySelector(".add-item");
const body = document.getElementsByTagName('body')[0];
addItem.addEventListener('click', () => {
    addmediaForm.style.display="table";
    body.classList.toggle('active');
    addItem.style.display="none";
    addmediaForm.scrollIntoView(true);
});
const closeForm = document.getElementById("mediaClose");
closeForm.addEventListener("click", () => {
    addmediaForm.style.display="none";
    body.classList.remove('active');
    addItem.style.display="inline-grid"
});
const heart = document.getElementById('heart');
const fav = document.getElementById('fav');
const filled = document.getElementById('heart_filled');
if (heart){
    heart.addEventListener("click", () => {
    filled.style.display="inline";
    heart.style.visibility='hidden';
    });
}
if (filled) {
    filled.addEventListener("click", () => {
    filled.style.display='none';
    heart.style.visibility='visible';
    });
}
const delete_button = document.getElementById('delete_button');
const check = document.querySelector(".check_delete");
if(delete_button) {
    delete_button.addEventListener('click', () => {
    check.style.display='table';
    editmediaForm.style.display='none';
    });
}
const cancel_delete = document.getElementById('cancel_check');
if(cancel_delete) {
    cancel_delete.addEventListener("click", () => {
    check.style.display='none';
    editmediaForm.style.display='table';
    });
}