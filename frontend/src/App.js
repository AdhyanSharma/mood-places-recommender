import React,{useState} from "react";
import MapView from "./MapView";
import EmotionDetector from "./EmotionDetector";
import {API} from "./api";
import "./index.css";

export default function App(){

const [mood,setMood]=useState("happy");
const [places,setPlaces]=useState([]);
const [reason,setReason]=useState("");
const [position,setPosition]=useState([21.1458,79.0882]);
const [camera,setCamera]=useState(false);
const [loading,setLoading]=useState(false);

const distance=(a,b,c,d)=>{
 const R=6371;
 const dLat=(c-a)*Math.PI/180;
 const dLon=(d-b)*Math.PI/180;
 const x=Math.sin(dLat/2)**2+
 Math.cos(a*Math.PI/180)*Math.cos(c*Math.PI/180)*Math.sin(dLon/2)**2;
 return (R*(2*Math.atan2(Math.sqrt(x),Math.sqrt(1-x)))).toFixed(2);
};

const fetchPlaces=async(selectedMood)=>{
 setLoading(true);

 navigator.geolocation.getCurrentPosition(async(pos)=>{
  const lat=pos.coords.latitude;
  const lng=pos.coords.longitude;

  setPosition([lat,lng]);

  const res=await API.post("/recommend",{mood:selectedMood,lat,lng});

  setPlaces(res.data.places);
  setReason(res.data.reason);
  setLoading(false);
 });
};

return(
<div className="container">

<h1>🌍 Mood Places Recommender</h1>

<div className="controls">
<select onChange={(e)=>setMood(e.target.value)}>
<option value="happy">😄 Happy</option>
<option value="sad">😢 Sad</option>
<option value="relaxed">🧘 Relaxed</option>
<option value="excited">🔥 Excited</option>
</select>

<button onClick={()=>fetchPlaces(mood)}>Recommend Places</button>
<button onClick={()=>setCamera(!camera)}>🤖 Detect Mood</button>
</div>

{reason && <div className="reason">💡 {reason}</div>}
{loading && <p>Finding nearby places...</p>}
{camera && <EmotionDetector onMood={fetchPlaces}/>}

<MapView places={places} position={position}/>

<div className="cards">
{places.map((p,i)=>(
<div className="card" key={i}>
<h3>{p.name}</h3>
<p>📍 {distance(position[0],position[1],p.lat,p.lng)} km away</p>
⭐ {p.rating}
</div>
))}
</div>

</div>
);
}