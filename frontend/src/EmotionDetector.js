import React,{useRef} from "react";
import Webcam from "react-webcam";
import {API} from "./api";

export default function EmotionDetector({onMood}){

const webcamRef=useRef(null);

const capture=async()=>{
 const image=webcamRef.current.getScreenshot();
 const res=await API.post("/detect_mood",{image});
 onMood(res.data.mood);
};

return(
<div>
<Webcam ref={webcamRef} screenshotFormat="image/jpeg" width={300}/>
<br/>
<button onClick={capture}>Capture Mood</button>
</div>
);
}