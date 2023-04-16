
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
                // setTimeout( () => {
                //     $(hearts[heartItem]).find(".heart_filled").toggleClass('animate');
                // }, 40)
                // setTimeout(() => {
                //     $(hearts[heartItem]).find(".heart_filled").removeClass('animate');  
                // }, 500)
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

var upcount_card_id = '{{card.id}}';
var upcountItem = "{{counter.count}}";
var card_title = "{{card.title}}";
const ep_on = document.getElementsByClassName("ep-on");
const currentepDiv = document.getElementsByClassName('upcountDiv');
var inputCurrentEp = document.getElementsByClassName('inputCurrentEp');
var modalCurrentEp = document.getElementsByClassName('modalCurrentEp');
var currentEp = document.getElementsByClassName('currentEp');
var totalEp = document.getElementsByClassName('totalEp');
function upcountFunc(upcount_card_id, upcountItem, cardTitle) {
    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: "/upcount",
            data: {"card_id": upcount_card_id},
            success: function() {
                $(currentepDiv[upcountItem]).load(' .ep-on:eq('+upcountItem+')');
                $(modalCurrentEp[upcountItem]).load(' .inputCurrentEp:eq('+upcountItem+')');
                $('.hidden_input1:eq('+upcountItem+')').load(' .currentEp:eq('+upcountItem+')');
                testCall(upcountItem, cardTitle, upcount_card_id);
            }
        });
    });
}      
const upcountButton = document.getElementsByClassName('upcount');
function testCall(upcountItem, cardTitle, upcount_card_id) {
    var epX = +currentEp[upcountItem].value;
    var new_ep = epX + 1;
    if (totalEp[upcountItem].value != "?") {
        var totalX = Number(totalEp[upcountItem].value);
        if (new_ep == totalX) {
            upcountButton[upcountItem].style.display='none'; 
            setTimeout( () => {
                let text = cardTitle + " seems to be completed. Would you like to move " + cardTitle + " to your completed list?";
                if (confirm(text) == true) {
                    changeStatus(upcount_card_id)
                }
            }, 100);           
        }
    }
}
function changeStatus(upcount_card_id) {
    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: "/change-status",
            data: {"card_id": upcount_card_id},
            success: function() {
                window.location.reload();
            }
        });
    });    
}

var user_id = '{{user.id}}';
const theme_name = document.getElementById("theme_title");


