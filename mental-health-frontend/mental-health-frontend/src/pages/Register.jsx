import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';

const Register = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                setMessage('✅ Registration successful! Redirecting to login...');
                setTimeout(() => navigate('/login'), 3000);
            } else {
                const errorData = await response.json();
                if (response.status === 400 && errorData.detail.includes('exists')) {
                    setMessage('❌ Email already exists. Redirecting to login...');
                    setTimeout(() => navigate('/login'), 3000);
                } else {
                    setMessage('❌ Registration failed.');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            setMessage('❌ Server error. Try again later.');
        }
    };

    return (
        <>
            <div className="page-header-centered">
            <Header />
            <div className="register-container">
                <h2>Register</h2>
                <form onSubmit={handleRegister}>
                    <input 
                        type="email" 
                        placeholder="Email" 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        required 
                    />
                    <input 
                        type="password" 
                        placeholder="Password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required 
                    />
                    <button type="submit">Register</button>
                </form>
                <p>{message}</p>
                <button onClick={() => navigate('/login')}>Go to Login</button>
                </div>
            </div>
        </>
    );
};

export default Register;
