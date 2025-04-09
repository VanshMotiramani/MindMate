import { Link } from "react-router-dom";
import { useTheme } from '../context/ThemeContext';
import '../styles/Header.css';

const Header = () => {
  const { darkMode, toggleTheme } = useTheme();

  return (
    <header className="header">
      <Link to="/" className="logo-container">
        <img
          src="/src/assets/logo.png"
          alt="MindMate Logo"
          style={{ paddingRight: '12rem', height: '110px', width: 'auto' }}
        />
      </Link>

      <button className="theme-toggle-btn" onClick={toggleTheme}>
        {darkMode ? '🌞 Light Mode' : '🌙 Dark Mode'}
      </button>
    </header>
  );
};

export default Header;
