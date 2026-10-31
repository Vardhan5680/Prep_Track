import { createContext, useContext, useEffect, useState } from 'react'
import api from '../lib/api'
const AuthContext = createContext(null)
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); const [loading, setLoading] = useState(true)
  useEffect(() => { const token = localStorage.getItem('prep_track_token'); if (!token) { setLoading(false); return }
    api.get('/auth/me').then(r => setUser(r.data)).catch(() => localStorage.removeItem('prep_track_token')).finally(() => setLoading(false))
  }, [])
  const signIn = async (email, password) => { const body = new URLSearchParams({ username: email, password }); const { data } = await api.post('/auth/login', body); localStorage.setItem('prep_track_token', data.access_token); setUser(data.user) }
  const signUp = async (name, email, password) => { const { data } = await api.post('/auth/register', { name, email, password }); localStorage.setItem('prep_track_token', data.access_token); setUser(data.user) }
  const signOut = () => { localStorage.removeItem('prep_track_token'); setUser(null) }
  return <AuthContext.Provider value={{ user, loading, signIn, signUp, signOut }}>{children}</AuthContext.Provider>
}
export const useAuth = () => useContext(AuthContext)
