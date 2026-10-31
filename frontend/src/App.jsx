import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Progress from './pages/Progress'
import Tasks from './pages/Tasks'
import Materials from './pages/Materials'
import Login from './pages/Login'
import Settings from './pages/Settings'
function Protected(){ const {user,loading}=useAuth(); const location=useLocation(); if(loading) return <div className="loading-screen">Loading your workspace…</div>; return user ? <div className="app-shell"><Sidebar/><main className="main"><Routes><Route path="/" element={<Dashboard/>}/><Route path="/tasks" element={<Tasks/>}/><Route path="/progress" element={<Progress/>}/><Route path="/materials" element={<Materials/>}/><Route path="/settings" element={<Settings/>}/><Route path="*" element={<Navigate to="/" replace/>}/></Routes></main></div> : <Navigate to="/login" state={{from:location}} replace/> }
export default function App(){ const {user,loading}=useAuth(); if(loading) return <div className="loading-screen">Loading Prep Track…</div>; return <Routes><Route path="/login" element={user?<Navigate to="/" replace/>:<Login/>}/><Route path="*" element={<Protected/>}/></Routes> }
