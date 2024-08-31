import 'bootstrap/dist/css/bootstrap.min.css';

function Navbar() {
    return (
        <nav className="navbar navbar-expand-lg bg-light">            
            <div className="container-fluid">
                <a className="navbar-brand me-0" href="/">Navbar</a>
                <form className="d-flex w-100" role="search">
                    <input className="form-control me-5 ms-5" type="search" placeholder="Search" aria-label="Search"/>
                    <button className="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </nav>
    )
  }
  
  export default Navbar

