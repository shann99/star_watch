const hamburger = document.querySelector('.hamburger');
const navUL = document.querySelector('.nav-ul');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navUL.classList.toggle('active');
});

const acc = document.querySelector('.profile-button');
const acc_nav = document.querySelector('.login-nav');

acc.addEventListener('click', () => {
    // acc.classList.toggle('active');
    acc_nav.classList.toggle('active');
});


// document.querySelectorAll(".nav-item").forEach