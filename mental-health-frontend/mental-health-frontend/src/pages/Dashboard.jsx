import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Dashboard.css';
import Header from '../components/Header';

const Dashboard = () => {
    const [sentiments, setSentiments] = useState([]);
    const [newSentiment, setNewSentiment] = useState('');
    const navigate = useNavigate();

    const token = localStorage.getItem('token');

    const fetchSentiments = async () => {
        try {
            const response = await fetch('http://localhost:8000/sentiments', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setSentiments(data);
            } else {
                navigate('/login');
            }
        } catch (error) {
            console.error('Error fetching sentiments:', error);
            navigate('/login');
        }
    };

    const handleCreateSentiment = async () => {
        if (!newSentiment.trim()) return;

        try {
            const response = await fetch('http://localhost:8000/sentiments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ sentiments: newSentiment }),
            });

            if (response.ok) {
                setNewSentiment('');
                fetchSentiments();
            } else {
                console.error('Failed to create sentiment');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    useEffect(() => {
        if (!token) {
            navigate('/login');
            return;
        }
        fetchSentiments();
    }, [navigate, token]);

    return (
        <>
            <Header />
            <div className="dashboard-container">
                <h2 className="dashboard-title">📊 Your Sentiments</h2>

                {sentiments.length === 0 ? (
                    <p>No sentiments recorded yet.</p>
                ) : (
                    <div className="recommendation-grid">
                        {sentiments.map((s) => (
                            <div key={s.id} className="recommendation-card">
                                <details open className="collapsible">
                                    <summary>📝 {s.sentiments}</summary>

                                    <div className="section">
                                        <h3>🧠 Diagnosis:</h3>
                                        <p>{s.recommendation.status}</p>
                                    </div>

                                    <div className="section">
                                        <h3>🧘 Coping Mechanisms:</h3>
                                        <ul>
                                            {s.recommendation.coping_mechanisms?.map((c, i) => (
                                                <li key={i}>🌱 {c}</li>
                                            ))}
                                        </ul>
                                    </div>

                                    <div className="section">
                                        <h3>🎵 Recommended Songs:</h3>
                                        <div className="music-grid">
                                            {s.recommendation.music?.map((song, index) => (
                                                <div key={index} className="music-card">
                                                    <strong>🎶 {song.track_name}</strong>
                                                    <br />
                                                    <span>🎤 {song.artists}</span>
                                                    <div className="genre">🎧 {song.track_genre}</div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </details>
                            </div>
                        ))}
                    </div>
                )}

                {/* ➕ Add New Sentiment */}
                <div className="add-sentiment-section">
                    <h3>➕ Add New Sentiment</h3>
                    <textarea
                        rows="3"
                        placeholder="Write your sentiment..."
                        value={newSentiment}
                        onChange={(e) => setNewSentiment(e.target.value)}
                    />
                    <button onClick={handleCreateSentiment}>Submit</button>
                </div>

                {/* Logout Button */}
                <button
                    className="logout-btn"
                    onClick={() => {
                        localStorage.removeItem('token');
                        navigate('/login');
                    }}
                >
                    Logout
                </button>
            </div>
        </>
    );
};

export default Dashboard;
