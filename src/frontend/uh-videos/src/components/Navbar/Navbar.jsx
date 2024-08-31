import 'bootstrap/dist/css/bootstrap.min.css';

function Navbar() {
    return (
      <>
        <nav class="navbar navbar-expand-lg bg-light">            
            <div class="container-fluid">
                <a class="navbar-brand me-0" href="#">Navbar</a>
                <form class="d-flex w-100" role="search">
                    <input class="form-control me-5 ms-5" type="search" placeholder="Search" aria-label="Search"/>
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </nav>
      </>
    )
  }
  
  export default Navbar

