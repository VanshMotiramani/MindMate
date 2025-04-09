import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import '../styles/Home.css';

const Home = () => {
    const navigate = useNavigate();

    return (
        <>
        <div className="page-header-centered">
            <Header />
            <div className="home-container">
                <div className="home-card">
                    <h2>🌿 Welcome to MindMate</h2>
                    <p>
                        Your personal companion for better mental wellness. Track your thoughts, understand your emotions, and grow healthier every day.
                    </p>
                    <button onClick={() => navigate('/login')}>Login</button>
                    <button onClick={() => navigate('/register')}>Register</button>
                </div>
            </div>
        </div>
        </>
    );
};

export default Home;
