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
const arrow_down = document.querySelector('.arrow_down');

if (acc) {
    acc.addEventListener('click', () => {
        acc_nav.classList.toggle('active');
            arrow_down.classList.toggle('active');
    });
}
const themes = document.getElementById("theme_dropdown");
const mode = document.getElementById('mode');
if (themes) {
    themes.addEventListener('click', () => {
        if(mode.style.display != "flex") {
            mode.style.display="flex";
        }
        else {
            mode.style.display='none';
        }
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
        $.ajax({
            type: "POST",
            url: "/fav",
            data: {"card_id": card_id, "card_fav": true},
            success: function() {
                $(hearts[heartItem]).load(' .heart_buttons:eq('+ heartItem +')');
                test =  $(".hearts").find(".heart_filled");
                setTimeout( () => {
                    $(hearts[heartItem]).find(".heart_filled").toggleClass('animate');
                }, 30)
                setTimeout(() => {
                    $(hearts[heartItem]).find(".heart_filled").removeClass('animate');  
                }, 340)
            }
        });
    });
}
function unhearted(card_id, heartItem) {
    $(document).ready(function() {
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
        editMedia.style.display='flex';
    });
}

const delete_account = document.getElementById("delete_acc_button");
const check_delete = document.querySelector(".check_acc_delete");
if(delete_account) {
    delete_account.addEventListener("click", () => {
        check_delete.style.display='table';
        document.getElementById('account-title').style.display='none';
        accountForm.style.display='none';
        check_delete.scrollIntoView({behavior: "smooth"});
    });
}
const cancel_acc_delete = document.getElementById('cancel_delete');
if(cancel_acc_delete) {
    cancel_acc_delete.addEventListener("click", () => {
        check_delete.style.display='none';
        document.getElementById('account-title').style.display='block';
        accountForm.style.display='flex';
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
const heartsDiv = document.getElementsByClassName("hearts");
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
        var test_tag = $(this).find(newT).val();
        if (test_tag !== "") {
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
        }
        else {
            alert("Error: The tag you tried to enter was blank! Please add one or more characters and try again!");
        }
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


var user_id = '{{user.id}}';
const site_theme = document.querySelector("#site-theme");
function switch_modes_light(user_id) {
    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: "/light-mode",
            data: {"user_id": user_id},
            success: function() {
                site_theme.href = "light-theme.css"; 
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
                site_theme.href = "dark-theme.css";
            }
        });
    });
}
function system_mode(user_id) {   
    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: "/system-mode",
            data: {"user_id": user_id},
            success: function() {    
                site_theme.href = "system-theme.css";
            }
        });
    });
}
const search_search_form = document.getElementById("search_search");
const search_search_input = document.getElementById("search_search_box");
const search_clear_btn = document.getElementById("search_clear_btn");
if(search_search_form){
    search_search_form.addEventListener("click", (event) => {
        search_search_form.classList.toggle('active');
        if(search_search_input.value.length > 0) {
            search_clear_btn.style.visibility='visible';        
        } 
        else {
            search_clear_btn.style.visibility='hidden';
        }  
    });
    function countSearch() {
        if(search_search_input.value.length > 0) {
            search_clear_btn.style.visibility='visible';        
        } 
        else {
            search_clear_btn.style.visibility='hidden';
        }  
    }
    search_clear_btn.addEventListener("click", (event) => {
        document.getElementById('search_search_box').value="";
        search_search_input.focus();  
        search_clear_btn.style.visibility='hidden';
    });
    search_search_form.addEventListener("focusout", () => {
        search_search_form.classList.remove('active');
    });
}
const edit_description = document.getElementById("edit_description");
const active_desc_count = document.getElementById("active_desc_count");
const total_desc_count = document.getElementById('total_desc_count');
function countEditDesc() {
    const maxChara = 850;
    if(edit_description.value.length < maxChara) {
        active_desc_count.innerText = (maxChara - edit_description.value.length);
        total_desc_count.style.display='block';
    }
    else {
        active_desc_count.innerText = "You're at the limit!";
        total_desc_count.style.display='none';
    }
}
const add_description = document.getElementById("add_description");
const add_desc_count = document.getElementById("add_desc_count");
const add_desc_total = document.getElementById('add_desc_total');
function countAddDesc() {
    const maxChara = 850;
    if(add_description.value.length < maxChara) {
        add_desc_count.innerText = (maxChara - add_description.value.length).toString();
        add_desc_total.style.display='block';
    }
    else {
        add_desc_count.innerText = "You're at the limit!";
        add_desc_total.style.display='none';
    }
}
const nav_search = document.getElementById("nav_search");
const nav_search_box = document.getElementById("search_box");
const nav_search_clear_btn = document.getElementById("nav_search_clear_btn");

function countSearchBox() {
    if(nav_search_box.value.length > 0) {
        nav_search_clear_btn.style.visibility='visible';        
    } 
    else {
        nav_search_clear_btn.style.visibility='hidden';
    }  
}
nav_search_clear_btn.addEventListener("click", (event) => {
    document.getElementById('search_box').value="";
    search_box.focus();  
    nav_search_clear_btn.style.visibility='hidden';
});

const modal = document.getElementById('exampleModal')
modal.addEventListener('shown.bs.modal', () => {
    nav_search_box.focus();
});

carouselbgImg = document.getElementById("myCarousel");
if (carouselbgImg) {
    var img_src0 = document.getElementById('img-active0').src;
    var img0 = `url(${img_src0})`;
    var img_src1 = document.getElementById("img-active1").src;
    var img1 = `url(${img_src1})`;
    var img_src2 = document.getElementById("img-active2").src;
    var img2 = `url(${img_src2})`;
    var img_src3 = document.getElementById("img-active3").src;
    var img3 = `url(${img_src3})`;
    var img_src4 = document.getElementById("img-active4").src;
    var img4 = `url(${img_src4})`;

    carouselbgImg.style.backgroundImage=img0;

    carouselbgImg.addEventListener('slide.bs.carousel', event => {
        setTimeout(function(){
            var src = $('.active').find('img').attr('src'); 
            if (event.direction == 'left') {
                switch(src) {
                    case img_src0:
                        carouselbgImg.style.backgroundImage=img1;
                        break;
                    case img_src1:
                        carouselbgImg.style.backgroundImage=img2;
                        break;
                    case img_src2:
                        carouselbgImg.style.backgroundImage=img3;
                        break;
                    case img_src3:
                        carouselbgImg.style.backgroundImage=img4;
                        break;
                    case img_src4:
                        carouselbgImg.style.backgroundImage=img0;        
                        break;
                }
            }
            else {
                switch(src) {
                    case img_src0:
                        carouselbgImg.style.backgroundImage=img4;
                        break;
                    case img_src4:
                        carouselbgImg.style.backgroundImage=img3;
                        break;
                    case img_src3:
                        carouselbgImg.style.backgroundImage=img2;
                        break;
                    case img_src2:
                        carouselbgImg.style.backgroundImage=img1;
                        break;
                    case img_src1:
                        carouselbgImg.style.backgroundImage=img0;        
                        break;
                }
            }
        }, 70);
    });
}
