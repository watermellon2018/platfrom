import {Button, Layout} from 'antd';
import '../App.css';
import withAuth from '../components/check_auth'
import {Link, useNavigate} from 'react-router-dom';
import Cookies from 'js-cookie';
import Sidebar from '../components/sidebar'
import {BugOutlined, UserOutlined} from "@ant-design/icons";

import './basic.css'
import {useLayoutEffect} from "react";
import {registerApplication, start} from 'single-spa';

const { Header, Content } = Layout;

const BasicPage = (props) => {

    const navigate = useNavigate();
    const handleLogout = () => {
        Cookies.remove('token');
        navigate('/start')
    };


    return (
        <>
            <Header className="header">
                <div className='logo'>
                    <Link to='/' className="profile-button" style={{color: 'white'}}>
                        <BugOutlined />
                    </Link>
                </div>

                <div className='controller'>
                    <Link to='/profile' className="profile-button" style={{color: 'white'}}>
                        <UserOutlined />
                    </Link>
                    <Button type="primary" key='login' onClick={handleLogout}>Выйти</Button>
                </div>

            </Header>
            <Layout className='main'>
                <Sidebar />

                <Layout style={{ padding: '0 24px 24px' }}>
                    <Content
                        className="site-layout-background"
                        style={{
                            padding: 24,
                            margin: 0,
                            minHeight: 280,
                        }}
                    >
                        <div className="upload-container">
                            {/*{<DicomViewer file='C:\Users\stepa\Downloads\2_skull_ct\DICOM\l0' />}*/}
                            {props.component}
                        </div>
                    </Content>
                </Layout>
            </Layout>
        </>
    );
}

export default withAuth(BasicPage);
