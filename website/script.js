const wrapper =  document.querySelector('.wrapper');
const registerLink =  document.querySelector('.re-l');
const loginLink =  document.querySelector('.lg-l');
const btnPopup =  document.querySelector('.cta-button');
const iconClose =  document.querySelector('.i-close');

registerLink.onclick = () => {
    wrapper.classList.add('active');

};
loginLink.onclick = () => {
    wrapper.classList.remove('active');

};
btnPopup.onclick = () => {
    wrapper.classList.add('active-popup');

};

iconClose.onclick = () => {
    wrapper.classList.remove('active-popup');
    wrapper.classList.remove('active');

};
