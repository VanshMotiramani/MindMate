import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import '../styles/Login.css';
import api from '../api/axios';


const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loginError, setLoginError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoginError('');
    
        try {
            const formData = new URLSearchParams();
            formData.append("username", email);
            formData.append("password", password);
    
            const response = await api.post('/login', formData, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            });
    
            localStorage.setItem("token", response.data.token);
            navigate("/dashboard");
    
        } catch (error) {
            if (error.response && error.response.data) {
                setLoginError(error.response.data.detail || "Login failed. Please try again.");
            } else {
                setLoginError("Server error. Please try again later.");
            }
            console.error("Login error:", error);
        }
    };
    
    return (
        <>
            <div className="page-header-centered">
                <Header />
                <div className="login-container">
                    <h2>Login</h2>
                    <form onSubmit={handleLogin}>
                        <input
                            type="email"
                            name="email"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            autoComplete="email"
                            required
                        />
                        <input
                            type="password"
                            name="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            autoComplete="current-password"
                            required
                        />
                        <button type="submit">Login</button>
                    </form>

                    {loginError && <p className="error-message">{loginError}</p>}

                    <button onClick={() => navigate('/register')}>Go to Register</button>
                </div>
            </div>
        </>
    );
};

export default Login;
