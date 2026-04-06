import { Routes,Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Progress from './pages/Progress'
import Tasks from './pages/Tasks'
import Materials from './pages/Materials'
export default function App(){ return <div style={{display:'flex',fontFamily:'Arial'}}><Sidebar /><main style={{padding:30,flex:1}}><Routes><Route path='/' element={<Dashboard/>}/><Route path='/progress' element={<Progress/>}/><Route path='/tasks' element={<Tasks/>}/><Route path='/materials' element={<Materials/>}/></Routes></main></div>}