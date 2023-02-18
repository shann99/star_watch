var item = "{{counter.count}}";

const hamburger = document.querySelector('.hamburger');
const ham_nav = document.querySelector('.hamburger_navigation');
if(hamburger) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        if(ham_nav.style.display != 'flex') {
            ham_nav.style.display = 'flex'; 
        }
       else {
        ham_nav.style.display = 'none'; 
       }
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
        addmediaForm.style.display="flex";
        body.classList.toggle('active');
        addItem.style.display="none";
        addmediaForm.scrollIntoView({behavior: "smooth", block:"center", inline: "end"});
    });
}
const closeForm = document.getElementById("mediaClose");
if(closeForm) {
    closeForm.addEventListener("click", () => {
        addmediaForm.style.display="none";
        body.classList.remove('active');
        addItem.style.display="flex";
    });
}
const heart = document.getElementsByClassName('heart');
const filled = document.getElementsByClassName('heart_filled');
const hearts = document.getElementsByClassName('hearts');
var card_id = '{{card.id}}';
var card_fav = "{{card.fav}}";
var heartItem = "{{counter.count}}";
function hearted(card_id, heartItem) {
    $(document).ready(function() {
        console.log(heartItem);
        $.ajax({
            type: "POST",
            url: "/fav",
            data: {"card_id": card_id, "card_fav": true},
            success: function() {
                $(hearts[heartItem]).load(' .heart_buttons:eq('+ heartItem +')');
            }
        });
    });
}
function unhearted(card_id, heartItem) {
    $(document).ready(function() {
        console.log(heartItem);
        $.ajax({
            type: "POST",
            url: "/unfav",
            data: {"card_id": card_id, "card_fav": false},
            success: function() {
                $(hearts[heartItem]).load(' .heart_buttons:eq('+ heartItem +')');
            }
        });
    });
}

const delete_button = document.getElementById('delete_button');
const check = document.querySelector(".check_delete");
if(delete_button) {
    delete_button.addEventListener('click', () => {
    check.style.display='table';
    editMedia.style.display='none';
    check.scrollIntoView({behavior: "smooth"});
    });
}
const cancel_delete = document.getElementById('cancel_check');
if(cancel_delete) {
    cancel_delete.addEventListener("click", () => {
    check.style.display='none';
    editMedia.style.display='table';
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
const tag_input = document.getElementsByClassName("addTagInput");
function openTag(item){
    addTag[item].style.display="inline";
    add_button[item].style.display="none";
    cancel_tag__button[item].classList.toggle("active");
    tag_input[item].focus();
}
function closeTag(item) {
    addTag[item].style.display="none";
    add_button[item].style.display="inline";
    cancel_tag__button[item].classList.remove("active");
    tag_input[item].value="";
}

const cardIMG = document.getElementsByClassName("card-img-container");
const tagDiv = document.getElementsByClassName("tagForm");
const heartsDiv = document.getElementsByClassName("heart_buttons");
const stats = document.getElementsByClassName("bottom_row");
const seemore = document.getElementsByClassName("see_more");
const less = document.getElementsByClassName("see_less");
const rating = document.getElementsByClassName("rating");
const desc = document.getElementsByClassName("description");
const card = document.getElementsByClassName("card-item");
const edit_button = document.getElementsByClassName("toggleEdit");

function flipCardB(item) {
    card[item].classList.toggle("active"); 
    card[item].classList.remove("unactive");
    cardIMG[item].style.display="none";
    tagDiv[item].style.display="none";
    heartsDiv[item].style.display="none";
    stats[item].style.display="none";
    edit_button[item].style.display="none";
    seemore[item].style.display="none";
    less[item].style.display="grid";
    rating[item].style.display="inline";
    desc[item].style.display="inline";
    
}
function flipCardA(item) {
    card[item].classList.toggle("unactive");
    card[item].classList.remove("active");
    cardIMG[item].style.display="inline";
    tagDiv[item].style.display="inline";
    heartsDiv[item].style.display="inline";
    stats[item].style.display="inline";
    edit_button[item].style.display="inline";
    seemore[item].style.display="inline";
    less[item].style.display="none";
    rating[item].style.display="none";
    desc[item].style.display="none";
}
const newT = document.getElementsByClassName('addTagInput');
const newC = document.getElementsByClassName('cardID');
const newCount = document.getElementsByClassName('tagCount');
const tag_class = document.getElementsByClassName('tagForm');


$(document).ready(function() {
    $(".tagForm").on('submit', function(event) {
        var tagItem = $(this).find(newCount).val();
        $.ajax({
                type: "POST",
                url: "/tag",
                data: {
                    "card_id": $(this).find(newC).val(), 
                    "new_tag": $(this).find(newT).val() 
                },
                success: function(data) {
                    $(tag_class[tagItem]).load(' .tag:eq('+ tagItem +')');
                }
        });
        event.preventDefault();
    });
});
var upcount_card_id = '{{card.id}}';
var upcountItem = "{{counter.count}}";
const ep_on = document.getElementsByClassName("ep-on");
const currentepDiv = document.getElementsByClassName('upcountDiv');
function upcountFunc(upcount_card_id, upcountItem) {
    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: "/upcount",
            data: {"card_id": upcount_card_id},
            success: function() {
                $(currentepDiv[upcountItem]).load(' .ep-on:eq('+upcountItem+')');
            }
        });
    });
}

const search_btn = document.getElementById("search_button");
const search_box = document.getElementById("search_box");
function open_search() {
    if (search_box.style.display!="block") {
        search_box.style.display="block";
        search_btn.classList.toggle('active');
        search_box.focus();
    }
    else {
        search_box.style.display="none";
        search_btn.classList.remove('active');
    }
}
var user_id = '{{user.id}}';
function switch_modes_light(user_id) {
    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: "/light-mode",
            data: {"user_id": user_id},
            success: function() {
                location.reload();
            }
        });
    });

}
function switch_modes_dark(user_id) {   
    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: "/dark-mode",
            data: {"user_id": user_id},
            success: function() {
                location.reload();
            }
        });
    });
}