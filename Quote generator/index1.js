let button = document.getElementById('button');
let quote = document.getElementById('quote');

const url ="https://api.quotable.io/random";


let getQuote = ()=>{
    fetch(url)
    .then((data) => data.json())
    .then((items) =>{
       console.log(items.content);
       console.log(items.author);
       quote.innerText = items.content;
       author.innerText= items.author
    });
};
window.addEventListener("load",getQuote);
button.addEventListener("click",getQuote)