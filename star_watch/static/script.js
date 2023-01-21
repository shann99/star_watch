const hamburger = document.querySelector('.hamburger');
const navUL = document.querySelector('.nav-ul');
if(hamburger) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navUL.classList.toggle('active');
    });
}

const acc = document.querySelector('.profile-button');
const acc_nav = document.querySelector('.login-nav');
if (acc) {
    acc.addEventListener('click', () => {
        acc_nav.classList.toggle('active');
    });
}

const addItem = document.querySelector(".add-item");
const body = document.getElementsByTagName('body')[0];
if(addItem) {
    addItem.addEventListener('click', () => {
        addmediaForm.style.display="table";
        body.classList.toggle('active');
        addItem.style.display="none";
        addmediaForm.scrollIntoView({behavior: "smooth"});
    });
}
const closeForm = document.getElementById("mediaClose");
if(closeForm) {
    closeForm.addEventListener("click", () => {
        addmediaForm.style.display="none";
        body.classList.remove('active');
        addItem.style.display="inline-grid"
    });
}
const heart = document.getElementById('heart');
const filled = document.getElementById('heart_filled');
if (heart){
    heart.addEventListener("click", () => {
    filled.style.display="inline";
    heart.style.display='none';
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
    check.scrollIntoView({behavior: "smooth"});
    });
}
const cancel_delete = document.getElementById('cancel_check');
if(cancel_delete) {
    cancel_delete.addEventListener("click", () => {
    check.style.display='none';
    editmediaForm.style.display='table';
    });
}

const delete_account = document.getElementById("delete_acc_button");
const check_delete = document.querySelector(".check_acc_delete");
if(delete_account) {
    delete_account.addEventListener("click", () => {
        check_delete.style.display='table';
        accountForm.style.display='none';
        check_delete.scrollIntoView({behavior: "smooth"});
    });
}
const cancel_acc_delete = document.getElementById('cancel_delete');
if(cancel_acc_delete) {
    cancel_acc_delete.addEventListener("click", () => {
        check_delete.style.display='none';
        accountForm.style.display='table';
    });
}
const addTag = document.getElementsByClassName("addTagForm");
const add_button = document.getElementsByClassName("plus_tag_button");
const cancel_tag__button = document.getElementsByClassName("cancel_tag_button");
var item = "{{counter.count}}";
function openTag(item){
    addTag[item].style.display="inline";
    add_button[item].style.display="none";
    cancel_tag__button[item].classList.toggle("active");
}
function closeTag(item) {
    addTag[item].style.display="none";
    add_button[item].style.display="inline";
    cancel_tag__button[item].classList.remove("active");
}

const cardIMG = document.getElementsByClassName("card-image");
const tagDiv = document.getElementsByClassName("tag");
const heartsDiv = document.getElementsByClassName("heart_buttons");
const stats = document.getElementsByClassName("bottom_row");
const more = document.getElementsByClassName("see_more");
const less = document.getElementsByClassName("see_less");
const rating = document.getElementsByClassName("rating");
const desc = document.getElementsByClassName("description");
const card = document.getElementsByClassName("card-item");
const edit_button = document.getElementsByClassName("edit_button");
const edit_buttonB = document.getElementsByClassName("editButtonB");

function flipCardB(item) {
    cardIMG[item].style.display="none";
    tagDiv[item].style.display="none";
    heartsDiv[item].style.display="none";
    stats[item].style.display="none";
    more[item].style.display="none";
    edit_button[item].style.display="none";
    edit_buttonB[item].style.display="inline";
    less[item].style.display="inline";
    rating[item].style.display="inline";
    desc[item].style.display="inline";
    card[item].classList.toggle("active");
    
}
function flipCardA(item) {
    cardIMG[item].style.display="inline";
    tagDiv[item].style.display="inline";
    heartsDiv[item].style.display="inline";
    stats[item].style.display="inline";
    more[item].style.display="inline";
    edit_button[item].style.display="inline";
    less[item].style.display="none";
    rating[item].style.display="none";
    desc[item].style.display="none";
    edit_buttonB[item].style.display="none";
    card[item].classList.remove("active");
}