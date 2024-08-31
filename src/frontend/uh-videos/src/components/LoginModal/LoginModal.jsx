import { useState } from 'react';
// Modal
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

function LoginModal() {
    // Modal
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const handleSubmit = () => {
        console.log('enviando los datos')
    }
    
    return (
        <>
            <Button variant="success" onClick={handleShow}>
            Login
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Welcome again</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label htmlFor="exampleFormControlInput1" className="form-label">Email address</label>
                            <input type="email" className="form-control" id="exampleFormControlInput1" placeholder="name@example.com"/>
                        </div>
                        <div className='d-flex justify-content-center'>
                            <button className="btn btn-primary" type="submit">Submit form</button>
                        </div>
                    </form>
                </Modal.Body>
            </Modal>
        </>
    )
}

export default LoginModal;