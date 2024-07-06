const delbtncls = document.querySelectorAll('.delbtncls');
const buttonAddClss = document.querySelector('#classAddbtn');
const buttonAddDoc = document.querySelector('#docAddbtn');
const popup = document.querySelector('.popup-wrapper');
const popupD = document.querySelector('#ppwb');
const vAulaB = document.querySelector('.VideoAula');
const Vform = document.querySelector('.VAForm');
const Dform = document.querySelector('.DAForm');
const DformB = document.querySelector('#DFormB');

const sideb = document.querySelector('.popup-sideb');
let biter = document.createElement('div');
Vform.style.display = 'block'
biter.classList.add('iterator-b')
let row = 0

sideb.appendChild(biter)
popup.addEventListener('click', PopAct);
popupD.addEventListener('click', PopAct);

buttonAddClss.addEventListener('click', addClssRow);
if (buttonAddDoc != null) {
    buttonAddDoc.addEventListener('click', addClssRow);
}

for (let i = 0; i < delbtncls.length; i++) {
    delbtncls[i].addEventListener("click", sndDelclss); 
}

function addClssRow(e) {
    if (e.target == buttonAddDoc) {
        $(popupD).fadeIn()
        DformB.style.display = 'block'
    }
    else {
        $(popup).fadeIn();
        popup.style.display = 'block';
    }
}

function PopAct(e) {
    const classNames = e.target.classList[0];
    if (classNames == 'popup-close' || classNames == 'popup-wrapper') {
        popup.style.display = 'none';
        popupD.style.display = 'none';
        // closes popup window
    }
    else if (classNames == 'VideoAulap' || classNames == 'VideoAula')
    {
        row = 0
        biter.style.top = '0%'
        Dform.style.display = 'none'
        Vform.style.display = 'block'
    }
    else if (classNames == 'DocumentoAulap' || classNames == 'DocumentoAula')
    {
        row = 1
        biter.style.top = row*40 + 'px'
        Vform.style.display = 'none'
        Dform.style.display = 'block'
    }
    console.log(classNames);
}

let allClass = document.getElementsByClassName('delbtncls');

for (var i = 0; i < allClass.length; i++) {
    allClass[i].addEventListener('click', sndDelclss);
}

function sndDelclss(e) {
    if (confirm("Tem certeza que deseja deletar aula?") == false) {
        return "canceled"
    }
    else {
        $.ajax({
            type: "POST",
            url: "/classMDel",
            data: {
                "id": e.target.name
            },
            success: function(data) {
                console.log("Course deleted successfully");
                window.location.href = `/coursePgRdr/${coursid}/1`;
            },
            error: function(xhr, status, error) {
                //console.log("Error deleting class: ", error);
                window.location.href = `/coursePgRdr/${coursid}/1`;
            }
        });
    }
}