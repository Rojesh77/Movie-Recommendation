let nextDom =document.getElementsByClassName('next');
let prevDom =document.getElementsByClassName('prev');
let carouselDOm = document.querySelector('.carousel');
let listItemDom = document.querySelector('.carousel .list')
let thumbnailDom = document.querySelector('.carousel .thumbnail')

nextDom.onclick = function(){
  showSlider('next');
}

prevDom = function(){
  showSlider('prev');
}
let timeRunning = 3000;
let timeAutoNext = 7000;
let runTimeOut;
let runAutoRun;
runAutoRun = setTimeout(()=>{
nextDom.click();
}, timeAutoNext);

function showSlider(type){
  let itemslider = document.querySelectorALl('.carousel .list .item')
  let itemThumbnail = document.querySelectorAll('.carousel .thumbnail .item')
}

if (type == 'next'){
  listItemDom.appendChild(itemslider[0]);
  thumbnailDom.appendChild(itemThumbnail[0]);
  carouselDOm.classList.add('next');
}
else{
  let positionLastItem = itemslider.length - 1;
  listItemDom.prepend(itemslider[positionLastItem]);
  thumbnailDom.prepend(itemThumbnail[positionLastItem]);
  carouselDOm.classList.add('prev');
}

clearTimeout(runTimeOut);
runTimeOut = setTimeout(()=>{
  carouselDOm.classList.remove('next');
  carouselDOm.classList.remove('prev');

}, timeRunning);

clearTimeout(runAutoRun);
