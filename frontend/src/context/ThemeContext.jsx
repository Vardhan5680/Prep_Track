import { createContext, useContext, useEffect, useState } from 'react'
const ThemeContext = createContext(null)
const presets = {
  study: { label: 'Warm study', primary: '#806044', accent: '#a9a16b', background: '#f6f0e5', surface: '#fffdf8', text: '#3d342b' },
  pastel: { label: 'Pastel academic', primary: '#7967b5', accent: '#7aa99a', background: '#f5f1fb', surface: '#ffffff', text: '#342d43' },
  midnight: { label: 'Midnight focus', primary: '#8b83e8', accent: '#65b9b0', background: '#171b2b', surface: '#242a3d', text: '#f0eff8' },
  vibrant: { label: 'Fresh energy', primary: '#287c91', accent: '#d28a43', background: '#edf6f5', surface: '#ffffff', text: '#203b40' }
}
export function ThemeProvider({ children }) {
  const [settings, setSettings] = useState(() => {
    try { return JSON.parse(localStorage.getItem('prep_track_theme')) || { preset: 'study', customPrimary: '', customAccent: '' } }
    catch { return { preset: 'study', customPrimary: '', customAccent: '' } }
  })
  const palette = presets[settings.preset] || presets.study
  useEffect(() => {
    const root = document.documentElement
    root.dataset.theme = settings.preset
    root.style.setProperty('--theme-primary', settings.customPrimary || palette.primary)
    root.style.setProperty('--theme-accent', settings.customAccent || palette.accent)
    root.style.setProperty('--theme-bg', palette.background)
    root.style.setProperty('--theme-surface', palette.surface)
    root.style.setProperty('--theme-text', palette.text)
    localStorage.setItem('prep_track_theme', JSON.stringify(settings))
  }, [settings, palette])
  return <ThemeContext.Provider value={{ settings, setSettings, presets }}>{children}</ThemeContext.Provider>
}
export const useTheme = () => useContext(ThemeContext)