const site_theme = document.querySelector("#site-theme");
function switch_modes_light(user_id) {
    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: "/light-mode",
            data: {"user_id": user_id},
            success: function() {
                site_theme.href = "light-theme.css"; 
                $(theme_name).load(' #theme_title');
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
                $(theme_name).load(' #theme_title');
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
                $(theme_name).load(' #theme_title');
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
const edit_description = document.getElementsByClassName("edit_description");
const active_desc_count = document.getElementsByClassName("active_desc_count");
const total_desc_count = document.getElementsByClassName('total_desc_count');
var edit_card_count = '{{counter.count}}'
function countEditDesc(edit_card_count) {
    const maxChara = 850;
    console.log(edit_card_count);
    if(edit_description[edit_card_count].value.length < maxChara) {
        active_desc_count[edit_card_count].innerText = (maxChara - edit_description[edit_card_count].value.length);
        total_desc_count[edit_card_count].style.display='block';
    }
    else {
        active_desc_count[edit_card_count].innerText = "You're at the limit!";
        total_desc_count[edit_card_count].style.display='none';
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
carouselbgImg1 = document.getElementById("myCarousel1");
if (carouselbgImg1) {
    var lesser_img_src0 = document.getElementById('lesser-img-active0').src;
    var lesser_img0 = `url(${lesser_img_src0})`;
    var lesser_img_src1 = document.getElementById("lesser-img-active1").src;
    var lesser_img1 = `url(${lesser_img_src1})`;
    var lesser_img_src2 = document.getElementById("lesser-img-active2").src;
    var lesser_img2 = `url(${lesser_img_src2})`;

    carouselbgImg1.style.backgroundImage=lesser_img0;

    carouselbgImg1.addEventListener('slide.bs.carousel', event => {
        setTimeout(function(){
            var src = $('.active').find('img').attr('src'); 
            if (event.direction == 'left') {
                switch(src) {
                    case lesser_img_src0:
                        carouselbgImg1.style.backgroundImage=lesser_img1;
                        break;
                    case lesser_img_src1:
                        carouselbgImg1.style.backgroundImage=lesser_img2;
                        break;
                    case lesser_img_src2:
                        carouselbgImg1.style.backgroundImage=lesser_img0;
                        break;
                }
            }
            else {
                switch(src) {
                    case lesser_img_src0:
                        carouselbgImg1.style.backgroundImage=lesser_img2;
                        break;
                    case lesser_img_src2:
                        carouselbgImg1.style.backgroundImage=lesser_img1;
                        break;
                    case lesser_img_src1:
                        carouselbgImg1.style.backgroundImage=lesser_img0;        
                        break;
                }
            }
        }, 70);
    });
}
var tagCounterId = "{{counter.tag}}";
const expand_tag = document.getElementsByClassName("expand_more");
const expand_exta = document.getElementsByClassName("expand_extra");
const expand_edit = document.getElementsByClassName("expand_edit")
const expand_delete = document.getElementsByClassName("expand_delete")
function expandMoreTag(tagCounterId) {
    expand_tag[tagCounterId].classList.toggle("active");
    if(expand_tag[tagCounterId].classList.contains("active")) {
        expand_exta[tagCounterId].innerText="chevron_left";
        expand_edit[tagCounterId].style.display='contents';
        expand_delete[tagCounterId].style.display='contents';
    }
    else {
        expand_edit[tagCounterId].style.display='none';
        expand_delete[tagCounterId].style.display='none';
        expand_exta[tagCounterId].innerText="chevron_right";
    }
}
const updateTagInput = document.getElementsByClassName('input_tag_name');
const updateTagCount = document.getElementsByClassName('updateTagCounter');

var cardId = '{{card.id}}';
var tagId = '{{tag.id}}';
var tagEditItem = '{{counter.tag}}'
var tag_card_counter = '{{counter.counter}}'
var tagName = document.getElementsByClassName('tag-name');
var input_tag = document.getElementsByClassName('input_tag_name');
var updateTagId = document.getElementsByClassName('updateTagId');
var updateTagDiv = document.getElementsByClassName('tagTest');
var editTagForm = document.getElementsByClassName('editTagForm');

function edit_tag(tagId, tag_card_counter, tagEditItem) {
    tagName[tagEditItem].style.display='none';
    input_tag[tagEditItem].setAttribute('type','text');
    input_tag[tagEditItem].setAttribute('size', input_tag[tagEditItem].getAttribute('placeholder').length);
    input_tag[tagEditItem].focus();
    $(editTagForm[tag_card_counter]).on('keypress', function(e) {
        var key = e.which;
        if (key == 13 && input_tag[tagEditItem].value != "") {
            $.ajax({
                type: "POST",
                url: "/update_tag",
                data: {
                    "tag_id": $(updateTagId[tagEditItem]).val(),
                    "tag_update": $(input_tag[tagEditItem]).val()
                },
                success: function() {
                    for (i = 0; i < editTagFormDiv.length; ++i) {
                        $(editTagForm[i]).load(' .tag:eq('+ i +')');
                    }
                }
            });  
            e.preventDefault();  
        }
    });
}
var tagId = '{{tag.id}}';
var tagDeleteItem = '{{counter.count}}';
function delete_tag(tagId, tagDeleteItem) {
    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: "/delete_tag",
            data: {"tag_id": tagId},
            success: function() {
                for (i = 0; i < editTagFormDiv.length; ++i) {
                    $(editTagForm[i]).load(' .tag:eq('+ i +')');
                  }
                $('.addTagWrapper:eq(' + tagDeleteItem +')').load(' .addTagForm:eq(' + tagDeleteItem +')');

            }
        });
    });
}

const addTag = document.getElementsByClassName("tagForm");
const add_button = document.getElementsByClassName("plus_tag_button");
const cancel_tag__button = document.getElementsByClassName("cancel_tag_button");
const tag_input = document.getElementsByClassName("addTagInput");
var tagCounterItem = "{{counter.count}}";
function openTag(tagCounterItem){
    console.log("open tag", tagCounterItem);
    addTag[tagCounterItem].style.display="block";
    add_button[tagCounterItem].style.display="none";
    cancel_tag__button[tagCounterItem].classList.toggle("active");
    tag_input[tagCounterItem].focus();
}
function closeTag(tagCounterItem) {
    console.log("close tag", tagCounterItem);
    addTag[tagCounterItem].style.display="none";
    add_button[tagCounterItem].style.display="inline";
    cancel_tag__button[tagCounterItem].classList.remove("active");
    tag_input[tagCounterItem].value="";
}



