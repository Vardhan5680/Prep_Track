import { useEffect,useState } from 'react'
import axios from 'axios'
export default function Tasks(){ const [tasks,setTasks]=useState([]); useEffect(()=>{axios.get('http://127.0.0.1:8000/tasks').then(r=>setTasks(r.data))},[]); return <div><h1>Tasks</h1>{tasks.map(t=><p key={t.id}>{t.title}</p>)}</div>}