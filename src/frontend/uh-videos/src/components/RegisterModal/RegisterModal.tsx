import React, { useState } from 'react';
// Modal
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

function RegisterModal() {
    const [show, setShow] = useState(false);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const handleSubmit = async (event) => {
        event.preventDefault();

        const registerData = {
            username: name,
            email: email,
        };

        try {
            const response = await fetch('http://localhost:8000/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(registerData),
            });

            if (!response.ok) {
                throw new Error('Registration failed');
            }

            handleClose();
        } catch (error) {
            setError('Registration failed: ' + error.message);
        }
    };

    return (
        <>
            <Button variant="primary" onClick={handleShow}>
                Register
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Who are you?</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {error && <p className="text-danger">{error}</p>}
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label htmlFor="name" className="form-label">Name</label>
                            <input
                                type="text"
                                className="form-control"
                                id="username"
                                placeholder="Johnson"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required
                            />
                        </div>
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
                            <button className="btn btn-primary" type="submit">Register</button>
                        </div>
                    </form>
                </Modal.Body>

            </Modal>
        </>
    );
}

export default RegisterModal;
