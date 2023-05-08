import React, { useState } from 'react';
import { Layout, Menu, Button } from 'antd';
import { UploadOutlined, UserOutlined, VideoCameraOutlined, SettingOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const { Sider } = Layout;

// после регистрации есть вкладка добавить
const Sidebar = () => {
    const navigate = useNavigate();

    const [collapsed, setCollapsed] = useState(false);

    const onCollapse = (collapsed) => {
        setCollapsed(collapsed);
    };


    const handleMenuClick = () => {
        navigate('/homogen');
    };

    return (
        <Sider collapsible collapsed={collapsed} onCollapse={onCollapse}>
            <div className="logo" />
            <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">

                <Menu.ItemGroup title="Легкие">
                    <Menu.Item
                        onClick={handleMenuClick}
                        icon={<UserOutlined />}
                        key="unhomogen">
                        Негомогенность
                    </Menu.Item>

                    <Menu.Item icon={<VideoCameraOutlined />} key="mass">Узлы</Menu.Item>
                    <Menu.Item icon={<UploadOutlined />} key="pneumonia">Пневмония</Menu.Item>
                </Menu.ItemGroup>

            </Menu>
        </Sider>
    );
};


export default Sidebar;
