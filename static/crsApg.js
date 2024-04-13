const buttonAddClss = document.querySelector('#classAddbtn');
const popup = document.querySelector('.popup-wrapper');
const vAulaB = document.querySelector('.VideoAula')

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
    else if (classNames == 'VideoAulap' || classNames == 'DocumentoAulap')
    {
        e.target.style.backgroundColor = 'red'
    }
    console.log(classNames);
}
