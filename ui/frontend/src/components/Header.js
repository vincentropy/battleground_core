import React from 'react'
import { Navbar, Nav, NavItem,NavDropdown, MenuItem } from 'react-bootstrap';
import {LinkContainer} from 'react-router-bootstrap'

const Header = () =>(
  <Navbar inverse>
    <Navbar.Header>
      <LinkContainer to="/">
      <Navbar.Brand>
        Battleground
      </Navbar.Brand>
    </LinkContainer>
    <Navbar.Toggle />
  </Navbar.Header>

  <Navbar.Collapse>
    <Nav>
      <LinkContainer to="/about">
      <NavItem eventKey={1}>About</NavItem>
    </LinkContainer>
    <LinkContainer to="/games">
    <NavItem eventKey={2}>Observe Games</NavItem>
  </LinkContainer>
</Nav>
</Navbar.Collapse>
</Navbar>
);

export default Header