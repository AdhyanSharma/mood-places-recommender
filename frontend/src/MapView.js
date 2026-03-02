import {MapContainer,TileLayer,Marker,Popup} from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function MapView({places,position}){
 return(
<MapContainer center={position} zoom={13} className="map">
<TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>

{places.map((p,i)=>(
<Marker key={i} position={[p.lat,p.lng]}>
<Popup>{p.name}</Popup>
</Marker>
))}
</MapContainer>
);
}