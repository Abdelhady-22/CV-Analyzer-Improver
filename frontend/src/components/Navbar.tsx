/* ── Navbar Component ── */

import { NavLink } from 'react-router-dom';

export default function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-inner">
                <NavLink to="/" className="navbar-brand">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                        <path d="M14 2v6h6" />
                        <path d="M16 13H8" />
                        <path d="M16 17H8" />
                        <path d="M10 9H8" />
                    </svg>
                    CV Analyzer
                </NavLink>

                <div className="navbar-links">
                    <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''} end>
                        Upload
                    </NavLink>
                    <NavLink to="/analysis" className={({ isActive }) => isActive ? 'active' : ''}>
                        Analysis
                    </NavLink>
                    <NavLink to="/generate" className={({ isActive }) => isActive ? 'active' : ''}>
                        Generate
                    </NavLink>
                </div>
            </div>
        </nav>
    );
}
