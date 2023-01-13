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
const editor = document.getElementById('edit_button');
const card_container = document.querySelector('.card-container');

// editor.addEventListener('click', () => {

//     card_container.classList.toggle('active');
// });
// const closeEdit = document.getElementById("cancel_button");
// closeEdit.addEventListener('click', () => {
//     editmediaForm.style.display="none";
//     card_container.classList.remove('active');
// });