const buttonAddClss = document.querySelector('#classAddbtn');
const popup = document.querySelector('.popup-wrapper');
const vAulaB = document.querySelector('.VideoAula');
const Vform = document.querySelector('.VAForm');
const Dform = document.querySelector('.DAForm');

const sideb = document.querySelector('.popup-sideb');
let biter = document.createElement('div');

Vform.style.display = 'block'
biter.classList.add('iterator-b')
let row = 0

sideb.appendChild(biter)
popup.addEventListener('click', PopAct);
buttonAddClss.addEventListener('click', addClssRow);

function addClssRow(e) {
    $(popup).fadeIn();
    popup.style.display = 'block';
}

function PopAct(e) {
    const classNames = e.target.classList[0];
    if (classNames == 'popup-close' || classNames == 'popup-wrapper') {
        popup.style.display = 'none';
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
