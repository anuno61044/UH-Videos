import React, { useState } from 'react';
// Modal
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

function LoginModal() {
    const [show, setShow] = useState(false);
    const [email, setEmail] = useState('');
    const [error, setError] = useState<string>('');

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const handleSubmit = async (event) => {
        event.preventDefault();

        const loginData = {
            email: email,  // Usando solo el email para autenticar
        };

        try {
            const response = await fetch('http://localhost:8000/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginData),
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            localStorage.setItem('access', data.access);
            localStorage.setItem('refresh', data.refresh);
            handleClose();
            window.location.replace("/")
        } catch (error) {
            setError('Login failed: ' + error.message);
        }
    };

    return (
        <>
            <Button variant="light" onClick={handleShow}>
                Login
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Welcome again</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {error && <p className="text-danger">{error}</p>}
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label htmlFor="email" className="form-label">Email address</label>
                            <input
                                type="email"
                                className="form-control"
                                id="email"
                                placeholder="name@example.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className='d-flex justify-content-center'>
                            <button className="btn btn-primary" type="submit">Submit form</button>
                        </div>
                    </form>
                </Modal.Body>
            </Modal>
        </>
    );
}

export default LoginModal;
