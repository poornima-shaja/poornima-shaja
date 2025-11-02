console.log("welcome to spotify");
//initial the variable
let songIndex = 0;
let audioElement = new Audio('BTS_JIMIN_-_FILTER.mp3');

let masterplay = document.getElementById("masterplay");
let myProgressBar= document.getElementById("myProgressBar");
let gif= document.getElementById("gif");


let songs = [{songName: "filter by Jimin", filePath: "BTS_JIMIN_-_FILTER.mp3", coverPath: "https://upload.wikimedia.org/wikipedia/en/7/76/BTS_-_Life_Goes_On_%28Vinyl%29.png",
songName: "save me", filePath: "BTS-방탄소년단-Save-ME-Official-MV.mp3", coverPath: "songs/",
   
songName: "run", filePath: "RUN - BTS- [PagalWorld.NL].mp3", coverPath: "https://upload.wikimedia.org/wikipedia/en/7/76/BTS_-_Life_Goes_On_%28Vinyl%29.png",
   
songName: "spring", filePath: "Spring Day - BTS- [PagalWorld.NL].mp3", coverPath: "https://upload.wikimedia.org/wikipedia/en/7/76/BTS_-_Life_Goes_On_%28Vinyl%29.png",
   
songName: "life goes on song", filePath: "BTS_JIMIN_-_FILTER.mp3", coverPath: "https://upload.wikimedia.org/wikipedia/en/7/76/BTS_-_Life_Goes_On_%28Vinyl%29.png",
   
songName: "life goes on song", filePath: "BTS_JIMIN_-_FILTER.mp3", coverPath: "https://upload.wikimedia.org/wikipedia/en/7/76/BTS_-_Life_Goes_On_%28Vinyl%29.png",
   
songName: "life goes on song", filePath: "BTS_JIMIN_-_FILTER.mp3", coverPath: "https://upload.wikimedia.org/wikipedia/en/7/76/BTS_-_Life_Goes_On_%28Vinyl%29.png"}
   
   
    ]
//audioElement.play();

//handle play/pause click
masterplay.addEventListener('click' , ()=>{
    if(audioElement.paused || audioElement.currentTime<=0){
        audioElement.play();
        masterplay.classList.remove( 'fa-play-circle');
        masterplay.classList.add( 'fa-pause-circle');
        gif.style.opacity = 1;
    }
    else{
        audioElement.pause();
        masterplay.classList.remove('fa-pause-circle');
        masterplay.classList.add('fa-play-circle');
        gif.style.opacity = 0;
    }
})

//listen to events
audioElement.addEventListener('timeupdate',()=>{
    //update seekbar
    progress = parseInt((audioElement.currentTime/audioElement.duration)* 100);
    myProgressBar.value = progress; 
})

myProgressBar.addEventListener('change',()=>{
    audioElement.currentTime = myProgressBar.value * audioElement.duration/100;
})

