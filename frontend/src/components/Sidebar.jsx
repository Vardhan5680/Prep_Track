import { Link } from 'react-router-dom'
export default function Sidebar(){
 const item={padding:'12px',display:'block',color:'white',textDecoration:'none'}
 return <aside style={{width:240,background:'#111',color:'#fff',minHeight:'100vh',padding:20}}>
 <h2>Prep Track</h2>
 <Link style={item} to='/'>Dashboard</Link>
 <Link style={item} to='/progress'>Progress</Link>
 <Link style={item} to='/tasks'>Tasks</Link>
 <Link style={item} to='/materials'>Materials</Link>
 </aside>
}