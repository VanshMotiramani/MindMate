import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header className="header">
      <Link to="/" className="logo-container">
        <img 
          src="/src/assets/logo.png" 
          alt="MindMate Logo" 
          style={{ height: '110px', width: 'auto' }}
        />
      </Link>
    </header>
  );
};

export default Header;