const newT = document.getElementsByClassName('addTagInput');
const newC = document.getElementsByClassName('cardID');
var tag_number = document.getElementsByClassName('tag_num');
const newCount = document.getElementsByClassName('tagCount');
const divtag = document.getElementsByClassName('divtag');
const tagForm = document.getElementsByClassName('tagForm');
var editTagFormDiv = document.querySelectorAll('.editTagForm');
$(document).ready(function() {
    $(".tagForm").on('submit', function(event) {
        var tagItem = $(this).find(newCount).val();
        var test_tag = $(this).find(newT).val();
        var tag_num = $(this).find(tag_number).val();
        if (test_tag !== "") {
           $.ajax({
                type: "POST",
                url: "/tag",
                data: {
                    "card_id": $(this).find(newC).val(), 
                    "new_tag": $(this).find(newT).val() 
                },
                success: function(data) {
                    for (i = 0; i < editTagFormDiv.length; ++i) {
                        $(editTagForm[i]).load(' .tag:eq('+ i +')');
                      }
                     
                    $('.addTagWrapper:eq(' + tagItem +')').load(' .addTagForm:eq(' + tagItem +')');
                    setTimeout( () => {
                        addTag[tagItem].style.display="none";
                    }, 132)
                }
            });  
        }
        event.preventDefault();
    });
});


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
    setTimeout(() => {
        cardIMG[item].style.display="none";
        tagDiv[item].style.display="none";
        heartsDiv[item].style.display="none";
        stats[item].style.display="none";
        edit_button[item].style.display="none";
        seemore[item].style.display="none";
        editTagForm[item].style.display='none';
    }, 132)
    setTimeout( () => {
        less[item].style.display="grid";
        rating[item].style.display="inline";
        desc[item].style.display="inline";
    }, 150)
   
}
function flipCardA(item) {
    card[item].classList.toggle("unactive");
    card[item].classList.remove("active");
    setTimeout(() => {
        less[item].style.display="none";
        rating[item].style.display="none";
        desc[item].style.display="none";
    }, 135)
    
    setTimeout( () => {    
        cardIMG[item].style.display="inline";
        tagDiv[item].style.display="inline";
        heartsDiv[item].style.display="inline";
        stats[item].style.display="inline";
        edit_button[item].style.display="inline";
        seemore[item].style.display="inline";
        editTagForm[item].style.display='inline';
        addTag[item].style.display="none";
    }, 150)
    
}
const releaseStatInput = document.getElementById("release_input");
$(document).ready(function() {
    $("#releaseStatSelect").on('change', function(){
        if ($(this).val() == "Currently Releasing") {
            releaseStatInput.placeholder="Enter the release schedule (ex. Weekly on Wednesdays)";
            releaseStatInput.setAttribute('type','text');
        }
        else if (($(this).val() == "Scheduled Release")) {
            releaseStatInput.placeholder="Enter the release date (ex. April 11, 2023)";
            releaseStatInput.setAttribute('type','date');
        }
        else {
            releaseStatInput.setAttribute('type','hidden');
        }
    });   
});

const editreleaseStatInput = document.getElementsByClassName("editReleaseInput");
const editReleaseStatClass = document.getElementsByClassName("edit_releaseStatSelect");
$(document).ready(function() {
    for(let i = 0; i < editReleaseStatClass.length; i++){
            editReleaseStatClass[i].addEventListener("click", function() {
                $(editReleaseStatClass[i]).on('change', function(){
                if ($(editReleaseStatClass[i]).val() == "Currently Releasing") {                    
                    editreleaseStatInput[i].setAttribute('type','text');

                    if (editreleaseStatInput[i].placeholder == "") {
                        editreleaseStatInput[i].placeholder = "Enter the release schedule (ex. Weekly on Wednesdays)";
                    }
                }
                else if (($(editReleaseStatClass[i]).val() == "Scheduled Release")) {
                    if (editreleaseStatInput[i].placeholder == "") {
                        editreleaseStatInput[i].placeholder = "Enter the release date (ex. April 11, 2023)";
                    }
                    editreleaseStatInput[i].setAttribute('type','date');
                }
                else {
                    editreleaseStatInput[i].setAttribute('type','hidden');
                }
            }); 
        })
    
    
    }
      
});
const containerRA_Right = document.getElementById("currentreleasesMoreRight");
const containerRA_Left = document.getElementById("currentreleasesMoreLeft");
const containerRA_Div = document.getElementById("currentreleasesArrowsDiv");
const releaseContainerA = document.getElementById("releases-containerA");

var scrollAmount = 0;
var scrollMin = 0
if (containerRA_Div) {
    containerRA_Left.onclick = function () {
        releaseContainerA.scrollTo({
            top: 0,
            left: scrollAmount -= 1200,
            behavior: 'smooth'
        });
    };

    containerRA_Right.onclick = function () {
        releaseContainerA.scrollTo({
            top: 0,
            left: scrollAmount += 1200,
            behavior: 'smooth'
        });
    };
    
}
    

const containerRB_Right = document.getElementById("schedreleasesMoreRight");
const containerRB_Left = document.getElementById("schedreleasesMoreLeft");
const containerRB_Div = document.getElementById("schedreleasesArrowsDiv");
const releaseContainerB = document.getElementById("releases-containerB");

if(containerRB_Div) {
    containerRB_Left.onclick = function () {
        releaseContainerB.scrollTo({
            top: 0,
            left: scrollAmount -= 1200,
            behavior: 'smooth'
        });
    };

    containerRB_Right.onclick = function () {
        releaseContainerB.scrollTo({
            top: 0,
            left: scrollAmount += 1200,
            behavior: 'smooth'
        });
    };
}

const containerRC_Right = document.getElementById("unreleasedMoreRight");
const containerRC_Left = document.getElementById("unreleasedMoreLeft");
const containerRC_Div = document.getElementById("unreleasedArrowsDiv");
const releaseContainerC = document.getElementById("releases-containerC");

if (containerRC_Div) {
    containerRC_Left.onclick = function () {
        releaseContainerC.scrollTo({
            top: 0,
            left: scrollAmount -= 1200,
            behavior: 'smooth'
        });
    };

    containerRC_Right.onclick = function () {
        releaseContainerC.scrollTo({
            top: 0,
            left: scrollAmount += 1200,
            behavior: 'smooth'
        });
    };  
}


    
  