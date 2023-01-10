import React, { useReducer } from "react";
import { Link, NavLink } from "react-router-dom";
import { Button, Container, Dropdown, Icon, Menu, Segment } from "semantic-ui-react";


export default function NavBar() {
    
    return (
        <Segment inverted>
            <Menu inverted secondary>
                <Container >
                    <Menu.Item as={NavLink} to='/' header name='Create Model'>
                        <img src="/assets/logo.svg" alt="logo" color="white" style={{ marginRight: '10px' }} />
                        Bancruptcy Prediction App
                    </Menu.Item>
                    <Menu.Item as={NavLink} to='/model' name='Create Model' />
                    {/* <Menu.Item as={NavLink} to='/s' name='My Companies' /> */}

                    <Menu.Item position="right">

                        <Dropdown item text='Display Options'>
                            <Dropdown.Menu>
                                <Dropdown.Header>Text Size</Dropdown.Header>
                                <Dropdown.Item>Small</Dropdown.Item>
                                <Dropdown.Item>Medium</Dropdown.Item>
                                <Dropdown.Item>Large</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                    </Menu.Item>
                </Container>
            </Menu>
        </Segment>
    )
}