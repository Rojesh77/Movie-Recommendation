document.addEventListener('DOMContentLoaded', function() {
let nextt = document.querySelector('.nextt')
let prevv = document.querySelector('.prevv')

if(nextt && prevv){
nextt.addEventListener('click', function(){
    let items = document.querySelectorAll('.item')
    document.querySelector('.slide').appendChild(items[0])
});

prevv.addEventListener('click', function(){
    let items = document.querySelectorAll('.item')
   let slide = document.querySelector('.slide');
   slide.insertBefore(items[items.length - 1], slide.firstChild)
});
}

});