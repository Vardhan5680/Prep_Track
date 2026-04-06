import { useEffect,useState } from 'react'
import axios from 'axios'
export default function Progress(){ const [items,setItems]=useState([]); useEffect(()=>{axios.get('http://127.0.0.1:8000/progress').then(r=>setItems(r.data))},[]); return <div><h1>Progress</h1>{items.map(i=><p key={i.id}>{i.topic}: {i.solved}/{i.total}</p>)}</div>}