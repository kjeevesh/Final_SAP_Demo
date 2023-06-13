import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { Link } from 'react-router-dom';
import './styles.css'


function BasicExample() {
  return (
    <><Navbar bg="grey" expand="lg">
      <Container>
        <Navbar.Brand href="/home" className='header'>PwC</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/home" className='header'>Home</Nav.Link>
            <Nav.Link as={Link} to="/contactus" className='header'>Contact Us</Nav.Link>
            <NavDropdown title="Services" id="basic-nav-dropdown" className='header'>
              <NavDropdown.Item href="action/3.1"></NavDropdown.Item>
              <NavDropdown.Item as={Link} to="scheduler">
                Scheduler
              </NavDropdown.Item>
              
              
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
    <br />
    <h1 class="text-big" > Security and business controls monitoring </h1>
    <p class="text-small">


    One of the key objectives of an organization is to manage Governance, risk management and compliance with industry and government regulations. 
    PwC service offering for automated monitoring of Security and Business Controls will manage IT and security risks, reduce costs, and meet compliance requirements. It will also help improve decision-making and performance through an integrated view of how well an organization manages its risks.

    Organizations start the compliance journey with access control monitoring, thereafter, moving to process control for exception-based reporting and monitoring.  Once this is achieved, organizations move to implementing risk management for defining a controlled risk environment using the existing and integrating with the new. 

    This also helps standardization and harmonization of risk, controls and processes across regulation frameworks and acceptance of responsibility for internal controls. Our solution will help cater to all areas thereby developing a better governance system
      </p>

    
      <br />

      <h1 class="text-big" > Regulatory compliance</h1>
      <p class="text-small">
      The best plan of action for regulatory compliance is to have the correct security controls in place to ensure that financial data is accurate and protected against loss
      PwC service offering for automated monitoring of Security and Business Controls provides a feasibility to design security and business controls, which can then be monitored effectively as per a predefined frequency.
      The monitoring process in the solution can be integrated with an ITSM tool to enable a workflow driven assessment which brings in the involvement of multiple team members and stakeholders thereby documenting their responses and actions for better governance and compliance


      </p>
      </>
  );
}

export default BasicExample;