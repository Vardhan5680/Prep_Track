import { useTheme } from '../context/ThemeContext'
export default function Settings() {
  const { settings, setSettings, presets } = useTheme()
  return <div className="page">
    <header className="page-header"><div><span className="eyebrow">MAKE IT YOUR STUDY SPACE</span><h1>Study appearance</h1><p className="muted">Choose a calm, motivating look that feels right for your preparation.</p></div></header>
    <section className="panel theme-panel"><div className="panel-head"><div><span className="eyebrow">READY-MADE STYLES</span><h3>Choose your study theme</h3></div></div>
      <div className="theme-grid">{Object.entries(presets).map(([key, theme])=><button type="button" key={key} onClick={()=>setSettings(v=>({...v,preset:key}))} className={`theme-choice ${settings.preset===key?'selected':''}`} style={{'--swatch':theme.primary,'--swatch-accent':theme.accent,'--swatch-bg':theme.background}}><span className="theme-swatches"><i/><i/><i/></span><b>{theme.label}</b><small>{settings.preset===key?'Currently selected':'Select theme'}</small></button>)}</div>
    </section>
    <section className="panel theme-panel"><div className="panel-head"><div><span className="eyebrow">MAKE IT PERSONAL</span><h3>Custom colours</h3></div></div>
      <p className="muted theme-help">Choose your own main and accent colours. Leave a colour unchanged to use the selected theme's default.</p>
      <div className="color-controls"><label>Main colour<input type="color" value={settings.customPrimary||presets[settings.preset].primary} onChange={e=>setSettings(v=>({...v,customPrimary:e.target.value}))}/></label><label>Accent colour<input type="color" value={settings.customAccent||presets[settings.preset].accent} onChange={e=>setSettings(v=>({...v,customAccent:e.target.value}))}/></label></div>
      <button className="btn btn-primary" onClick={()=>setSettings(v=>({...v,customPrimary:'',customAccent:''}))}>Reset custom colours</button>
    </section>
    <p className="progress-note">Your appearance is saved in this browser and will remain selected when you sign out and sign in again on this device.</p>
  </div>
}
